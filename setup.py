# =====================================================
# setup.py - FRAMEWORK MACRO-ECONOMIA
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
        print(f"[{step}/5] {text}...")

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
        license_txt = "MIT License\n\nCopyright (c) 2024 Gabriel W. Soares\n\nPermission is hereby granted, free of charge..."
        (self.base_dir / 'LICENSE').write_text(license_txt, encoding='utf-8')

    def create_orchestrator(self):
        self.print_step(3, "Criando orquestrador (run_pipeline.py)")
        
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
            print(f"ERRO: {path} não encontrado. Execute setup.py novamente ou baixe do Git.")
            continue
            
        print(f"\\n>>> Rodando {script}...")
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
        self.print_step(4, "Instalando bibliotecas")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        except:
            print("  ! Aviso: Instale manualmente com 'pip install -r requirements.txt'")

    def trigger(self):
        self.print_step(5, "Finalizando")
        print("\n" + "="*50)
        print("SETUP FINALIZADO COM SUCESSO!")
        print("Autor: Gabriel W. Soares")
        print("="*50)
        
        print("\nDeseja rodar a análise completa agora? (S/N)")
        if input(">> ").strip().upper() == 'S':
            subprocess.run([sys.executable, 'run_pipeline.py'])
        else:
            print("Ok. Para rodar depois: python run_pipeline.py")

if __name__ == "__main__":
    ProjectSetup().run()
    
    # Método para rodar sequencialmente
    setup = ProjectSetup()
    setup.create_structure()
    setup.create_files()
    setup.create_orchestrator()
    setup.install_libs()
    setup.trigger()