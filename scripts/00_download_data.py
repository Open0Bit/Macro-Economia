"""
Script: 00_download_data.py
Descrição: Baixa dados históricos de APIs públicas (FRED, Yahoo Finance, World Bank).
"""

import os
import pandas as pd
import yfinance as yf
from fredapi import Fred
import requests
import time
from datetime import datetime

# ==========================================
# CONFIGURAÇÃO
# ==========================================
# Sua chave API fornecida
FRED_API_KEY = '6a8a8112991258a38fa4b6b0daa1d310'

START_DATE = '2015-01-01'
END_DATE = datetime.now().strftime('%Y-%m-%d')

# Mapeamento de Séries do FRED
FRED_SERIES = {
    'STLFSI4': 'Financial_Stress_Index',
    'VIXCLS': 'VIX',
    'TEDRATE': 'TED_Spread',
    'T10Y2Y': 'Yield_Curve_10Y2Y',
    'DEXCHUS': 'USD_CNY',
    'DCOILWTICO': 'Oil_WTI',
    'GOLDAMGBD228NLBM': 'Gold_Price',
    'DGS10': 'Treasury_10Y'
}

# ETFs para Yahoo Finance
ETF_TICKERS = [
    'MCHI', 'FXI', 'KWEB', # China
    'INDA', 'VNM', 'EWW',  # Pares
    'GLD', 'SHV', 'DBA'    # Defensivos/Commodities
]

# Indicadores Banco Mundial
WB_INDICATORS = {
    'NY.GDP.MKTP.CD': 'GDP_USD',
    'FP.CPI.TOTL.ZG': 'Inflation_Pct',
    'BX.KLT.DINV.WD.GD.ZS': 'FDI_Pct_GDP'
}
WB_COUNTRIES = ['CHN', 'USA', 'IND']

def setup_directories():
    """Garante que diretórios existem"""
    os.makedirs('data/raw', exist_ok=True)
    print("✓ Diretórios verificados")

def download_fred_data():
    """Baixa dados do Federal Reserve"""
    print("\n[1/3] Baixando dados do FRED...")
    try:
        fred = Fred(api_key=FRED_API_KEY)
        data_frames = []
        
        for series_id, name in FRED_SERIES.items():
            print(f"  - Baixando {name} ({series_id})...")
            try:
                # Baixar série
                series = fred.get_series(series_id, observation_start=START_DATE)
                # Converter para DataFrame
                df = series.to_frame(name=name)
                data_frames.append(df)
                time.sleep(0.5) # Evitar rate limit
            except Exception as e:
                print(f"    ! Erro em {name}: {e}")
        
        if data_frames:
            # Combinar todos os dados pelo índice (data)
            fred_df = pd.concat(data_frames, axis=1)
            fred_df.index.name = 'date'
            
            # Salvar
            output_path = 'data/raw/fred_data.csv'
            fred_df.to_csv(output_path)
            print(f"  ✓ Dados FRED salvos em {output_path}")
        else:
            print("  ✗ Nenhum dado do FRED foi baixado.")
            
    except Exception as e:
        print(f"  ✗ Falha crítica no módulo FRED: {e}")
        print("    Verifique se a chave API está correta e ativa.")

def download_etf_data():
    """Baixa dados do Yahoo Finance"""
    print("\n[2/3] Baixando dados de ETFs (Yahoo Finance)...")
    try:
        # Baixar dados em lote
        tickers_str = " ".join(ETF_TICKERS)
        print(f"  - Baixando: {tickers_str}")
        
        # Download
        df = yf.download(ETF_TICKERS, start=START_DATE, end=END_DATE, progress=False)
        
        # Achatar MultiIndex nas colunas se necessário e salvar
        # O yfinance retorna (Price, Ticker). Vamos salvar bruto e processar depois.
        output_path = 'data/raw/etf_data.csv'
        df.to_csv(output_path)
        print(f"  ✓ Dados ETFs salvos em {output_path}")
        
    except Exception as e:
        print(f"  ✗ Erro ao baixar ETFs: {e}")

def download_wb_data():
    """Baixa dados do Banco Mundial via API REST"""
    print("\n[3/3] Baixando dados do Banco Mundial...")
    
    all_data = []
    
    for country in WB_COUNTRIES:
        for indicator, name in WB_INDICATORS.items():
            url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=1000&date=2010:2024"
            try:
                response = requests.get(url)
                data = response.json()
                
                if len(data) > 1 and isinstance(data[1], list):
                    for entry in data[1]:
                        if entry['value'] is not None:
                            all_data.append({
                                'country': country,
                                'indicator': name,
                                'year': entry['date'],
                                'value': entry['value']
                            })
                print(f"  - {country} - {name}: OK")
            except Exception as e:
                print(f"  ! Erro {country}/{name}: {e}")
    
    if all_data:
        df = pd.DataFrame(all_data)
        output_path = 'data/raw/wb_data.csv'
        df.to_csv(output_path, index=False)
        print(f"  ✓ Dados Banco Mundial salvos em {output_path}")

if __name__ == "__main__":
    print("=== INICIANDO DOWNLOAD DE DADOS ===")
    setup_directories()
    download_fred_data()
    download_etf_data()
    download_wb_data()
    print("\n=== DOWNLOAD CONCLUÍDO ===")
    print("Agora execute: python scripts/01_process_data.py")