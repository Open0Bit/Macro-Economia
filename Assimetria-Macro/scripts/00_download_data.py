
import yfinance as yf
import pandas as pd
import os

def download():
    print("  > Baixando dados de mercado (SPY, TLT)...")
    tickers = ['SPY', 'TLT']
    
    # CORREÇÃO AQUI: Adicionado auto_adjust=False para garantir que a coluna 'Adj Close' exista
    data = yf.download(tickers, start="2020-01-01", auto_adjust=False)['Adj Close']
    
    output_path = "data/raw/market_data.csv"
    data.to_csv(output_path)
    print(f"  > Dados salvos em {output_path}")

if __name__ == "__main__":
    download()
