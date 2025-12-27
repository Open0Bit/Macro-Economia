"""
Script: 01_process_data.py
Descrição: Processa dados brutos, calcula indicadores compostos e cria o dataset mestre.
"""

import pandas as pd
import numpy as np
import os

def load_and_clean_fred():
    """Carrega e processa dados do FRED (Macro/Estresse)"""
    print("[1/4] Processando dados macro (FRED)...")
    
    # Carregar
    df = pd.read_csv('data/raw/fred_data.csv', index_col='date', parse_dates=True)
    
    # Preencher dados faltantes (forward fill para dados diários)
    df = df.ffill().dropna()
    
    # 1. Calcular Volatilidade do Câmbio (Janela de 21 dias ~ 1 mês útil)
    if 'USD_CNY' in df.columns:
        df['CNY_Vol_30d'] = df['USD_CNY'].pct_change().rolling(window=21).std() * np.sqrt(252)
    
    # 2. Normalização (Z-Score)
    indicators = {
        'VIX': 'z_VIX',
        'TED_Spread': 'z_TED',
        'Yield_Curve_10Y2Y': 'z_Yield', 
        'CNY_Vol_30d': 'z_CNY_Vol'
    }
    
    z_scores = pd.DataFrame(index=df.index)
    
    for col, z_col_name in indicators.items():
        if col in df.columns:
            mu = df[col].mean()
            sigma = df[col].std()
            z_scores[z_col_name] = (df[col] - mu) / sigma
    
    if 'z_Yield' in z_scores.columns:
        z_scores['z_Yield'] = -z_scores['z_Yield']

    # 3. Criar Índice de Estresse China
    df['China_Stress_Index'] = z_scores.mean(axis=1)
    df['China_Stress_Index'] = df['China_Stress_Index'].rolling(window=5).mean()
    
    df[['China_Stress_Index']].to_csv('data/processed/china_stress_index.csv')
    print("  ✓ Índice de Estresse calculado e salvo")
    
    return df

def load_and_process_etfs():
    """Carrega dados de ETFs e calcula proxy de fluxo (VERSÃO ROBUSTA)"""
    print("[2/4] Processando fluxos de ETFs...")
    
    # Tenta carregar detectando headers múltiplos
    try:
        # Formato comum: Header 0=Atributo (Close, Volume), Header 1=Ticker
        df = pd.read_csv('data/raw/etf_data.csv', header=[0, 1], index_col=0, parse_dates=True)
    except:
        # Fallback para 3 headers se o índice tiver nome
        df = pd.read_csv('data/raw/etf_data.csv', header=[0, 1, 2], index_col=0, parse_dates=True)
    
    # Função auxiliar para extrair dados limpos
    def safe_extract(df, key_part):
        # Tenta encontrar a coluna 'Close' ou 'Adj Close' ou 'Volume'
        # Varrer nível 0 das colunas
        for col in df.columns.levels[0]:
            if key_part.lower() in str(col).lower():
                data = df.xs(col, axis=1, level=0, drop_level=True)
                # Remover duplicatas de colunas (caso existam)
                return data.loc[:, ~data.columns.duplicated()]
        return pd.DataFrame()

    prices = safe_extract(df, 'Close') # Pega 'Adj Close' ou 'Close'
    volumes = safe_extract(df, 'Volume')
    
    if prices.empty or volumes.empty:
        print("  ! AVISO: Não foi possível estruturar preços/volumes corretamente.")
        print("  Verifique o arquivo data/raw/etf_data.csv")
        return pd.DataFrame()

    # Alinhar colunas
    common_cols = prices.columns.intersection(volumes.columns)
    prices = prices[common_cols]
    volumes = volumes[common_cols]

    # Calcular Fluxo (Preço * Volume)
    money_flow = prices * volumes
    
    processed_flows = pd.DataFrame(index=money_flow.index)
    
    targets = {
        'China_Tech': 'KWEB',
        'China_Large': 'FXI',
        'Gold': 'GLD',
        'India': 'INDA'
    }
    
    for name, ticker in targets.items():
        if ticker in money_flow.columns:
            # Extrair Série com segurança (evita erro de DataFrame vs Series)
            raw_data = money_flow[ticker]
            if isinstance(raw_data, pd.DataFrame):
                raw_data = raw_data.iloc[:, 0] # Pega primeira coluna se for duplicado
                
            price_data = prices[ticker]
            if isinstance(price_data, pd.DataFrame):
                price_data = price_data.iloc[:, 0]

            # Média móvel
            raw_flow = raw_data.rolling(window=21).mean()
            
            # Normalização (0 a 1)
            min_val = raw_flow.min()
            max_val = raw_flow.max()
            
            # Evitar divisão por zero
            if max_val > min_val:
                val = (raw_flow - min_val) / (max_val - min_val)
            else:
                val = 0.0
                
            processed_flows[f'{name}_Flow_Index'] = val
            processed_flows[f'{name}_Price'] = price_data
            
    processed_flows.dropna(inplace=True)
    processed_flows.to_csv('data/processed/institutional_flows.csv')
    print("  ✓ Dados de Fluxo processados e salvos")
    
    return processed_flows

def process_wb_data():
    """Processa dados anuais do Banco Mundial"""
    print("[3/4] Processando dados do Banco Mundial...")
    
    try:
        df = pd.read_csv('data/raw/wb_data.csv')
        if df.empty: return pd.DataFrame()
        
        china_wb = df[df['country'] == 'CHN'].pivot(index='year', columns='indicator', values='value')
        china_wb.index = pd.to_datetime(china_wb.index, format='%Y')
        china_wb_monthly = china_wb.resample('ME').ffill()
        
        china_wb_monthly.to_csv('data/processed/wb_macro.csv')
        print("  ✓ Dados Banco Mundial processados")
        return china_wb_monthly
    except Exception as e:
        print(f"  ! Aviso WB (não crítico): {e}")
        return pd.DataFrame()

def create_master_dataset(fred_df, flows_df, wb_df):
    """Combina tudo num único dataset"""
    print("[4/4] Criando Master Dataset...")
    
    if flows_df.empty:
        print("  ! Erro crítico: Sem dados de fluxo. Abortando master dataset.")
        return

    # Juntar FRED e Fluxos
    master = pd.merge(fred_df, flows_df, left_index=True, right_index=True, how='inner')
    
    # Juntar WB
    if not wb_df.empty:
        wb_reindexed = wb_df.reindex(master.index, method='ffill')
        master = pd.merge(master, wb_reindexed, left_index=True, right_index=True, how='left')
    
    master = master.dropna()
    output_path = 'data/processed/master_dataset.csv'
    master.to_csv(output_path)
    
    print("="*50)
    print(f"DATASET MESTRE CRIADO: {output_path}")
    print(f"Linhas: {len(master)}")
    print("="*50)

if __name__ == "__main__":
    os.makedirs('data/processed', exist_ok=True)
    
    fred_data = load_and_clean_fred()
    flows_data = load_and_process_etfs()
    wb_data = process_wb_data()
    
    create_master_dataset(fred_data, flows_data, wb_data)
    
    print("\nSUCESSO! Próximo passo: python scripts/02_leadlag_analysis.py")