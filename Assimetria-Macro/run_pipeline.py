"""
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
            
        print(f"\n>>> Rodando {script}...")
        # Uses the current python interpreter
        ret = subprocess.run([sys.executable, path])
        if ret.returncode != 0:
            print("Erro na execução. Parando.")
            break
            
    print("\n=== CONCLUÍDO ===")

if __name__ == "__main__":
    run()
