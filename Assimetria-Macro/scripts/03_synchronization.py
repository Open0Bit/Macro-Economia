
import pandas as pd
import matplotlib.pyplot as plt

def visualize():
    print("  > Gerando gráficos...")
    df = pd.read_csv("data/processed/returns.csv", index_col=0, parse_dates=True)
    
    plt.figure(figsize=(10, 6))
    (1 + df).cumprod().plot()
    plt.title("Retorno Acumulado")
    plt.savefig("figures/cumulative_returns.png")
    print("  > Gráfico salvo em figures/cumulative_returns.png")

if __name__ == "__main__":
    visualize()
