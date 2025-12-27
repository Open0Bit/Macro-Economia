"""
Script: 03_synchronization.py
Descrição: Analisa se ativos diferentes se sincronizam (contágio) durante períodos de estresse.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração de Estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("talk")

def load_data():
    print("[1/3] Carregando dados...")
    return pd.read_csv('data/processed/master_dataset.csv', index_col=0, parse_dates=True)

def plot_rolling_correlation(df, asset1_col, asset2_col, window=60):
    """
    Plota a correlação móvel entre dois ativos junto com o Índice de Estresse.
    Se a correlação sobe junto com o estresse, indica contágio.
    """
    print(f"[2/3] Analisando Sincronização: {asset1_col} vs {asset2_col}...")
    
    # Calcular retornos se forem preços, ou usar níveis se forem índices
    # Aqui assumimos que as colunas de Flow_Index e Stress já são estacionárias/indicadores
    
    # Correlação Móvel (Rolling Correlation)
    rolling_corr = df[asset1_col].rolling(window=window).corr(df[asset2_col])
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot da Correlação (Eixo Esquerdo)
    color = 'tab:blue'
    ax1.set_xlabel('Data')
    ax1.set_ylabel(f'Correlação ({window} dias)', color=color)
    ax1.plot(rolling_corr.index, rolling_corr, color=color, label='Correlação')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(-1, 1)
    
    # Plot do Índice de Estresse (Eixo Direito - Sombra)
    ax2 = ax1.twinx()  
    color_stress = 'tab:red'
    ax2.set_ylabel('Índice de Estresse China', color=color_stress)
    ax2.fill_between(df.index, df['China_Stress_Index'], color=color_stress, alpha=0.1, label='Estresse')
    ax2.tick_params(axis='y', labelcolor=color_stress)
    
    plt.title(f'Sincronização de Mercado\nCorrelação entre {asset1_col} e {asset2_col}')
    
    # Salvar
    clean_name1 = asset1_col.replace('_Flow_Index', '').replace('_Price', '')
    clean_name2 = asset2_col.replace('_Flow_Index', '').replace('_Price', '')
    output_path = f'figures/sync_{clean_name1}_vs_{clean_name2}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"  ✓ Gráfico salvo em {output_path}")
    plt.close()

def analyze_regime_change(df):
    """
    Verifica se a correlação muda drasticamente entre regimes de 'Calma' vs 'Estresse'.
    """
    print("\n[3/3] Teste de Regime (Calma vs Estresse)...")
    
    # Definir limiar de estresse (Top 25% dos valores históricos)
    threshold = df['China_Stress_Index'].quantile(0.75)
    
    high_stress = df[df['China_Stress_Index'] > threshold]
    low_stress = df[df['China_Stress_Index'] <= threshold]
    
    results = []
    
    # Pares para analisar
    pairs = [
        ('China_Large_Flow_Index', 'China_Tech_Flow_Index'), # Contágio interno
        ('China_Large_Flow_Index', 'India_Flow_Index'),      # Contágio regional
        ('China_Large_Flow_Index', 'Gold_Flow_Index')        # Fuga para segurança
    ]
    
    for asset1, asset2 in pairs:
        if asset1 in df.columns and asset2 in df.columns:
            corr_calm = low_stress[asset1].corr(low_stress[asset2])
            corr_stress = high_stress[asset1].corr(high_stress[asset2])
            
            diff = corr_stress - corr_calm
            
            interpretation = "Estável"
            if diff > 0.2: interpretation = "Convergem (Contágio?)"
            if diff < -0.2: interpretation = "Divergem (Desacoplamento)"
            
            results.append({
                'Par': f"{asset1.split('_')[1]} vs {asset2.split('_')[0]}",
                'Corr (Calma)': f"{corr_calm:.2f}",
                'Corr (Estresse)': f"{corr_stress:.2f}",
                'Diferença': f"{diff:.2f}",
                'Status': interpretation
            })
    
    # Exibir tabela
    print("\n" + "="*65)
    print(f"{'PAR DE ATIVOS':<30} | {'CALMA':<8} | {'ESTRESSE':<8} | {'STATUS'}")
    print("-" * 65)
    for res in results:
        print(f"{res['Par']:<30} | {res['Corr (Calma)']:<8} | {res['Corr (Estresse)']:<8} | {res['Status']}")
    print("="*65 + "\n")

if __name__ == "__main__":
    os.makedirs('figures', exist_ok=True)
    
    df = load_data()
    
    # 1. Tech vs Large Caps (Eles caem juntos quando o estresse sobe?)
    if 'China_Tech_Flow_Index' in df.columns and 'China_Large_Flow_Index' in df.columns:
        plot_rolling_correlation(df, 'China_Tech_Flow_Index', 'China_Large_Flow_Index')
        
    # 2. China vs Índia (Investidores saem da China e vão pra Índia?)
    if 'China_Large_Flow_Index' in df.columns and 'India_Flow_Index' in df.columns:
        plot_rolling_correlation(df, 'China_Large_Flow_Index', 'India_Flow_Index')
        
    # 3. Análise de Regime
    analyze_regime_change(df)
    
    print("ANÁLISE COMPLETA ENCERRADA!")
    print("Verifique a pasta 'figures/' para ver todos os gráficos gerados.")