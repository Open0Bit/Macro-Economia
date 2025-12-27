"""
Script: 02_leadlag_analysis.py
Descrição: Analisa a relação temporal (quem lidera e quem segue) entre 
o Estresse Financeiro e o Fluxo de Capitais (ETFs).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import grangercausalitytests, ccf
import os

# Configuração de Estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("talk")

def load_data():
    """Carrega o dataset mestre"""
    print("[1/3] Carregando dados processados...")
    df = pd.read_csv('data/processed/master_dataset.csv', index_col=0, parse_dates=True)
    return df

def analyze_cross_correlation(df, target_flow='China_Tech_Flow_Index', max_lag=30):
    """
    Calcula correlação cruzada com defasagem (Lead-Lag).
    
    Se Lag < 0: Estresse HOJE se correlaciona com Fluxo no PASSADO (Fluxo Lidera)
    Se Lag > 0: Estresse HOJE se correlaciona com Fluxo no FUTURO (Estresse Lidera)
    """
    print(f"\n[2/3] Analisando Correlação Cruzada: Estresse vs {target_flow}...")
    
    # Prepara séries (usando diferenças para focar em mudanças, não níveis)
    # Invertemos o fluxo, pois queremos ver se "Aumento de Estresse" causa "Queda de Fluxo"
    # Mas correlação negativa já indicaria isso. Vamos manter original.
    
    stress = df['China_Stress_Index'].diff().fillna(0)
    flow = df[target_flow].diff().fillna(0)
    
    # Calcular CCF (Cross Correlation Function)
    # O statsmodels ccf retorna apenas lags positivos (future). 
    # Precisamos fazer manualmente para ver passado e futuro.
    
    lags = np.arange(-max_lag, max_lag + 1)
    correlations = []
    
    for lag in lags:
        if lag < 0:
            # Fluxo deslocado para trás (Stress vs Fluxo Passado)
            corr = stress.corr(flow.shift(abs(lag)))
        else:
            # Fluxo deslocado para frente (Stress vs Fluxo Futuro)
            corr = stress.corr(flow.shift(-lag))
        correlations.append(corr)
    
    # Criar DataFrame para plotar
    ccf_df = pd.DataFrame({'Lag': lags, 'Correlation': correlations})
    
    # Visualização
    plt.figure(figsize=(12, 6))
    colors = ['red' if c < 0 else 'blue' for c in ccf_df['Correlation']]
    plt.bar(ccf_df['Lag'], ccf_df['Correlation'], color=colors, alpha=0.7)
    
    plt.axvline(0, color='black', linestyle='--', linewidth=1)
    plt.title(f'Lead-Lag: Estresse Financeiro vs {target_flow}\n(Barras Negativas = Fluxo cai quando Estresse sobe)')
    plt.xlabel('Defasagem (Dias)\n<-- Fluxo Lidera (Antecipa) | Estresse Lidera (Reage) -->')
    plt.ylabel('Correlação de Pearson')
    
    # Destacar o pico
    peak_corr = ccf_df.loc[ccf_df['Correlation'].abs().idxmax()]
    plt.annotate(f"Pico: {peak_corr['Lag']} dias", 
                 xy=(peak_corr['Lag'], peak_corr['Correlation']),
                 xytext=(peak_corr['Lag'], peak_corr['Correlation'] + 0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    output_path = f'figures/lead_lag_{target_flow}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ✓ Gráfico salvo em {output_path}")
    plt.close()
    
    return ccf_df

def run_granger_causality(df, target_flow='China_Tech_Flow_Index', max_lag=10):
    """
    Teste de Causalidade de Granger.
    Verifica se X ajuda a prever Y melhor que apenas o passado de Y.
    """
    print(f"\n[3/3] Teste de Causalidade de Granger ({target_flow})...")
    
    # Granger exige estacionaridade. Usaremos as diferenças (retornos/mudanças).
    data_diff = df[['China_Stress_Index', target_flow]].diff().dropna()
    
    # 1. Stress Causa Fluxo? (Stress -> Fluxo)
    print(f"  A. Teste: Estresse -> Causa -> Fluxo?")
    # O statsmodels recebe (Y, X) na ordem: (coluna afetada, coluna causadora)
    gc_res_1 = grangercausalitytests(data_diff[[target_flow, 'China_Stress_Index']], 
                                     maxlag=[1, 3, 5, 10], verbose=False)
    
    # 2. Fluxo Causa Stress? (Fluxo -> Causa -> Stress)
    print(f"  B. Teste: Fluxo (Investidor) -> Antecipa -> Estresse?")
    gc_res_2 = grangercausalitytests(data_diff[['China_Stress_Index', target_flow]], 
                                     maxlag=[1, 3, 5, 10], verbose=False)
    
    # Função auxiliar para extrair o melhor p-valor
    def get_best_pvalue(results):
        best_p = 1.0
        best_lag = 0
        for lag, test in results.items():
            # Pega o p-valor do teste SSR F-test
            p_val = test[0]['ssr_ftest'][1]
            if p_val < best_p:
                best_p = p_val
                best_lag = lag
        return best_p, best_lag

    p1, lag1 = get_best_pvalue(gc_res_1)
    p2, lag2 = get_best_pvalue(gc_res_2)
    
    print("\n  RESUMO DOS RESULTADOS (P-Valor < 0.05 indica causalidade):")
    print(f"  1. Estresse causa Fluxo? p={p1:.4f} (Lag {lag1})")
    print(f"  2. Fluxo antecipa Estresse? p={p2:.4f} (Lag {lag2})")
    
    interpretation = ""
    if p1 < 0.05 and p2 >= 0.05:
        interpretation = "CONCLUSÃO: Reativo. O mercado reage ao estresse oficial."
    elif p2 < 0.05 and p1 >= 0.05:
        interpretation = "CONCLUSÃO: Preditivo. Investidores saem ANTES do estresse subir."
    elif p1 < 0.05 and p2 < 0.05:
        interpretation = "CONCLUSÃO: Feedback Loop. Um alimenta o outro (vicioso)."
    else:
        interpretation = "CONCLUSÃO: Sem relação estatística clara no curto prazo."
        
    print(f"  >> {interpretation}")
    
    # Salvar resumo em texto
    with open('output/granger_results.txt', 'a') as f:
        f.write(f"\n--- {target_flow} ---\n")
        f.write(f"Stress -> Fluxo: p={p1:.4f}\n")
        f.write(f"Fluxo -> Stress: p={p2:.4f}\n")
        f.write(f"{interpretation}\n")

if __name__ == "__main__":
    # Criar pastas se não existirem
    os.makedirs('figures', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # Limpar log anterior
    if os.path.exists('output/granger_results.txt'):
        os.remove('output/granger_results.txt')

    df = load_data()
    
    # Analisar Tech (KWEB) - Setor mais sensível
    if 'China_Tech_Flow_Index' in df.columns:
        analyze_cross_correlation(df, 'China_Tech_Flow_Index')
        run_granger_causality(df, 'China_Tech_Flow_Index')
    
    # Analisar Large Caps (FXI) - Mercado geral
    if 'China_Large_Flow_Index' in df.columns:
        analyze_cross_correlation(df, 'China_Large_Flow_Index')
        run_granger_causality(df, 'China_Large_Flow_Index')
        
    print("\nSUCESSO! Gráficos salvos em 'figures/'.")
    print("Próximo passo: python scripts/03_synchronization.py")