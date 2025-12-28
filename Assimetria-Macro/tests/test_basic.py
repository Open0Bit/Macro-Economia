import pytest
import os
# =============================================================================
# tests/__init__.py
# =============================================================================
"""
Testes unitários para o Framework de Preparação Assimétrica
"""

__version__ = "1.0.0"


# =============================================================================
# tests/test_basic.py
# =============================================================================
"""
Testes básicos para garantir que o pipeline funciona
"""

import pytest
import os
import sys

# Adicionar pasta raiz ao path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def test_directory_structure():
    """Verifica se pastas necessárias existem"""
    assert os.path.exists('scripts'), 'Pasta scripts/ não encontrada'
    assert os.path.exists('run_pipeline.py'), 'run_pipeline.py não encontrado'
    print("✓ Estrutura de pastas OK")


def test_scripts_exist():
    """Verifica se todos os scripts existem"""
    scripts = [
        'scripts/00_download_data.py',
        'scripts/01_process_data.py',
        'scripts/02_leadlag_analysis.py',
        'scripts/03_synchronization.py'
    ]
    
    for script in scripts:
        assert os.path.exists(script), f'{script} não encontrado'
    
    print("✓ Todos os scripts existem")


def test_imports():
    """Testa se bibliotecas necessárias estão instaladas"""
    try:
        import pandas
        import numpy
        import matplotlib
        import statsmodels
        import yfinance
        print("✓ Todas as bibliotecas estão instaladas")
    except ImportError as e:
        pytest.fail(f"Biblioteca não encontrada: {str(e)}")


def test_requirements_file():
    """Verifica se requirements.txt existe"""
    assert os.path.exists('requirements.txt'), 'requirements.txt não encontrado'
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
        assert 'pandas' in content, 'pandas não está em requirements.txt'
        assert 'numpy' in content, 'numpy não está em requirements.txt'
    
    print("✓ requirements.txt OK")


def test_documentation_exists():
    """Verifica se documentação existe"""
    docs = ['README.md', 'FRAMEWORK.md', 'IMPLEMENTATION_GUIDE.md']
    
    for doc in docs:
        assert os.path.exists(doc), f'{doc} não encontrado'
    
    print("✓ Documentação completa")


def test_pipeline_imports():
    """Testa se run_pipeline.py pode ser importado"""
    try:
        import run_pipeline
        assert hasattr(run_pipeline, 'PipelineOrchestrator'), 'PipelineOrchestrator não encontrado'
        print("✓ run_pipeline.py pode ser importado")
    except Exception as e:
        pytest.fail(f"Erro ao importar run_pipeline.py: {str(e)}")


if __name__ == "__main__":
    # Executar testes localmente
    pytest.main([__file__, '-v'])