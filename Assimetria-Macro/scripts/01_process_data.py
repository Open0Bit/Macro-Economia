
import pandas as pd
import numpy as np

def process():
    print("  > Processando dados (Cálculo de Retornos)...")
    df = pd.read_csv("data/raw/market_data.csv", index_col=0, parse_dates=True)
    # Calculate Log Returns
    returns = np.log(df / df.shift(1)).dropna()
    output_path = "data/processed/returns.csv"
    returns.to_csv(output_path)
    print(f"  > Dados processados salvos em {output_path}")

if __name__ == "__main__":
    process()
