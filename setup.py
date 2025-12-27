# =====================================================
# setup.py - SCRIPT DE AUTOMAÇÃO COMPLETA
# Execute este arquivo para criar toda a estrutura
# =====================================================

"""
USO:
    python setup.py

Este script:
1. Cria toda a estrutura de pastas
2. Cria arquivos vazios necessários
3. Instala dependências Python
4. Configura git (se ainda não configurado)
5. Gera requirements.txt
6. Cria .gitignore apropriado

Compatível com Windows, Linux e macOS
"""

import os
import sys
import subprocess
from pathlib import Path

class ProjectSetup:
    """Automação completa de setup do projeto"""
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.errors = []
        
    def print_header(self, text):
        """Imprime cabeçalho formatado"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70 + "\n")
    
    def print_step(self, step_num, text):
        """Imprime número e descrição do passo"""
        print(f"[{step_num}/8] {text}...")
    
    def create_directory_structure(self):
        """Cria toda a estrutura de diretórios"""
        self.print_step(1, "Criando estrutura de diretórios")
        
        directories = [
            'data/raw',
            'data/processed',
            'scripts',
            'notebooks',
            'figures',
            'output',
            'docs',
            'tests'
        ]
        
        for directory in directories:
            path = self.base_dir / directory
            path.mkdir(parents=True, exist_ok=True)
            print(f"  OK {directory}/")
        
        print("\n  Estrutura de pastas criada com sucesso!")
    
    def create_requirements_txt(self):
        """Cria arquivo requirements.txt"""
        self.print_step(2, "Criando requirements.txt")
        
        requirements = """# Analise de Dados
pandas>=2.0.0
numpy>=1.24.0

# Visualizacao
matplotlib>=3.7.0
seaborn>=0.12.0

# Estatistica
scipy>=1.10.0
statsmodels>=0.14.0

# APIs de Dados Publicos
fredapi>=0.5.0
yfinance>=0.2.0
requests>=2.31.0

# Notebook Interativo
jupyter>=1.0.0
ipykernel>=6.25.0

# Utilitarios
python-dateutil>=2.8.0
openpyxl>=3.1.0
"""
        
        req_path = self.base_dir / 'requirements.txt'
        req_path.write_text(requirements, encoding='utf-8')
        print(f"  OK requirements.txt criado")
    
    def create_gitignore(self):
        """Cria .gitignore apropriado"""
        self.print_step(3, "Criando .gitignore")
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb_checkpoints/

# Ambiente Virtual
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Dados sensiveis
**/config_local.py
**/*_secret.py

# Outputs temporarios
*.log
*.tmp
"""
        
        gitignore_path = self.base_dir / '.gitignore'
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        print(f"  OK .gitignore criado")
    
    def create_readme_data(self):
        """Cria README_data.md documentando fontes"""
        self.print_step(4, "Criando documentação de dados")
        
        # Texto simplificado para evitar erros de codificacao
        readme_data = """# Documentacao dos Dados

## Fontes de Dados

Todas as fontes utilizadas neste projeto sao publicas e gratuitas.

### 1. Federal Reserve Economic Data (FRED)

**URL:** https://fred.stlouisfed.org/  

**Series utilizadas:**
- `STLFSI4`: St. Louis Fed Financial Stress Index
- `VIXCLS`: CBOE Volatility Index (VIX)
- `TEDRATE`: TED Spread
- `T10Y2Y`: 10-Year Treasury Constant Maturity Minus 2-Year
- `DEXCHUS`: China / U.S. Foreign Exchange Rate

### 2. Yahoo Finance

**ETFs utilizados:**
- `MCHI`: iShares MSCI China ETF
- `FXI`: iShares China Large-Cap ETF
- `KWEB`: KraneShares CSI China Internet ETF
- `GLD`: SPDR Gold Trust

### 3. World Bank Open Data

**Indicadores:**
- GDP (current US$)
- Inflation
- FDI inflows

## Processamento de Dados

### Indice de Estresse China

**Normalizacao:**
Cada componente e convertido para z-score:

z = (x - media) / desvio_padrao

**Indice Final:**
Stress_Index = mean(z_VIX, z_CNY_Vol, z_TED, z_YieldCurve)

---
Atualizado: Dezembro 2024
"""
        
        readme_data_path = self.base_dir / 'data' / 'README_data.md'
        readme_data_path.write_text(readme_data, encoding='utf-8')
        print(f"  OK data/README_data.md criado")
    
    def install_dependencies(self):
        """Instala dependências Python"""
        self.print_step(5, "Instalando dependências Python")
        
        print("\n  Verificando se pip está atualizado...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                         check=True, capture_output=True)
            print("  OK pip atualizado")
        except subprocess.CalledProcessError:
            print(f"  AVISO: Não foi possível atualizar pip")
        
        print("\n  Instalando pacotes do requirements.txt...")
        
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                         check=True, capture_output=True)
            print("  OK Todas as dependências instaladas!")
        except subprocess.CalledProcessError:
            print(f"  ERRO ao instalar dependências")
            print(f"  Execute manualmente: pip install -r requirements.txt")
            self.errors.append("Instalação de dependências falhou")
    
    def create_license(self):
        """Cria arquivo LICENSE (MIT)"""
        self.print_step(6, "Criando LICENSE")
        
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

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        
        license_path = self.base_dir / 'LICENSE'
        license_path.write_text(license_text, encoding='utf-8')
        print(f"  OK LICENSE criado")
    
    def initialize_git(self):
        """Inicializa git se necessário"""
        self.print_step(7, "Verificando Git")
        
        git_dir = self.base_dir / '.git'
        
        if git_dir.exists():
            print("  OK Repositório Git já inicializado")
            return
        
        try:
            subprocess.run(['git', 'init'], check=True, capture_output=True)
            print("  OK Repositório Git inicializado")
            
        except FileNotFoundError:
            print("  AVISO: Git não encontrado no sistema")
            self.errors.append("Git não instalado")
        except subprocess.CalledProcessError:
            print("  AVISO: Erro ao inicializar Git")
            self.errors.append("Erro ao inicializar Git")
    
    def create_empty_scripts(self):
        """Cria arquivos de script vazios com comentários de template"""
        self.print_step(8, "Criando templates de scripts")
        
        scripts = {
            '00_download_data.py': '''"""
Script para download de dados.
"""
FRED_API_KEY = 'COLE_SUA_CHAVE_AQUI'
''',
            '01_process_data.py': '''"""
Script para processamento de dados.
"""
''',
            '02_leadlag_analysis.py': '''"""
Analise de lead-lag.
"""
''',
            '03_synchronization.py': '''"""
Analise de sincronizacao.
"""
'''
        }
        
        for filename, content in scripts.items():
            script_path = self.base_dir / 'scripts' / filename
            script_path.write_text(content, encoding='utf-8')
            print(f"  OK scripts/{filename}")
    
    def print_summary(self):
        """Imprime resumo final"""
        self.print_header("SETUP COMPLETO!")
        
        if not self.errors:
            print("OK Projeto configurado com sucesso!\n")
        else:
            print("AVISO Setup concluído com avisos:\n")
            for error in self.errors:
                print(f"  - {error}")
            print()
        
        print("Proximos passos:")
        print("  1. Cole os codigos completos nos scripts")
        print("  2. Obtenha sua chave API FRED")
        print("  3. Execute: python scripts/00_download_data.py")
        print("\n" + "=" * 70 + "\n")
    
    def run(self):
        """Executa setup completo"""
        self.print_header("SETUP AUTOMATICO")
        
        print("Pressione ENTER para continuar...")
        input()
        
        self.create_directory_structure()
        self.create_requirements_txt()
        self.create_gitignore()
        self.create_readme_data()
        self.install_dependencies()
        self.create_license()
        self.initialize_git()
        self.create_empty_scripts()
        self.print_summary()


# =====================================================
# SCRIPT BASH ALTERNATIVO (Linux/macOS)
# =====================================================

BASH_SCRIPT = '''#!/bin/bash
# setup.sh
mkdir -p data/raw data/processed scripts notebooks figures output docs tests
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
'''

# =====================================================
# SCRIPT BATCH ALTERNATIVO (Windows)
# =====================================================

BATCH_SCRIPT = '''@echo off
mkdir data\\raw 2>nul
mkdir data\\processed 2>nul
mkdir scripts 2>nul
mkdir notebooks 2>nul
mkdir figures 2>nul
mkdir output 2>nul
mkdir docs 2>nul
mkdir tests 2>nul
python -m venv venv
call venv\\Scripts\\activate.bat
pip install -r requirements.txt
pause
'''

if __name__ == "__main__":
    # Criar scripts alternativos com encoding seguro
    try:
        Path('setup.sh').write_text(BASH_SCRIPT, encoding='utf-8')
        print("  OK setup.sh criado")
        
        Path('setup.bat').write_text(BATCH_SCRIPT, encoding='utf-8')
        print("  OK setup.bat criado")
    except Exception as e:
        print(f"Aviso ao criar scripts extras: {e}")
    
    # Executar setup principal
    setup = ProjectSetup()
    setup.run()