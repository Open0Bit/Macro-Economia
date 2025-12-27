# =====================================================
# setup.py - FRAMEWORK MACRO-ECONOMIA (CORRECTED)
# Autor: Gabriel W. Soares
# =====================================================

import os
import sys
import subprocess
from pathlib import Path
import time

class ProjectSetup:
    """Automação completa: Setup + Pipeline de Dados + Restauração"""
    
    def __init__(self):
        self.base_dir = Path.cwd()
        
    def print_step(self, step, text):
        print(f"[{step}/6] {text}...")

    def create_structure(self):
        self.print_step(1, "Criando pastas")
        for d in ['data/raw', 'data/processed', 'scripts', 'figures', 'output']:
            (self.base_dir / d).mkdir(parents=True, exist_ok=True)

    def create_files(self):
        self.print_step(2, "Gerando arquivos de configuração")
        
        # 1. Requirements
        reqs = "pandas>=2.0.0\nnumpy>=1.24.0\nmatplotlib>=3.7.0\nseaborn>=0.12.0\nscipy>=1.10.0\nstatsmodels>=0.14.0\nfredapi>=0.5.0\nyfinance>=0.2.0\nrequests>=2.31.0"
        (self.base_dir / 'requirements.txt').write_text(reqs, encoding='utf-8')
        
        # 2. License
        license_txt = "MIT License\n\nCopyright (c) 2024 Gabriel W. Soares"
        (self.base_dir / 'LICENSE').write_text(license_txt, encoding='utf-8')

    def create_analysis_scripts(self):
        """Creates the actual logic scripts so the pipeline has something to run."""
        self.print_step(3, "Gerando scripts de análise (Templates)")

        # Script 00: Download Data (Example using yfinance to avoid FRED API key requirement for demo)
        # Script 00: Download Data (CORRIGIDO)
        script_00 = '''
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
'''
        (self.base_dir / 'scripts/00_download_data.py').write_text(script_00, encoding='utf-8')

        # Script 01: Process Data
        script_01 = '''
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
'''
        (self.base_dir / 'scripts/01_process_data.py').write_text(script_01, encoding='utf-8')

        # Script 02: Lead/Lag Analysis (Placeholder)
        script_02 = '''
import pandas as pd

def analyze():
    print("  > Executando análise de Lead-Lag (Correlação)...")
    df = pd.read_csv("data/processed/returns.csv", index_col=0, parse_dates=True)
    corr = df.corr()
    print("  > Matriz de Correlação:")
    print(corr)
    # Here you would add complex Granger Causality logic
    
if __name__ == "__main__":
    analyze()
'''
        (self.base_dir / 'scripts/02_leadlag_analysis.py').write_text(script_02, encoding='utf-8')

        # Script 03: Synchronization (Plotting)
        script_03 = '''
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
'''
        (self.base_dir / 'scripts/03_synchronization.py').write_text(script_03, encoding='utf-8')

    def create_orchestrator(self):
        self.print_step(4, "Criando orquestrador (run_pipeline.py)")
        
        content = '''"""
Script Orquestrador: Executa todo o pipeline automaticamente.
"""
import subprocess
import sys
import os

def run():
    print("=== INICIANDO PIPELINE MACRO ===")
    scripts = ['00_download_data.py', '01_process_data.py', '02_leadlag_analysis.py', '03_synchronization.py']
    
    for script in scripts:
        path = f'scripts/{script}'
        if not os.path.exists(path):
            print(f"ERRO: {path} não encontrado. Execute setup.py novamente.")
            continue
            
        print(f"\\n>>> Rodando {script}...")
        # Uses the current python interpreter
        ret = subprocess.run([sys.executable, path])
        if ret.returncode != 0:
            print("Erro na execução. Parando.")
            break
            
    print("\\n=== CONCLUÍDO ===")

if __name__ == "__main__":
    run()
'''
        (self.base_dir / 'run_pipeline.py').write_text(content, encoding='utf-8')

    def install_libs(self):
        self.print_step(5, "Instalando bibliotecas")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        except:
            print("  ! Aviso: Instale manualmente com 'pip install -r requirements.txt'")

    def trigger(self):
        self.print_step(6, "Finalizando")
        print("\n" + "="*50)
        print("SETUP FINALIZADO COM SUCESSO!")
        print("Autor: Gabriel W. Soares")
        print("="*50)
        
        print("\nDeseja rodar a análise completa agora? (S/N)")
        if input(">> ").strip().upper() == 'S':
            subprocess.run([sys.executable, 'run_pipeline.py'])
        else:
            print("Ok. Para rodar depois: python run_pipeline.py")

    def run_setup(self):
        """Orchestrates the setup process."""
        self.create_structure()
        self.create_files()
        self.create_analysis_scripts() # Added this step
        self.create_orchestrator()
        self.install_libs()
        self.trigger()

if __name__ == "__main__":
    # Corrected main execution
    ProjectSetup().run_setup()