"""
Script 02: Analise Lead-Lag e Causalidade de Granger
Framework: Preparacao Assimetrica e Crises Sistemicas
Autor: Gabriel W. Soares
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend nao-interativo para evitar problemas de memoria
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
import warnings
import os
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def check_stationarity(series, name):
    """Testa estacionariedade usando Augmented Dickey-Fuller"""
    result = adfuller(series.dropna())
    
    print(f"\n  Teste ADF para {name}:")
    print(f"    ADF Statistic: {result[0]:.4f}")
    print(f"    p-value: {result[1]:.4f}")
    
    if result[1] <= 0.05:
        print(f"    -> Serie e estacionaria (p<0.05)")
        return True
    else:
        print(f"    -> Serie NAO e estacionaria (p>0.05)")
        return False

def compute_cross_correlation(x, y, max_lag=12):
    """Calcula correlacao cruzada entre duas series"""
    correlations = []
    lags = range(-max_lag, max_lag + 1)
    
    for lag in lags:
        if lag < 0:
            corr = x.iloc[:lag].corr(y.iloc[-lag:])
        elif lag > 0:
            corr = x.iloc[lag:].corr(y.iloc[:-lag])
        else:
            corr = x.corr(y)
        
        correlations.append(corr)
    
    return pd.Series(correlations, index=lags)

def cross_correlation_analysis():
    """Analise de correlacao cruzada"""
    print("\n[1/4] Analise de Correlacao Cruzada...")
    
    monthly = pd.read_csv('data/processed/monthly_data.csv', 
                          index_col=0, parse_dates=True)
    
    if 'DELTA_EXPOSURE_RATIO' not in monthly.columns or 'DELTA_STRESS_INDEX' not in monthly.columns:
        print("  [ERRO] Variaveis necessarias nao encontradas")
        return None
    
    exposure = monthly['DELTA_EXPOSURE_RATIO'].dropna()
    stress = monthly['DELTA_STRESS_INDEX'].dropna()
    
    common_index = exposure.index.intersection(stress.index)
    exposure = exposure.loc[common_index]
    stress = stress.loc[common_index]
    
    ccf = compute_cross_correlation(exposure, stress, max_lag=6)
    
    print(f"\n  Correlacoes Cruzadas (Exposure x Stress):")
    print(f"  {'Lag':<6} {'Corr':<8} {'Interpretacao'}")
    print("  " + "-"*50)
    
    for lag in range(-6, 7):
        corr = ccf[lag]
        
        if lag < 0:
            interpretation = "Exposure precede Stress"
        elif lag > 0:
            interpretation = "Stress precede Exposure"
        else:
            interpretation = "Contemporaneo"
        
        marker = "***" if abs(corr) > 0.3 else ("**" if abs(corr) > 0.2 else "*" if abs(corr) > 0.1 else "")
        print(f"  {lag:6d} {corr:8.3f} {marker:4s} {interpretation}")
    
    # Visualizar
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].stem(ccf.index, ccf.values, basefmt=" ")
    axes[0].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    axes[0].axhline(y=0.2, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
    axes[0].axhline(y=-0.2, color='r', linestyle='--', linewidth=0.5, alpha=0.5)
    axes[0].set_xlabel('Lag (meses)')
    axes[0].set_ylabel('Correlacao')
    axes[0].set_title('Funcao de Correlacao Cruzada\nDelta-Exposure x Delta-Stress')
    axes[0].grid(True, alpha=0.3)
    
    max_neg_lag = ccf.idxmin()
    max_neg_corr = ccf.min()
    
    axes[1].plot(exposure.index, exposure.values, label='Delta-Exposure', alpha=0.7)
    axes[1].plot(stress.index, stress.values, label='Delta-Stress', alpha=0.7)
    axes[1].set_xlabel('Data')
    axes[1].set_ylabel('Valor')
    axes[1].set_title('Series Temporais (Mudancas Mensais)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/cross_correlation.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"\n  [OK] Grafico salvo: figures/cross_correlation.png")
    
    print(f"\n  Lag de maxima correlacao negativa: {max_neg_lag} meses (r={max_neg_corr:.3f})")
    if max_neg_lag < 0:
        print(f"  -> Exposicao tende a PRECEDER estresse em {abs(max_neg_lag)} meses")
    
    return ccf

def granger_causality_test():
    """Teste de Causalidade de Granger"""
    print("\n[2/4] Teste de Causalidade de Granger...")
    
    monthly = pd.read_csv('data/processed/monthly_data.csv', 
                          index_col=0, parse_dates=True)
    
    data = monthly[['DELTA_STRESS_INDEX', 'DELTA_EXPOSURE_RATIO']].dropna()
    
    if len(data) < 30:
        print(f"  [ERRO] Dados insuficientes: {len(data)} observacoes")
        return None
    
    print(f"  Dados: {len(data)} observacoes mensais")
    
    print("\n  Verificando estacionariedade...")
    check_stationarity(data['DELTA_STRESS_INDEX'], 'Delta-Stress')
    check_stationarity(data['DELTA_EXPOSURE_RATIO'], 'Delta-Exposure')
    
    # Teste 1
    print("\n  " + "="*50)
    print("  TESTE 1: Delta-Exposure -> Delta-Stress")
    print("  H0: Delta-Exposure NAO causa Granger Delta-Stress")
    print("  " + "="*50)
    
    try:
        result_1 = grangercausalitytests(
            data[['DELTA_STRESS_INDEX', 'DELTA_EXPOSURE_RATIO']], 
            maxlag=6,
            verbose=False
        )
        
        print(f"\n  {'Lag':<6} {'F-stat':<10} {'p-value':<10} {'Resultado'}")
        print("  " + "-"*50)
        
        for lag in range(1, 7):
            f_stat = result_1[lag][0]['ssr_ftest'][0]
            p_value = result_1[lag][0]['ssr_ftest'][1]
            
            if p_value < 0.01:
                result = "Rejeita H0 ***"
            elif p_value < 0.05:
                result = "Rejeita H0 **"
            elif p_value < 0.10:
                result = "Rejeita H0 *"
            else:
                result = "Nao rejeita H0"
            
            print(f"  {lag:<6} {f_stat:<10.3f} {p_value:<10.4f} {result}")
    
    except Exception as e:
        print(f"  [ERRO] Erro no teste: {str(e)}")
    
    # Teste 2
    print("\n  " + "="*50)
    print("  TESTE 2: Delta-Stress -> Delta-Exposure")
    print("  H0: Delta-Stress NAO causa Granger Delta-Exposure")
    print("  " + "="*50)
    
    try:
        result_2 = grangercausalitytests(
            data[['DELTA_EXPOSURE_RATIO', 'DELTA_STRESS_INDEX']], 
            maxlag=6,
            verbose=False
        )
        
        print(f"\n  {'Lag':<6} {'F-stat':<10} {'p-value':<10} {'Resultado'}")
        print("  " + "-"*50)
        
        for lag in range(1, 7):
            f_stat = result_2[lag][0]['ssr_ftest'][0]
            p_value = result_2[lag][0]['ssr_ftest'][1]
            
            if p_value < 0.01:
                result = "Rejeita H0 ***"
            elif p_value < 0.05:
                result = "Rejeita H0 **"
            elif p_value < 0.10:
                result = "Rejeita H0 *"
            else:
                result = "Nao rejeita H0"
            
            print(f"  {lag:<6} {f_stat:<10.3f} {p_value:<10.4f} {result}")
    
    except Exception as e:
        print(f"  [ERRO] Erro no teste: {str(e)}")
    
    return result_1, result_2

def var_estimation():
    """Estima modelo VAR e cria impulso-resposta simplificado"""
    print("\n[3/4] Estimacao de Modelo VAR...")
    
    monthly = pd.read_csv('data/processed/monthly_data.csv', 
                          index_col=0, parse_dates=True)
    
    data = monthly[['DELTA_STRESS_INDEX', 'DELTA_EXPOSURE_RATIO']].dropna()
    
    if len(data) < 30:
        print(f"  [ERRO] Dados insuficientes para VAR")
        return None
    
    try:
        model = VAR(data)
        lag_order = model.select_order(maxlags=6)
        optimal_lag = lag_order.aic
        
        print(f"  Lag otimo (AIC): {optimal_lag}")
        
        results = model.fit(optimal_lag)
        
        print(f"\n  [OK] Modelo VAR({optimal_lag}) estimado")
        
        print(f"\n  Gerando funcoes de impulso-resposta...")
        irf = results.irf(10)
        
        fig = plt.figure(figsize=(10, 6))
        
        plt.subplot(2, 2, 1)
        irf.plot(impulse='DELTA_EXPOSURE_RATIO',
                 response='DELTA_STRESS_INDEX')
        plt.title('Impulso: Exposure -> Resposta: Stress')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 2)
        irf.plot(impulse='DELTA_STRESS_INDEX',
                 response='DELTA_EXPOSURE_RATIO')
        plt.title('Impulso: Stress -> Resposta: Exposure')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 3)
        irf.plot(impulse='DELTA_EXPOSURE_RATIO',
                 response='DELTA_EXPOSURE_RATIO')
        plt.title('Impulso: Exposure -> Resposta: Exposure')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 4)
        irf.plot(impulse='DELTA_STRESS_INDEX',
                 response='DELTA_STRESS_INDEX')
        plt.title('Impulso: Stress -> Resposta: Stress')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('figures/impulse_response.png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        print(f"  [OK] Grafico salvo: figures/impulse_response.png")
        
        return results
        
    except Exception as e:
        print(f"  [ERRO] Erro na estimacao VAR: {str(e)}")
        print(f"  [INFO] Pulando geracao de graficos de impulso-resposta")
        return None

def interpret_results():
    """Interpreta os resultados"""
    print("\n[4/4] Interpretacao dos Resultados...")
    
    print("\n  " + "="*60)
    print("  RESUMO DA ANALISE LEAD-LAG")
    print("  " + "="*60)
    
    print("""
  INTERPRETACAO DOS RESULTADOS:
  
  1. Se Delta-Exposure -> Delta-Stress e significante (p<0.05):
     -> Mudancas em exposicao PRECEDEM mudancas em estresse
     -> Consistente com mecanismo de ANTECIPACAO (H1)
  
  2. Se Delta-Stress -> Delta-Exposure e significante (p<0.05):
     -> Estresse causa mudancas em exposicao
     -> Consistente com REACAO a eventos publicos
  
  3. Se ambos sao significantes:
     -> Existe FEEDBACK LOOP bidirecional
     -> Sistema e reflexivo e potencialmente amplificador
    """)

def generate_summary():
    """Gera resumo da analise"""
    print("\n" + "="*60)
    print("RESUMO DA ANALISE LEAD-LAG")
    print("="*60)
    
    outputs = {
        'figures/cross_correlation.png': 'Correlacao cruzada',
        'figures/impulse_response.png': 'Impulso-resposta VAR'
    }
    
    for file, description in outputs.items():
        if os.path.exists(file):
            print(f"[OK] {description:30s} -> {file}")
        else:
            print(f"[--] {description:30s} -> Nao gerado")
    
    print("\n[OK] Analise lead-lag concluida!")
    print("[OK] Proximo passo: python scripts/03_synchronization.py")
    print("="*60)

def main():
    """Funcao principal"""
    print("="*60)
    print("FRAMEWORK: PREPARACAO ASSIMETRICA")
    print("Script 02: Analise Lead-Lag e Causalidade de Granger")
    print("="*60)
    
    if not os.path.exists('data/processed/monthly_data.csv'):
        print("\n[ERRO] Dados processados nao encontrados!")
        print("[ERRO] Execute primeiro: python scripts/01_process_data.py")
        return
    
    os.makedirs('figures', exist_ok=True)
    plt.close('all')
    
    cross_correlation_analysis()
    granger_causality_test()
    var_estimation()
    interpret_results()
    
    plt.close('all')
    generate_summary()

if __name__ == "__main__":
    main()
