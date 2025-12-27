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
    """Automação completa: Setup + Pipeline de Dados"""
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.errors = []
        
    def print_header(self, text):
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70 + "\n")
    
    def print_step(self, step_num, text):
        print(f"[{step_num}/6] {text}...")
    
    def create_directory_structure(self):
        self.print_step(1, "Criando estrutura de diretórios")
        directories = ['data/raw', 'data/processed', 'scripts', 'figures', 'output', 'docs']
        for directory in directories:
            (self.base_dir / directory).mkdir(parents=True, exist_ok=True)
            
    def create_requirements(self):
        self.print_step(2, "Gerando requirements.txt")
        reqs = """pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
statsmodels>=0.14.0
fredapi>=0.5.0
yfinance>=0.2.0
requests>=2.31.0
openpyxl>=3.1.0
"""
        (self.base_dir / 'requirements.txt').write_text(reqs)

    def create_license(self):
        self.print_step(3, "Assinando LICENSE (MIT)")
        license_text = """MIT License

Copyright (c) 2024 Gabriel W. Soares

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""
        (self.base_dir / 'LICENSE').write_text(license_text)

    def install_dependencies(self):
        self.print_step(4, "Instalando dependências")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        except:
            print("  ! Aviso: Instalação automática falhou. Execute 'pip install -r requirements.txt' manualmente.")

    def create_orchestrator(self):
        """Cria um script para rodar tudo de uma vez"""
        self.print_step(5, "Gerando orquestrador de pipeline")
        
        run_all_content = '''"""
Script Orquestrador: Executa todo o pipeline de uma vez.
"""
import subprocess
import sys
import time
import os

def run_step(script_name):
    print(f"\\n>>> EXECUTANDO: {script_name}...")
    t0 = time.time()
    # Verifica se o arquivo existe
    if not os.path.exists(f'scripts/{script_name}'):
        print(f"X Erro: Arquivo scripts/{script_name} não encontrado.")
        return False
        
    result = subprocess.run([sys.executable, f'scripts/{script_name}'])
    dt = time.time() - t0
    
    if result.returncode == 0:
        print(f"✓ {script_name} concluído em {dt:.1f}s")
        return True
    else:
        print(f"X Erro em {script_name}")
        return False

if __name__ == "__main__":
    print("=== INICIANDO PIPELINE MACRO ===")
    
    steps = [
        '00_download_data.py',
        '01_process_data.py',
        '02_leadlag_analysis.py',
        '03_synchronization.py'
    ]
    
    for step in steps:
        if not run_step(step):
            print("Pipeline interrompido por erro.")
            break
            
    print("\\n=== PIPELINE FINALIZADO ===")
'''
        (self.base_dir / 'run_pipeline.py').write_text(run_all_content, encoding='utf-8')
        print("  ✓ run_pipeline.py criado na raiz")

    def run_pipeline_trigger(self):
        """O Gatilho Automático"""
        self.print_step(6, "Finalização")
        print("\n" + "="*50)
        print("SETUP CONCLUÍDO COM SUCESSO!")
        print("Autor: Gabriel W. Soares")
        print("="*50)
        
        # O GATILHO
        print("\n[OPCIONAL] Deseja executar toda a análise agora?")
        print("Isso irá baixar dados, processar e gerar os gráficos.")
        print("Nota: Certifique-se de ter configurado a API KEY no script 00.")
        choice = input("Digite 'S' para Sim ou ENTER para Sair: ").strip().upper()
        
        if choice == 'S':
            print("\nIniciando Piloto Automático...\n")
            try:
                subprocess.run([sys.executable, 'run_pipeline.py'])
            except Exception as e:
                print(f"Erro ao executar pipeline: {e}")
        else:
            print("\nOk. Para rodar depois, use: python run_pipeline.py")

    def run(self):
        self.print_header("FRAMEWORK MACRO - SETUP")
        self.create_directory_structure()
        self.create_requirements()
        self.create_license()
        self.install_dependencies()
        self.create_orchestrator()
        self.run_pipeline_trigger()

if __name__ == "__main__":
    setup = ProjectSetup()
    setup.run()