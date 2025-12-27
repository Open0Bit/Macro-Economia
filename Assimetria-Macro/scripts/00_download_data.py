# =============================================================================
# 00_download_data.py - VERSÃO WINDOWS-SAFE
# =============================================================================

"""
Script 00: Download de Dados Publicos
Framework: Preparacao Assimetrica e Crises Sistemicas
Autor: Gabriel W. Soares
"""

import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import time

def create_directories():
    """Cria estrutura de pastas necessaria"""
    directories = [
        'data/raw',
        'data/processed',
        'figures',
        'output'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("[OK] Estrutura de pastas criada")

def download_etf_data():
    """Download de dados de ETFs publicos"""
    print("\n[1/3] Baixando dados de ETFs...")
    
    etfs = {
        'FXI': 'iShares China Large-Cap ETF',
        'MCHI': 'iShares MSCI China ETF',
        'KWEB': 'KraneShares China Internet ETF',
        'GLD': 'SPDR Gold Trust',
        'SPY': 'SPDR S&P 500 ETF',
        'TLT': 'iShares 20+ Year Treasury'
    }
    
    start_date = "2015-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    tickers_list = list(etfs.keys())
    tickers_str = ' '.join(tickers_list)
    
    print(f"  -> Baixando {len(tickers_list)} ETFs...")
    
    try:
        data = yf.download(tickers_str, start=start_date, end=end_date, 
                          progress=False, auto_adjust=True, group_by='ticker')
        
        df_etfs = pd.DataFrame()
        
        for ticker in tickers_list:
            try:
                if len(tickers_list) > 1:
                    prices = data[ticker]['Close']
                else:
                    prices = data['Close']
                
                df_etfs[ticker] = prices
                print(f"    [OK] {ticker}: {len(prices.dropna())} observacoes")
            except Exception as e:
                print(f"    [ERRO] {ticker}: {str(e)}")
        
        if not df_etfs.empty:
            output_path = "data/raw/etf_prices.csv"
            df_etfs.to_csv(output_path)
            print(f"\n  [OK] Dados salvos em {output_path}")
            print(f"  [OK] Periodo: {df_etfs.index[0].date()} ate {df_etfs.index[-1].date()}")
            print(f"  [OK] {len(df_etfs)} dias de negociacao")
            return df_etfs
        else:
            print("\n  [ERRO] Nenhum dado foi baixado")
            return None
            
    except Exception as e:
        print(f"\n  [ERRO] Falha no download: {str(e)}")
        return None

def download_macro_indicators():
    """Download de indicadores macroeconomicos do FRED"""
    print("\n[2/3] Baixando indicadores macroeconomicos (FRED)...")
    
    try:
        from pandas_datareader import data as pdr
        
        indicators = {
            'VIXCLS': 'CBOE Volatility Index',
            'TEDRATE': 'TED Spread',
            'T10Y2Y': 'Treasury Yield Curve',
            'DEXCHUS': 'China/USD Exchange Rate'
        }
        
        start_date = "2015-01-01"
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        all_indicators = {}
        
        for code, name in indicators.items():
            try:
                print(f"  -> Baixando {code}...")
                series = pdr.DataReader(code, 'fred', start_date, end_date)
                all_indicators[code] = series.iloc[:, 0]
                print(f"    [OK] {len(series)} observacoes")
                time.sleep(0.5)
            except Exception as e:
                print(f"    [ERRO] {str(e)}")
        
        if all_indicators:
            df_macro = pd.DataFrame(all_indicators)
            output_path = "data/raw/macro_indicators.csv"
            df_macro.to_csv(output_path)
            print(f"\n  [OK] Indicadores salvos em {output_path}")
            return df_macro
        else:
            print("\n  [AVISO] Nenhum indicador baixado")
            return None
            
    except ImportError:
        print("\n  [AVISO] pandas-datareader nao instalado")
        print("  [INFO] Instale com: pip install pandas-datareader")
        print("  [INFO] Continuando sem indicadores FRED...")
        return None

def calculate_cny_volatility(etf_data):
    """Calcula volatilidade CNY/USD usando proxy de ETFs"""
    print("\n[3/3] Calculando volatilidade implicita...")
    
    if etf_data is None or 'FXI' not in etf_data.columns or 'SPY' not in etf_data.columns:
        print("  [ERRO] ETFs necessarios nao disponiveis")
        return None
    
    returns_fxi = etf_data['FXI'].pct_change()
    returns_spy = etf_data['SPY'].pct_change()
    
    vol_fxi = returns_fxi.rolling(30).std() * (252 ** 0.5)
    vol_spy = returns_spy.rolling(30).std() * (252 ** 0.5)
    
    vol_ratio = vol_fxi / vol_spy
    
    df_vol = pd.DataFrame({
        'VOL_FXI': vol_fxi,
        'VOL_SPY': vol_spy,
        'VOL_RATIO': vol_ratio
    })
    
    output_path = "data/raw/volatility_proxy.csv"
    df_vol.to_csv(output_path)
    print(f"  [OK] Volatilidade salva em {output_path}")
    return df_vol

def generate_summary():
    """Gera resumo dos dados coletados"""
    print("\n" + "="*60)
    print("RESUMO DA COLETA DE DADOS")
    print("="*60)
    
    files_status = {
        'data/raw/etf_prices.csv': 'Precos de ETFs',
        'data/raw/macro_indicators.csv': 'Indicadores FRED',
        'data/raw/volatility_proxy.csv': 'Volatilidade calculada'
    }
    
    for file, description in files_status.items():
        if os.path.exists(file):
            df = pd.read_csv(file, index_col=0)
            print(f"[OK] {description:30s} -> {len(df):5d} observacoes")
        else:
            print(f"[--] {description:30s} -> Nao disponivel")
    
    print("\n[OK] Coleta de dados concluida!")
    print("[OK] Proximo passo: python scripts/01_process_data.py")
    print("="*60)

def main():
    """Funcao principal"""
    print("="*60)
    print("FRAMEWORK: PREPARACAO ASSIMETRICA")
    print("Script 00: Download de Dados Publicos")
    print("="*60)
    
    create_directories()
    etf_data = download_etf_data()
    macro_data = download_macro_indicators()
    
    if etf_data is not None:
        vol_data = calculate_cny_volatility(etf_data)
    
    generate_summary()

if __name__ == "__main__":
    main()
