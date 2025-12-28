# Guia de Configuração Avançada
## Framework de Preparação Assimétrica

Este guia explica como configurar e usar os recursos avançados do repositório.

---

## 📓 1. Jupyter Notebooks

### 1.1 Instalação

```bash
# Se ainda não tiver Jupyter instalado
pip install jupyter notebook

# Ou usar JupyterLab (interface mais moderna)
pip install jupyterlab
```

### 1.2 Executar Notebook

```bash
# Método 1: Jupyter Notebook clássico
jupyter notebook notebooks/01_Quick_Start.ipynb

# Método 2: JupyterLab
jupyter lab

# Método 3: VS Code (se instalado)
# Abra o arquivo .ipynb diretamente no VS Code
```

### 1.3 Criar Seus Próprios Notebooks

```bash
# Criar novo notebook
jupyter notebook notebooks/02_Minha_Analise.ipynb

# Estrutura recomendada:
notebooks/
  ├── 01_Quick_Start.ipynb         # Análise rápida (fornecido)
  ├── 02_Custom_Analysis.ipynb     # Suas análises customizadas
  ├── 03_Country_Comparison.ipynb  # Comparações entre países
  └── 04_Historical_Study.ipynb    # Estudos históricos
```

### 1.4 Dicas de Uso

**Executar todas as células:**
```python
# No notebook, apertar:
# Shift + Enter = Executar célula atual e ir para próxima
# Ctrl + Enter = Executar célula atual
# Cell > Run All = Executar todas
```

**Exportar para PDF/HTML:**
```bash
# Exportar para HTML
jupyter nbconvert --to html notebooks/01_Quick_Start.ipynb

# Exportar para PDF (requer LaTeX)
jupyter nbconvert --to pdf notebooks/01_Quick_Start.ipynb
```

---

## ⚙️ 2. Arquivo .env (Configuração)

### 2.1 Criar Arquivo .env

```bash
# Copiar template
cp .env.example .env

# Editar com seu editor preferido
nano .env
# ou
vim .env
# ou abra no VS Code
```

### 2.2 Configurar API Keys (Opcional)

**FRED API Key (Recomendado):**
1. Acesse: https://fred.stlouisfed.org/
2. Crie conta gratuita
3. Vá em: My Account > API Keys > Request API Key
4. Copie a chave e cole no .env:
```bash
FRED_API_KEY=sua_chave_aqui_12345abcde
```

### 2.3 Usar Configuração nos Scripts

**Opção 1: Modificar scripts para ler .env**

Adicione no início de cada script Python:

```python
# No topo do arquivo, após imports
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

# Usar variáveis
start_date = os.getenv('START_DATE', '2020-01-01')  # padrão se não definido
fred_key = os.getenv('FRED_API_KEY')

if fred_key:
    # Usar API key
    os.environ['FRED_API_KEY'] = fred_key
```

**Instalar python-dotenv:**
```bash
pip install python-dotenv
# Adicionar ao requirements.txt:
echo "python-dotenv>=1.0.0" >> requirements.txt
```

**Opção 2: Modificar run_pipeline.py**

Adicione suporte a argumentos de linha de comando:

```bash
python run_pipeline.py --start-date 2015-01-01 --end-date 2024-12-31 --var-lag 12
```

---

## 🔄 3. GitHub Actions (CI/CD)

### 3.1 Estrutura do Arquivo

GitHub Actions usa o arquivo `.github/workflows/tests.yml` que já foi criado.

**Estrutura de pastas:**
```
.github/
  └── workflows/
      └── tests.yml    # Arquivo de configuração do CI
```

### 3.2 O Que o CI Faz Automaticamente

Quando você faz `git push` ou cria Pull Request, o GitHub automaticamente:

1. ✅ Testa código em Python 3.8, 3.9, 3.10, 3.11
2. ✅ Verifica se todos os imports funcionam
3. ✅ Executa testes unitários
4. ✅ Valida estrutura de pastas
5. ✅ Verifica estilo de código (PEP 8)
6. ✅ Testa download de dados
7. ✅ Valida documentação

### 3.3 Ver Resultados do CI

1. Vá ao seu repositório no GitHub
2. Clique na aba **Actions**
3. Veja status dos workflows:
   - ✅ Verde = Passou
   - ❌ Vermelho = Falhou
   - 🟡 Amarelo = Em execução

### 3.4 Badge de Status no README

Adicione ao topo do README.md:

```markdown
![Tests](https://github.com/seu-usuario/Macro-Economia/workflows/Tests%20e%20Validação/badge.svg)
```

Substitua `seu-usuario` pelo seu username do GitHub.

### 3.5 Configurar Notificações

**Por email:**
1. GitHub > Settings > Notifications
2. Ativar "Actions" notifications

**Por Slack/Discord (Avançado):**
```yaml
# Adicionar ao final de .github/workflows/tests.yml
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  if: always()
```

### 3.6 Desabilitar CI (Se Necessário)

Se quiser desabilitar temporariamente:

```bash
# Renomear arquivo
mv .github/workflows/tests.yml .github/workflows/tests.yml.disabled

# Para reabilitar
mv .github/workflows/tests.yml.disabled .github/workflows/tests.yml
```

---

## 🧪 4. Testes Unitários

### 4.1 Estrutura de Testes

```
tests/
  ├── __init__.py
  ├── test_pipeline.py          # Teste do pipeline
  ├── test_data_processing.py   # Testes de processamento
  └── test_analysis.py          # Testes de análise
```

### 4.2 Executar Testes Localmente

```bash
# Instalar pytest
pip install pytest pytest-cov

# Executar todos os testes
pytest tests/

# Executar com verbose
pytest tests/ -v

# Executar teste específico
pytest tests/test_pipeline.py

# Com cobertura de código
pytest tests/ --cov=scripts --cov-report=html
# Ver relatório: open htmlcov/index.html
```

### 4.3 Exemplo de Teste

```python
# tests/test_data_processing.py
import pytest
import pandas as pd
import os

def test_etf_returns_creation():
    """Testa se arquivo de retornos é criado corretamente"""
    
    # Assumir que pipeline foi executado
    file_path = 'data/processed/etf_returns.csv'
    
    assert os.path.exists(file_path), "Arquivo de retornos não encontrado"
    
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    
    assert len(df) > 0, "Arquivo está vazio"
    assert df.index.is_monotonic_increasing, "Datas não estão ordenadas"
    assert not df.isnull().all().any(), "Coluna completamente nula encontrada"

def test_stress_index_range():
    """Testa se índice de estresse está em range razoável"""
    
    stress = pd.read_csv('data/processed/stress_index.csv', 
                         index_col=0, parse_dates=True)
    
    # Z-scores devem estar majoritariamente entre -3 e 3
    assert (stress['STRESS_INDEX'].abs() < 5).sum() > len(stress) * 0.95
```

---

## 🐛 5. Troubleshooting

### 5.1 Jupyter não inicia

```bash
# Erro: "jupyter: command not found"
pip install --upgrade jupyter

# Erro: "Port already in use"
jupyter notebook --port 8889

# Erro: Kernel morreu
pip install --upgrade ipykernel
python -m ipykernel install --user
```

### 5.2 .env não é lido

```bash
# Verificar se python-dotenv está instalado
pip list | grep dotenv

# Verificar se arquivo existe
ls -la .env

# Verificar se variáveis são carregadas
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('START_DATE'))"
```

### 5.3 GitHub Actions falha

**Erro comum 1: "Module not found"**
- Adicione módulo ao `requirements.txt`

**Erro comum 2: "Tests failed"**
- Execute testes localmente: `pytest tests/ -v`
- Corrija erros antes de fazer push

**Erro comum 3: "Timeout"**
- Download pode demorar no CI
- Aumente timeout em `.github/workflows/tests.yml`:
```yaml
timeout-minutes: 10  # Aumentar se necessário
```

### 5.4 Testes falham localmente

```bash
# Limpar cache
pytest --cache-clear

# Executar em modo debug
pytest tests/ -vv --tb=long

# Executar apenas um teste
pytest tests/test_pipeline.py::test_directory_structure -v
```

---

## 📚 6. Recursos Adicionais

### 6.1 Documentação Oficial

- **Jupyter:** https://jupyter.org/documentation
- **GitHub Actions:** https://docs.github.com/en/actions
- **pytest:** https://docs.pytest.org/
- **python-dotenv:** https://pypi.org/project/python-dotenv/

### 6.2 Tutoriais

- **Jupyter para Cientistas de Dados:** https://www.datacamp.com/tutorial/tutorial-jupyter-notebook
- **GitHub Actions para Python:** https://realpython.com/python-continuous-integration/
- **pytest Best Practices:** https://docs.pytest.org/en/stable/goodpractices.html

### 6.3 Vídeos (YouTube)

- "Jupyter Notebook Tutorial" - Corey Schafer
- "GitHub Actions Tutorial" - Tech With Tim
- "Python Testing with pytest" - ArjanCodes

---

## ✅ Checklist de Configuração

Use este checklist para garantir que tudo está configurado:

- [ ] Jupyter instalado e funcionando
- [ ] Notebook `01_Quick_Start.ipynb` executa sem erros
- [ ] Arquivo `.env` criado e configurado
- [ ] FRED API Key obtida (opcional mas recomendado)
- [ ] GitHub Actions configurado (arquivo `.github/workflows/tests.yml`)
- [ ] Testes unitários passam localmente (`pytest tests/`)
- [ ] Badge de status adicionado ao README
- [ ] python-dotenv instalado
- [ ] pytest instalado

---

## 🆘 Precisa de Ajuda?

1. **Consulte primeiro:** [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
2. **Issues no GitHub:** Abra issue detalhando o problema
3. **Discussions:** Use para perguntas gerais
4. **Stack Overflow:** Tag com `python`, `jupyter`, `github-actions`

---

**Autor:** Gabriel W. Soares  
**Versão:** 1.0  
**Data:** Dezembro 2024