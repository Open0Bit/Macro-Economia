import pytest
import os

def test_directory_structure():
    """Verifica se pastas necessárias existem"""
    assert os.path.exists('data/raw')
    assert os.path.exists('data/processed')
    assert os.path.exists('figures')

def test_requirements_installed():
    """Verifica dependências críticas"""
    import pandas
    import numpy
    import statsmodels
    assert True
