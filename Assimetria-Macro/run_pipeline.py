"""
Script Orquestrador: Pipeline Completo de Análise
Framework: Preparação Assimétrica e Crises Sistêmicas
Autor: Gabriel W. Soares

Executa toda a pipeline analítica em sequência:
1. Download de dados públicos
2. Processamento e construção de índices
3. Análise lead-lag e causalidade de Granger
4. Análise de sincronização e event studies

Uso:
    python run_pipeline.py [--skip-download] [--verbose]
"""

import subprocess
import sys
import os
import time
from datetime import datetime
import argparse

class PipelineOrchestrator:
    """Gerencia execução completa do pipeline analítico"""
    
    def __init__(self, skip_download=False, verbose=False):
        self.skip_download = skip_download
        self.verbose = verbose
        self.start_time = time.time()
        self.scripts = [
            ('00_download_data.py', 'Download de Dados Públicos', not skip_download),
            ('01_process_data.py', 'Processamento e Construção de Índices', True),
            ('02_leadlag_analysis.py', 'Análise Lead-Lag e Causalidade Granger', True),
            ('03_synchronization.py', 'Análise de Sincronização e Event Studies', True)
        ]
    
    def print_header(self):
        """Imprime cabeçalho do pipeline"""
        print("\n" + "="*70)
        print(" " * 10 + "FRAMEWORK DE PREPARAÇÃO ASSIMÉTRICA")
        print(" " * 15 + "Pipeline Analítico Completo")
        print("="*70)
        print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.skip_download:
            print("Modo: Processamento apenas (download de dados pulado)")
        else:
            print("Modo: Análise completa (incluindo download)")
        
        print("="*70 + "\n")
    
    def print_step(self, step_num, total_steps, script_name, description):
        """Imprime informação do passo atual"""
        print("\n" + "-"*70)
        print(f"[{step_num}/{total_steps}] {description}")
        print(f"Script: {script_name}")
        print("-"*70)
    
    def run_script(self, script_path):
        """Executa um script Python e captura output"""
        try:
            if self.verbose:
                # Mostrar output completo
                result = subprocess.run(
                    [sys.executable, script_path],
                    check=True,
                    capture_output=False
                )
            else:
                # Capturar output e mostrar apenas resumo
                result = subprocess.run(
                    [sys.executable, script_path],
                    check=True,
                    capture_output=True,
                    text=True
                )
                
                # Extrair linhas com ✓ ou ✗ para resumo
                lines = result.stdout.split('\n')
                summary_lines = [line for line in lines 
                               if '✓' in line or '✗' in line or 'ERRO' in line.upper()]
                
                if summary_lines:
                    print("\nResumo da execução:")
                    for line in summary_lines[:10]:  # Mostrar até 10 linhas de resumo
                        print(line)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n✗ ERRO na execução de {script_path}")
            if hasattr(e, 'stderr') and e.stderr:
                print(f"Mensagem de erro:\n{e.stderr}")
            return False
        
        except Exception as e:
            print(f"\n✗ ERRO inesperado: {str(e)}")
            return False
    
    def check_dependencies(self):
        """Verifica se dependências necessárias estão instaladas"""
        print("Verificando dependências...")
        
        required_packages = [
            'pandas',
            'numpy',
            'matplotlib',
            'statsmodels',
            'yfinance',
            'scipy',
            'seaborn'
        ]
        
        missing = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✓ {package}")
            except ImportError:
                print(f"  ✗ {package} não encontrado")
                missing.append(package)
        
        if missing:
            print(f"\n✗ Dependências faltando: {', '.join(missing)}")
            print(f"✗ Instale com: pip install {' '.join(missing)}")
            return False
        
        print("✓ Todas as dependências estão instaladas\n")
        return True
    
    def create_directories(self):
        """Cria estrutura de diretórios necessária"""
        directories = [
            'data/raw',
            'data/processed',
            'scripts',
            'figures',
            'output',
            'docs'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def run(self):
        """Executa pipeline completo"""
        self.print_header()
        
        # Verificar dependências
        if not self.check_dependencies():
            return False
        
        # Criar estrutura
        self.create_directories()
        
        # Executar scripts em sequência
        active_scripts = [(s, d) for s, d, active in self.scripts if active]
        total_steps = len(active_scripts)
        
        for idx, (script_name, description) in enumerate(active_scripts, 1):
            script_path = f'scripts/{script_name}'
            
            # Verificar se script existe
            if not os.path.exists(script_path):
                print(f"\n✗ ERRO: Script {script_path} não encontrado!")
                print(f"✗ Certifique-se de que todos os scripts estão na pasta 'scripts/'")
                return False
            
            # Executar
            self.print_step(idx, total_steps, script_name, description)
            
            success = self.run_script(script_path)
            
            if not success:
                print(f"\n✗ Pipeline interrompido devido a erro em {script_name}")
                return False
            
            print(f"✓ {description} concluído com sucesso")
        
        # Finalização
        self.print_completion_summary()
        return True
    
    def print_completion_summary(self):
        """Imprime resumo de conclusão"""
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        print("\n" + "="*70)
        print(" " * 20 + "PIPELINE CONCLUÍDO COM SUCESSO")
        print("="*70)
        print(f"Tempo total de execução: {minutes}m {seconds}s")
        print(f"Conclusão: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n📊 OUTPUTS GERADOS:")
        
        # Listar arquivos gerados
        output_files = {
            'Dados Processados': [
                'data/processed/etf_returns.csv',
                'data/processed/stress_index.csv',
                'data/processed/exposure_proxy.csv',
                'data/processed/defensive_concentration.csv',
                'data/processed/synchronization_index.csv',
                'data/processed/monthly_data.csv'
            ],
            'Figuras e Gráficos': [
                'figures/cross_correlation.png',
                'figures/impulse_response.png',
                'figures/synchronization_analysis.png',
                'figures/comprehensive_report.png'
            ]
        }
        
        for category, files in output_files.items():
            print(f"\n  {category}:")
            for file in files:
                if os.path.exists(file):
                    size_kb = os.path.getsize(file) / 1024
                    print(f"    ✓ {file:45s} ({size_kb:.1f} KB)")
                else:
                    print(f"    ✗ {file:45s} (não gerado)")
        
        print("\n📖 PRÓXIMOS PASSOS:")
        print("  1. Revisar gráficos em: figures/")
        print("  2. Consultar dados processados em: data/processed/")
        print("  3. Ler documentação teórica em: TESE.md ou FRAMEWORK.md")
        print("  4. Adaptar análises para outros contextos/períodos")
        
        print("\n💡 PARA REPLICAR:")
        print("  python run_pipeline.py           # Execução completa")
        print("  python run_pipeline.py --skip-download  # Pular download")
        print("  python run_pipeline.py --verbose        # Output detalhado")
        
        print("\n" + "="*70 + "\n")

def main():
    """Função principal com argumentos de linha de comando"""
    parser = argparse.ArgumentParser(
        description='Framework de Preparação Assimétrica - Pipeline Analítico',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python run_pipeline.py                    # Execução completa
  python run_pipeline.py --skip-download    # Pular download de dados
  python run_pipeline.py --verbose          # Mostrar output completo
  python run_pipeline.py --skip-download --verbose  # Combinação
        """
    )
    
    parser.add_argument(
        '--skip-download',
        action='store_true',
        help='Pula download de dados (assume que dados já existem)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mostra output completo de cada script'
    )
    
    args = parser.parse_args()
    
    # Executar pipeline
    orchestrator = PipelineOrchestrator(
        skip_download=args.skip_download,
        verbose=args.verbose
    )
    
    success = orchestrator.run()
    
    # Exit code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()