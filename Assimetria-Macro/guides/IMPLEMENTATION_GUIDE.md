# Guia Prático de Implementação
## Framework de Preparação Assimétrica

**Para:** Pesquisadores, Analistas e Estudantes  
**Nível:** Intermediário (conhecimento básico de Python)  
**Tempo estimado:** 30 minutos para setup completo

---

## Início Rápido: 5 Minutos

Se você quer resultados imediatos sem detalhes técnicos:

```bash
# 1. Clonar repositório
git clone https://github.com/Open0Bit/Macro-Economia.git
cd Macro-Economia/Assimetria-Macro

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar pipeline completo
python run_pipeline.py

# 4. Ver resultados
# Abra os arquivos PNG em: figures/
```

**Pronto!** Você terá análises completas em `figures/` e dados processados em `data/processed/`.

---

## Setup Detalhado: Passo a Passo

### Passo 1: Verificar Ambiente

Antes de começar, certifique-se de ter:

**Sistema Operacional:**
- Windows 10/11, macOS 10.14+, ou Linux (Ubuntu 18.04+)

**Software:**
```bash
# Verificar Python
python --version  # Deve ser 3.8 ou superior

# Se não tiver Python, instale:
# Windows: https://www.python.org/downloads/
# Mac: brew install python3
# Linux: sudo apt-get install python3
```

**Espaço em disco:**
- Mínimo: 500MB
- Recomendado: 2GB (para dados históricos extensos)

### Passo 2: Preparar Ambiente Virtual

Ambiente virtual isola dependências do projeto:

**Linux/Mac:**
```bash
# Criar ambiente
python3 -m venv venv

# Ativar
source venv/bin/activate

# Verificar ativação (prompt deve mostrar "(venv)")
which python  # Deve apontar para venv/bin/python
```

**Windows (Command Prompt):**
```cmd
# Criar ambiente
python -m venv venv

# Ativar
venv\Scripts\activate.bat

# Verificar ativação
where python
```

**Windows (PowerShell):**
```powershell
# Criar ambiente
python -m venv venv

# Ativar (pode requerer permissões)
venv\Scripts\Activate.ps1

# Se erro de permissão:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Passo 3: Instalar Dependências

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar pacotes do requirements.txt
pip install -r requirements.txt

# Verificar instalação
pip list | grep -E "(pandas|numpy|statsmodels|yfinance)"
```

**Resolução de problemas comuns:**

**Erro: "No module named 'pandas'"**
```bash
pip install pandas --force-reinstall
```

**Erro: "Could not build wheels for statsmodels"**
```bash
# Linux/Mac: Instalar compilador C
sudo apt-get install build-essential  # Linux
xcode-select --install  # Mac

# Windows: Instalar Visual C++ Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**Erro: "SSL certificate verify failed" (yfinance)**
```bash
# Desabilitar verificação SSL (temporário)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org yfinance
```

### Passo 4: Estrutura de Pastas

O script `run_pipeline.py` cria pastas automaticamente, mas você pode criar manualmente:

```bash
mkdir -p data/{raw,processed}
mkdir -p figures
mkdir -p output
mkdir -p scripts
```

### Passo 5: Verificar Scripts

Certifique-se de que todos os scripts estão em `scripts/`:

```bash
ls scripts/
# Deve listar:
# 00_download_data.py
# 01_process_data.py
# 02_leadlag_analysis.py
# 03_synchronization.py
```

Se faltarem, baixe novamente do repositório.

---

## Executando Análises: Opções Detalhadas

### Opção A: Pipeline Completo (Recomendado)

```bash
python run_pipeline.py
```

**O que acontece:**
1. Baixa preços históricos de ETFs (Yahoo Finance) - ~2 min
2. Baixa indicadores macro (FRED) - ~1 min
3. Processa dados e constrói índices - ~30 seg
4. Executa análise lead-lag e Granger - ~1 min
5. Calcula sincronização e event studies - ~1 min

**Total:** ~5-7 minutos

**Output esperado:**
```
======================================================================
                    FRAMEWORK DE PREPARAÇÃO ASSIMÉTRICA
                        Pipeline Analítico Completo
======================================================================
Início: 2024-12-27 10:00:00
Modo: Análise completa (incluindo download)
======================================================================

Verificando dependências...
  ✓ pandas
  ✓ numpy
  ✓ matplotlib
  ...
✓ Todas as dependências estão instaladas

----------------------------------------------------------------------
[1/4] Download de Dados Públicos
Script: 00_download_data.py
----------------------------------------------------------------------
...
✓ Download de Dados Públicos concluído com sucesso

[... processos continuam ...]

======================================================================
                     PIPELINE CONCLUÍDO COM SUCESSO
======================================================================
Tempo total de execução: 6m 23s
```

### Opção B: Execução Incremental

Se quiser controlar cada etapa:

**Etapa 1: Download**
```bash
python scripts/00_download_data.py

# Verificar outputs
ls data/raw/
# Deve conter:
# - etf_prices.csv
# - macro_indicators.csv (se FRED funcionar)
# - volatility_proxy.csv
```

**Etapa 2: Processamento**
```bash
python scripts/01_process_data.py

# Verificar outputs
ls data/processed/
# Deve conter:
# - etf_returns.csv
# - stress_index.csv
# - exposure_proxy.csv
# - defensive_concentration.csv
# - monthly_data.csv
```

**Etapa 3: Lead-Lag**
```bash
python scripts/02_leadlag_analysis.py

# Verificar outputs
ls figures/
# Deve conter:
# - cross_correlation.png
# - impulse_response.png
```

**Etapa 4: Sincronização**
```bash
python scripts/03_synchronization.py

# Verificar outputs
ls figures/
# Deve conter:
# - synchronization_analysis.png
# - comprehensive_report.png
```

### Opção C: Análise Sem Download

Se você já tem dados ou quer testar processamento apenas:

```bash
python run_pipeline.py --skip-download
```

Útil para:
- Re-executar análises com parâmetros diferentes
- Testar mudanças no código sem re-baixar dados
- Trabalhar offline

---

## Interpretando Resultados: Guia Visual

### Arquivo: cross_correlation.png

**O que mostra:** Correlação entre mudanças em exposição e estresse para diferentes lags temporais.

**Como interpretar:**
- **Eixo X (Lag):** Meses de defasagem
  - Lag negativo = Exposição precede Estresse
  - Lag positivo = Estresse precede Exposição
  - Lag zero = Contemporâneo
  
- **Eixo Y (Correlação):** Força da relação
  - Valores negativos = Quando exposição cai, estresse sobe
  - Valores positivos = Quando exposição sobe, estresse sobe
  
- **Linhas tracejadas vermelhas:** Threshold de significância (~0.2)

**Padrão esperado se H1 é verdadeira:**
- Correlação negativa forte em lags negativos (exposure precede)
- Correlação fraca/insignificante em lags positivos

**Exemplo de interpretação:**
```
Se correlação em lag -3 = -0.35 (significante):
→ Quedas em exposição institucional precedem aumentos em estresse
  por aproximadamente 3 meses
→ Consistente com mecanismo de antecipação
```

### Arquivo: synchronization_analysis.png

**O que mostra:** Quatro painéis comparando sincronização em diferentes condições.

**Painel 1 (Superior Esquerdo):** Série temporal de sincronização
- Áreas vermelhas = Períodos de alto estresse
- Observar se sincronização aumenta nessas áreas

**Painel 2 (Superior Direito):** Box plots comparativos
- Caixa azul = Baixo estresse
- Caixa vermelha = Alto estresse
- Se caixa vermelha está mais alta: sincronização aumenta com estresse

**Painel 3 (Inferior Esquerdo):** Scatter plot
- Cada ponto = uma observação
- Linha vermelha = tendência
- Se linha tem inclinação positiva: mais estresse → mais sincronização

**Painel 4 (Inferior Direito):** Histogramas sobrepostos
- Azul = Distribuição em baixo estresse
- Vermelho = Distribuição em alto estresse
- Se vermelho está deslocado para direita: maior sincronização

### Arquivo: comprehensive_report.png

**O que mostra:** Painel consolidado com todas as métricas principais.

**Como usar:**
1. **Retornos cumulativos (topo):** Performance geral dos ativos
2. **Índice de Estresse (meio-esquerda):** Identificar eventos de crise
3. **Sincronização (meio-direita):** Ver se aumenta com estresse
4. **Exposição (inferior-esquerda):** Movimentos institucionais
5. **Defensivos (inferior-direita):** Rotação para segurança
6. **Resumo estatístico (fundo):** Métricas chave numéricas

**Análise integrada:**
- Procurar por padrões temporais consistentes
- Exposição cai → Sincronização sobe → Estresse aumenta?
- Defensivos sobem antes de picos de estresse?

---

## Customizando Análises

### Mudar Período de Análise

**Editar:** `scripts/00_download_data.py`

```python
# Linha ~30
start_date = "2020-01-01"  # Mudar aqui
end_date = datetime.now().strftime("%Y-%m-%d")
```

**Exemplo:** Analisar crise de 2008
```python
start_date = "2007-01-01"
end_date = "2010-12-31"
```

### Adicionar Novos ETFs

**Editar:** `scripts/00_download_data.py`

```python
# Linha ~25
etfs = {
    'FXI': 'iShares China Large-Cap ETF',
    'MCHI': 'iShares MSCI China ETF',
    # Adicionar novo ETF:
    'EWZ': 'iShares MSCI Brazil ETF',  # Exemplo: Brasil
}
```

### Ajustar Janela Rolling

**Editar:** `scripts/03_synchronization.py`

```python
# Linha ~40
window = 90  # dias, mudar para 60, 120, etc.
```

Janelas menores = mais sensível a mudanças
Janelas maiores = mais suave, menos ruído

### Modificar Threshold de Eventos

**Editar:** `scripts/03_synchronization.py`

```python
# Linha ~150
stress_threshold = stress['STRESS_INDEX'].mean() + 2 * stress['STRESS_INDEX'].std()
# Mudar '2' para '1.5' (mais eventos) ou '3' (menos eventos)
```

---

## Replicando para Outro País

### Exemplo: Adaptando para Brasil

**1. Identificar ETFs relevantes:**
```python
etfs = {
    'EWZ': 'iShares MSCI Brazil ETF',
    'BRXX': 'Global X Brazil 20 ETF',
    # Adicionar outros conforme necessário
}
```

**2. Ajustar indicadores macro:**

Se FRED não tem dados de Brasil, usar Yahoo Finance ou outras fontes:

```python
# Baixar BRL/USD
data = yf.download('BRLUSD=X', start=start_date, end=end_date)

# Baixar índice Bovespa
bovespa = yf.download('^BVSP', start=start_date, end=end_date)
```

**3. Construir índice de estresse customizado:**

Incluir indicadores específicos do Brasil:
- Spread de bonds brasileiros
- Volatilidade BRL
- CDS Brazil sovereign

**4. Interpretar resultados no contexto brasileiro:**

Considerar:
- Ciclos políticos (eleições)
- Dependência de commodities
- Relação com China (maior parceiro comercial)

---

## Troubleshooting: Problemas Comuns

### Problema: "ERRO: Dados brutos não encontrados"

**Causa:** Script 01 executado sem executar script 00 primeiro.

**Solução:**
```bash
# Executar download primeiro
python scripts/00_download_data.py

# Depois processar
python scripts/01_process_data.py
```

### Problema: "KeyError: 'Adj Close'"

**Causa:** Yahoo Finance mudou estrutura de dados.

**Solução:**
Editar `scripts/00_download_data.py`, linha onde usa yf.download:
```python
# Versão antiga
data = yf.download(tickers, start=start_date)['Adj Close']

# Versão corrigida
data = yf.download(tickers, start=start_date, auto_adjust=False)['Adj Close']
```

### Problema: "pandas-datareader error: Remote data access failed"

**Causa:** FRED API às vezes tem instabilidade ou requer API key.

**Solução 1:** Tentar novamente (pode ser timeout temporário)
```bash
python scripts/00_download_data.py
```

**Solução 2:** Pipeline funciona sem FRED (usa proxies)
```bash
# Continue com análise mesmo sem indicadores FRED
python scripts/01_process_data.py
```

**Solução 3:** Registrar para API key gratuita
1. Ir para: https://fred.stlouisfed.org/docs/api/api_key.html
2. Criar conta (gratuita)
3. Obter API key
4. Adicionar ao script:
```python
import os
os.environ['FRED_API_KEY'] = 'sua_chave_aqui'
```

### Problema: "Insufficient data for VAR estimation"

**Causa:** Período muito curto ou muitos dados faltantes.

**Solução:** Expandir período de análise
```python
# No script 00, aumentar janela temporal
start_date = "2018-01-01"  # ao invés de 2020
```

### Problema: Gráficos não abrem automaticamente

**Causa:** Backend matplotlib não configurado para display.

**Solução:** Gráficos são salvos automaticamente em `figures/`
```bash
# Abrir manualmente
# Mac:
open figures/comprehensive_report.png

# Linux:
xdg-open figures/comprehensive_report.png

# Windows:
start figures\comprehensive_report.png
```

---

## Workflow para Pesquisa Acadêmica

### Fase 1: Replicação Básica (Dia 1)

```bash
# 1. Setup inicial
git clone [repo]
cd Assimetria-Macro
pip install -r requirements.txt

# 2. Executar pipeline padrão
python run_pipeline.py

# 3. Revisar outputs
# - Ler FRAMEWORK.md para entender framework
# - Examinar figuras/ para padrões visuais
# - Revisar data/processed/ para dados numéricos
```

**Deliverable:** Compreensão do framework e validação de que pipeline funciona

### Fase 2: Adaptação ao Contexto (Dias 2-3)

```bash
# 1. Modificar período
# Editar scripts/00_download_data.py
start_date = "[seu_periodo]"

# 2. Adicionar ETFs/ativos relevantes ao seu estudo
etfs = {
    # ... seus ativos
}

# 3. Re-executar
python run_pipeline.py --skip-download  # se dados locais estão ok
```

**Deliverable:** Análise customizada para seu contexto geográfico/temporal

### Fase 3: Análise Aprofundada (Dias 4-7)

```python
# Criar notebook Jupyter para análises customizadas
import pandas as pd
import numpy as np

# Carregar dados processados
stress = pd.read_csv('data/processed/stress_index.csv', 
                     index_col=0, parse_dates=True)

# Suas análises adicionais aqui
# - Regressions com variáveis adicionais
# - Análises de subperíodos
# - Testes de robustez
```

**Deliverable:** Insights específicos ao seu tema de pesquisa

### Fase 4: Escrita e Documentação (Dias 8-14)

- Usar FRAMEWORK.md como template para seu paper
- Adaptar seções para seu contexto
- Incluir seus resultados customizados
- Citar apropriadamente o framework original

**Deliverable:** Artigo ou working paper

---

## Checklist de Validação

Antes de reportar resultados, verificar:

### Qualidade de Dados
- [ ] Dados cobrem período completo sem gaps significativos
- [ ] Nenhum outlier obviamente errôneo (e.g., preço = 0)
- [ ] Séries temporais têm sobreposição suficiente para análise

### Testes Estatísticos
- [ ] Tamanho de amostra adequado (mínimo 30 observações para VAR)
- [ ] Séries são estacionárias ou foram diferenciadas
- [ ] p-values são significativos no nível apropriado (<0.05 ou <0.01)
- [ ] Resultados são robustos a especificações alternativas

### Interpretação
- [ ] Distinção clara entre correlação e causalidade
- [ ] Limitações explicitamente reconhecidas
- [ ] Interpretações são qualificadas apropriadamente
- [ ] Explicações alternativas consideradas

### Documentação
- [ ] Código está comentado e compreensível
- [ ] Figuras têm títulos e legendas claras
- [ ] Metodologia está documentada em detalhe
- [ ] Resultados são replicáveis

---

## Recursos Adicionais

### Tutoriais Python Financeiro
- **Pandas for Finance:** https://pandas.pydata.org/docs/user_guide/10min.html
- **Statsmodels VAR:** https://www.statsmodels.org/stable/vector_ar.html
- **yfinance Documentation:** https://github.com/ranaroussi/yfinance

### Teoria Econométrica
- **Granger Causality:** https://en.wikipedia.org/wiki/Granger_causality
- **VAR Models:** Hamilton, J.D. (1994). Time Series Analysis. Princeton.

### Aplicações Similares
- **Systemic Risk:** https://www.systemic-risk-hub.org/
- **Financial Stress Indices:** St. Louis Fed Financial Stress Index

---

## Suporte

**Documentação completa:** README.md  
**Framework teórico:** FRAMEWORK.md  
**Issues GitHub:** [[repositório](https://github.com/Open0Bit/Macro-Economia/tree/main/Assimetria-Macro)]  

**Para dúvidas:**
1. Primeiro, consultar FAQ no README.md
2. Verificar se é problema conhecido neste guia
3. Abrir issue no GitHub com detalhes (logs de erro, sistema operacional, versão Python)

---

**Última atualização:** Dezembro 2024  
**Versão:** 1.0  
**Autor:** Gabriel W. Soares
