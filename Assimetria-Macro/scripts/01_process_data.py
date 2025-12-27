
# =============================================================================
# 01_process_data.py - VERSÃO WINDOWS-SAFE
# =============================================================================

"""
Script 01: Processamento de Dados
Framework: Preparacao Assimetrica e Crises Sistemicas
Autor: Gabriel W. Soares
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

def calculate_returns():
    """Calcula retornos logaritmicos"""
    print("\n[1/5] Calculando retornos logaritmicos...")
    
    prices = pd.read_csv('data/raw/etf_prices.csv', index_col=0, parse_dates=True)
    returns = np.log(prices / prices.shift(1))
    returns = returns.dropna()
    
    output_path = 'data/processed/etf_returns.csv'
    returns.to_csv(output_path)
    
    print(f"  [OK] Retornos calculados: {len(returns)} observacoes")
    print(f"  [OK] ETFs processados: {', '.join(returns.columns)}")
    print(f"  [OK] Salvo em {output_path}")
    
    return returns

def construct_stress_index():
    """Constroi Indice de Estresse Sistemico"""
    print("\n[2/5] Construindo Indice de Estresse Sistemico...")
    
    components = {}
    
    if os.path.exists('data/raw/macro_indicators.csv'):
        macro = pd.read_csv('data/raw/macro_indicators.csv', index_col=0, parse_dates=True)
        
        for col in macro.columns:
            if not macro[col].isna().all():
                z_score = (macro[col] - macro[col].mean()) / macro[col].std()
                components[f'Z_{col}'] = z_score
                print(f"  -> Adicionado: {col}")
    
    if os.path.exists('data/raw/volatility_proxy.csv'):
        vol = pd.read_csv('data/raw/volatility_proxy.csv', index_col=0, parse_dates=True)
        
        if 'VOL_RATIO' in vol.columns:
            z_vol = (vol['VOL_RATIO'] - vol['VOL_RATIO'].mean()) / vol['VOL_RATIO'].std()
            components['Z_VOL_RATIO'] = z_vol
            print(f"  -> Adicionado: VOL_RATIO (proxy)")
    
    prices = pd.read_csv('data/raw/etf_prices.csv', index_col=0, parse_dates=True)
    if 'FXI' in prices.columns:
        returns_fxi = prices['FXI'].pct_change()
        vol_fxi_30d = returns_fxi.rolling(30).std() * (252 ** 0.5)
        z_vol_fxi = (vol_fxi_30d - vol_fxi_30d.mean()) / vol_fxi_30d.std()
        components['Z_VOL_FXI_30D'] = z_vol_fxi
        print(f"  -> Adicionado: VOL_FXI_30D")
    
    if components:
        df_components = pd.DataFrame(components)
        stress_index = df_components.mean(axis=1, skipna=True)
        
        df_stress = pd.DataFrame({
            'STRESS_INDEX': stress_index,
            **components
        })
        
        output_path = 'data/processed/stress_index.csv'
        df_stress.to_csv(output_path)
        
        print(f"\n  [OK] Indice construido com {len(components)} componentes")
        print(f"  [OK] Periodo: {df_stress.index[0]} ate {df_stress.index[-1]}")
        print(f"  [OK] Salvo em {output_path}")
        
        print(f"\n  Estatisticas do Indice:")
        print(f"    Media: {stress_index.mean():.3f}")
        print(f"    Desvio: {stress_index.std():.3f}")
        print(f"    Maximo: {stress_index.max():.3f}")
        print(f"    Minimo: {stress_index.min():.3f}")
        
        return df_stress
    else:
        print("  [ERRO] Nenhum componente disponivel")
        return None

def calculate_exposure_proxy():
    """Calcula proxy de exposicao institucional"""
    print("\n[3/5] Calculando proxy de exposicao institucional...")
    
    prices = pd.read_csv('data/raw/etf_prices.csv', index_col=0, parse_dates=True)
    
    if 'FXI' in prices.columns and 'SPY' in prices.columns:
        exposure_ratio = prices['FXI'] / prices['SPY']
        exposure_ratio = (exposure_ratio / exposure_ratio.iloc[0]) * 100
        
        df_exposure = pd.DataFrame({
            'EXPOSURE_RATIO': exposure_ratio,
        })
        
        output_path = 'data/processed/exposure_proxy.csv'
        df_exposure.to_csv(output_path)
        
        print(f"  [OK] Proxy calculado: FXI/SPY ratio")
        print(f"  [OK] Variacao: {exposure_ratio.iloc[-1] - exposure_ratio.iloc[0]:.2f} pontos")
        print(f"  [OK] Salvo em {output_path}")
        
        return df_exposure
    else:
        print("  [ERRO] ETFs necessarios nao disponiveis")
        return None

def calculate_defensive_concentration():
    """Calcula concentracao em ativos defensivos"""
    print("\n[4/5] Calculando concentracao defensiva (GLD/FXI)...")
    
    prices = pd.read_csv('data/raw/etf_prices.csv', index_col=0, parse_dates=True)
    
    if 'GLD' in prices.columns and 'FXI' in prices.columns:
        defensive_ratio = prices['GLD'] / prices['FXI']
        defensive_ratio = (defensive_ratio / defensive_ratio.iloc[0]) * 100
        defensive_change_6m = defensive_ratio.diff(126)
        
        df_defensive = pd.DataFrame({
            'DEFENSIVE_RATIO': defensive_ratio,
            'DEFENSIVE_CHANGE_6M': defensive_change_6m
        })
        
        output_path = 'data/processed/defensive_concentration.csv'
        df_defensive.to_csv(output_path)
        
        print(f"  [OK] Ratio GLD/FXI calculado")
        print(f"  [OK] Variacao: {defensive_ratio.iloc[-1] - defensive_ratio.iloc[0]:.2f} pontos")
        print(f"  [OK] Salvo em {output_path}")
        
        return df_defensive
    else:
        print("  [ERRO] ETFs necessarios nao disponiveis")
        return None

def prepare_monthly_data():
    """Agrega dados para frequencia mensal"""
    print("\n[5/5] Preparando dados mensais para analise VAR...")
    
    files_to_aggregate = {
        'data/processed/stress_index.csv': 'STRESS_INDEX',
        'data/processed/exposure_proxy.csv': 'EXPOSURE_RATIO',
        'data/processed/defensive_concentration.csv': 'DEFENSIVE_RATIO'
    }
    
    monthly_data = {}
    
    for file, col_name in files_to_aggregate.items():
        if os.path.exists(file):
            df = pd.read_csv(file, index_col=0, parse_dates=True)
            if col_name in df.columns:
                monthly = df[col_name].resample('ME').last()
                monthly_data[col_name] = monthly
    
    if monthly_data:
        df_monthly = pd.DataFrame(monthly_data)
        
        for col in df_monthly.columns:
            df_monthly[f'DELTA_{col}'] = df_monthly[col].diff()
        
        output_path = 'data/processed/monthly_data.csv'
        df_monthly.to_csv(output_path)
        
        print(f"  [OK] Dados mensais agregados: {len(df_monthly)} meses")
        print(f"  [OK] Variaveis: {len(df_monthly.columns)} colunas")
        print(f"  [OK] Salvo em {output_path}")
        
        return df_monthly
    else:
        print("  [ERRO] Nenhum dado disponivel")
        return None

def generate_summary():
    """Gera resumo do processamento"""
    print("\n" + "="*60)
    print("RESUMO DO PROCESSAMENTO")
    print("="*60)
    
    processed_files = {
        'data/processed/etf_returns.csv': 'Retornos logaritmicos',
        'data/processed/stress_index.csv': 'Indice de Estresse',
        'data/processed/exposure_proxy.csv': 'Proxy de Exposicao',
        'data/processed/defensive_concentration.csv': 'Concentracao Defensiva',
        'data/processed/monthly_data.csv': 'Dados Mensais (VAR)'
    }
    
    for file, description in processed_files.items():
        if os.path.exists(file):
            df = pd.read_csv(file, index_col=0)
            print(f"[OK] {description:30s} -> {len(df):5d} obs")
        else:
            print(f"[--] {description:30s} -> Nao gerado")
    
    print("\n[OK] Processamento concluido!")
    print("[OK] Proximo passo: python scripts/02_leadlag_analysis.py")
    print("="*60)

def main():
    """Funcao principal"""
    print("="*60)
    print("FRAMEWORK: PREPARACAO ASSIMETRICA")
    print("Script 01: Processamento de Dados")
    print("="*60)
    
    if not os.path.exists('data/raw/etf_prices.csv'):
        print("\n[ERRO] Dados brutos nao encontrados!")
        print("[ERRO] Execute primeiro: python scripts/00_download_data.py")
        return
    
    returns = calculate_returns()
    stress = construct_stress_index()
    exposure = calculate_exposure_proxy()
    defensive = calculate_defensive_concentration()
    monthly = prepare_monthly_data()
    
    generate_summary()

if __name__ == "__main__":
    main()