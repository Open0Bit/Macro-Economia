# Framework Teórico-Metodológico: Preparação Assimétrica e Crises Sistêmicas

**Autor:** Gabriel W. Soares  
**Tipo:** Framework Teórico com Demonstração Empírica  
**Versão:** 3.0  
**Status:** ✅ Completo e Funcional  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange)
![Tests](https://github.com/Open0Bit/Macro-Economia/actions/workflows/assimetria-macro-tests.yml/badge.svg)

---

## Visão Geral

Este repositório apresenta um framework teórico-metodológico para análise de crises financeiras sistêmicas, focando especificamente no conceito de "preparação assimétrica". O projeto oferece protocolo sistemático e replicável para investigar como preparação não-coordenada de investidores institucionais pode amplificar fragilidades sistêmicas.

### O Que é Este Projeto

Este é um **framework teórico-metodológico com implementação demonstrativa** que utiliza exclusivamente dados públicos. O objetivo primário é desenvolver e validar metodologia analítica que possa ser aplicada por pesquisadores em diferentes contextos geográficos e temporais, não estabelecer causalidade definitiva sobre eventos específicos.

### O Que Este Projeto NÃO É

Este projeto não é uma análise empírica conclusiva sobre crises específicas. Não utilizamos dados proprietários de tracking institucional (EPFR, Bloomberg Terminal, Wind Database). Os resultados são indicativos da metodologia proposta, não conclusivos sobre causalidade econômica.

---

## Conceito Central: Preparação Assimétrica

**Definição:** Reposicionamento estratégico por atores com informação ou recursos superiores que, individualmente racional, produz externalidades negativas quando agregado, amplificando crises que os atores buscavam evitar.

### Mecanismos Operacionais

**M1 - Antecipação Via Assimetria Informacional**  
Investidores sofisticados detectam fragilidades estruturais mais cedo através de acesso privilegiado a informação, redes de comunicação superiores e capacidade analítica avançada.

**M2 - Sincronização Emergente Sem Coordenação**  
Convergência de estratégias ocorre organicamente através de sinais públicos comuns, modelos de risco similares e observação de pares, sem necessidade de comunicação explícita.

**M3 - Amplificação Via Limiares Críticos**  
Sistemas financeiros exibem não-linearidade: pequenos fluxos são absorvidos, mas além de threshold crítico, cascatas desproporcionais emergem.

---

## Estrutura do Repositório

```
Assimetria-Macro/
│
├── data/
│   ├── raw/                  # Dados brutos (ETFs, indicadores macro)
│   └── processed/            # Dados processados (índices, retornos)
│
├── scripts/
│   ├── 00_download_data.py   # Download de dados públicos
│   ├── 01_process_data.py    # Processamento e índices
│   ├── 02_leadlag_analysis.py    # Causalidade de Granger
│   └── 03_synchronization.py     # Sincronização e event studies
│
├── figures/                  # Visualizações geradas
│
├── FRAMEWORK.md                   # Framework teórico completo (v3.0)
├── run_pipeline.py           # Orquestrador principal
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

---

## Instalação e Configuração

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- 2GB de espaço em disco
- Conexão com internet (para download de dados)

### Passo 1: Clonar Repositório

```bash
git clone https://github.com/Open0Bit/Macro-Economia.git
cd Macro-Economia/Assimetria-Macro
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

Bibliotecas instaladas:
- **pandas**: Manipulação de dados
- **numpy**: Operações numéricas
- **matplotlib/seaborn**: Visualizações
- **statsmodels**: Análises econométricas (VAR, Granger)
- **yfinance**: Download de dados de ETFs
- **scipy**: Testes estatísticos
- **pandas-datareader**: Acesso a FRED (opcional)

---

## Uso: Executando a Análise

### Execução Completa (Recomendado)

```bash
python run_pipeline.py
```

Este comando executa toda a pipeline automaticamente:
1. Download de dados públicos (Yahoo Finance, FRED)
2. Processamento e construção de índices
3. Análise lead-lag e causalidade de Granger
4. Análise de sincronização e event studies

**Tempo estimado:** 5-10 minutos (dependendo da conexão)

### Execução Passo a Passo

Se preferir executar etapas individualmente:

```bash
# Etapa 1: Download
python scripts/00_download_data.py

# Etapa 2: Processamento
python scripts/01_process_data.py

# Etapa 3: Análise Lead-Lag
python scripts/02_leadlag_analysis.py

# Etapa 4: Sincronização
python scripts/03_synchronization.py
```

### Opções Avançadas

```bash
# Pular download (assumir que dados já existem)
python run_pipeline.py --skip-download

# Mostrar output detalhado de cada script
python run_pipeline.py --verbose

# Combinação
python run_pipeline.py --skip-download --verbose
```

---

## Outputs Gerados

### Dados Processados (data/processed/)

| Arquivo | Descrição |
|---------|-----------|
| `etf_returns.csv` | Retornos logarítmicos diários de ETFs |
| `stress_index.csv` | Índice de Estresse Sistêmico normalizado |
| `exposure_proxy.csv` | Proxy de exposição institucional (FXI/SPY) |
| `defensive_concentration.csv` | Concentração em ativos defensivos (GLD/FXI) |
| `synchronization_index.csv` | Índice de sincronização entre ETFs |
| `monthly_data.csv` | Dados agregados mensalmente para análise VAR |

### Visualizações (figures/)

| Arquivo | Conteúdo |
|---------|----------|
| `cross_correlation.png` | Correlação cruzada entre exposição e estresse |
| `impulse_response.png` | Funções impulso-resposta do modelo VAR |
| `synchronization_analysis.png` | Análise comparativa de sincronização |
| `comprehensive_report.png` | Painel consolidado com todas as métricas |

---

## Fontes de Dados (Exclusivamente Públicas)

### Yahoo Finance
- **ETFs utilizados:**
  - FXI: iShares China Large-Cap ETF
  - MCHI: iShares MSCI China ETF
  - KWEB: KraneShares China Internet ETF
  - GLD: SPDR Gold Trust
  - SPY: SPDR S&P 500 ETF
  - TLT: iShares 20+ Year Treasury Bond ETF

### FRED (Federal Reserve Economic Data)
- **Indicadores:**
  - VIXCLS: CBOE Volatility Index
  - TEDRATE: TED Spread
  - T10Y2Y: 10-Year minus 2-Year Treasury Spread
  - DEXCHUS: China/USD Exchange Rate

### Bank for International Settlements (BIS)
- CDS spreads soberanos (atualizações trimestrais)

**Nota importante:** Todos os dados são de domínio público e acessíveis gratuitamente. Não utilizamos fontes proprietárias.

---

## Metodologia Analítica

### Componente 1: Índice de Estresse Sistêmico

Construído através de normalização z-score de múltiplos indicadores:

```
Stress_t = (1/N) · Σ z_i,t

onde z_i,t = (x_i,t - μ_i) / σ_i
```

Componentes incluem VIX, TED Spread, volatilidade cambial e volatilidade de equity.

### Componente 2: Proxy de Exposição Institucional

Utilizamos ratio FXI/SPY como proxy de exposição institucional agregada:

```
Exposure_t = (Price_FXI,t / Price_SPY,t) · 100
```

Lógica: ETFs grandes são predominantemente detidos por instituições; movimentos refletem decisões agregadas.

### Componente 3: Análise Lead-Lag (Causalidade de Granger)

Modelo VAR bivariado:

```
Stress_t = α + Σ β_k·ΔExposure_(t-k) + Σ γ_k·Stress_(t-k) + ε_t
```

Teste estatístico determina se mudanças em exposição precedem temporalmente mudanças em estresse.

### Componente 4: Sincronização Temporal

Correlação rolling entre retornos de múltiplos ETFs:

```
Sync_t = (2/[N(N-1)]) · Σ Σ(i<j) Corr(r_i, r_j)_t
```

Comparação estatística entre períodos de alta e baixa estresse.

### Componente 5: Concentração Defensiva

Event study analisando ratio GLD/FXI ao redor de eventos de estresse:

```
ΔDefensive_pre = Defensive_Ratio_(t-6:t-1)
```

Testa se rotação para ativos defensivos ocorre antes de manifestações de estresse.

---

## Interpretação dos Resultados

### O Que os Testes Indicam

**Causalidade de Granger significante (p<0.05):**
- Se ΔExposure → ΔStress: Movimentos institucionais precedem estresse (consistente com antecipação)
- Se ΔStress → ΔExposure: Instituições reagem a eventos públicos
- Se ambos: Feedback loop bidirecional (sistema reflexivo)

**Aumento em sincronização durante crises:**
- Consistente com mecanismo M2 (sincronização emergente)
- Não prova coordenação, mas evidencia convergência comportamental

**Concentração defensiva pré-evento:**
- Se significante e positiva: Rotação antecipa crises (consistente com H3)
- Se não significante: Reação a eventos, não antecipação

### Limitações Metodológicas

**Dados agregados:** ETFs capturam apenas fração de atividade institucional total. Investimento direto, hedge funds e private equity não são observados.

**Causalidade vs. Correlação:** Granger estabelece precedência temporal, não causalidade econômica verdadeira. Variáveis omitidas podem explicar ambos fenômenos.

**Período limitado:** Análise focada em 2020-2024. Padrões podem ser específicos a este contexto.

**Geografia específica:** Framework desenvolvido para China. Aplicabilidade a outros contextos requer validação.

---

## 📂 Estrutura de Outputs

Após executar o pipeline, os seguintes arquivos serão gerados:

### Dados Processados (`data/processed/`)

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| [`etf_returns.csv`](data/processed/etf_returns.csv) | Retornos logarítmicos diários | Análise de correlação |
| [`stress_index.csv`](data/processed/stress_index.csv) | Índice de Estresse Sistêmico | Identificação de crises |
| [`exposure_proxy.csv`](data/processed/exposure_proxy.csv) | Proxy de exposição (FXI/SPY) | Comportamento institucional |
| [`defensive_concentration.csv`](data/processed/defensive_concentration.csv) | Concentração defensiva (GLD/FXI) | Event studies |
| [`synchronization_index.csv`](data/processed/synchronization_index.csv) | Índice de sincronização | Análise de convergência |
| [`monthly_data.csv`](data/processed/monthly_data.csv) | Dados agregados mensais | Análise VAR |

### Visualizações (`figures/`)

| Figura | Preview | Descrição |
|--------|---------|-----------|
| [`cross_correlation.png`](figures/cross_correlation.png) | ![Preview](figures/cross_correlation.png) | Correlação cruzada Exposure × Stress |
| [`impulse_response.png`](figures/impulse_response.png) | ![Preview](figures/impulse_response.png) | Funções impulso-resposta (VAR) |
| [`synchronization_analysis.png`](figures/synchronization_analysis.png) | ![Preview](figures/synchronization_analysis.png) | Análise comparativa de sincronização |
| [`comprehensive_report.png`](figures/comprehensive_report.png) | ![Preview](figures/comprehensive_report.png) | Painel consolidado completo |

> **💡 Dica:** Os links acima funcionarão após a primeira execução do pipeline. As imagens serão exibidas diretamente no GitHub.

---

## 📖 Documentação Completa

- **[FRAMEWORK.md](FRAMEWORK.md)** - Framework teórico-metodológico completo (8.500 palavras)
  - Teoria de preparação assimétrica
  - Protocolo metodológico detalhado
  - Análise demonstrativa China 2020-2024
  - Referências acadêmicas
  
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Guia prático de implementação
  - Setup passo a passo
  - Troubleshooting detalhado
  - Customização de análises
  - Replicação para outros países

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guia para contribuidores
  
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de versões

- **[CITATION.cff](CITATION.cff)** - Citação acadêmica padronizada

---

## 🔬 Para Pesquisadores Acadêmicos

Se você planeja usar este framework em pesquisa acadêmica:

1. **Leia primeiro:** [FRAMEWORK.md](FRAMEWORK.md) - Contém toda a teoria e metodologia
2. **Implemente:** Use este README como guia prático
3. **Cite:** Use [CITATION.cff](CITATION.cff) ou formato BibTeX abaixo

```bibtex
@misc{soares2024preparacao,
  author = {Soares, Gabriel W.},
  title = {Framework Teórico-Metodológico: Preparação Assimétrica e Crises Sistêmicas},
  year = {2024},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Open0Bit/Macro-Economia/tree/main/Assimetria-Macro}},
  note = {Versão 3.0}
}
```

---

## 🎯 Exemplos de Uso

### Análise Rápida (5 minutos)
```bash
git clone https://github.com/Open0Bit/Macro-Economia.git
cd Macro-Economia/Assimetria-Macro
pip install -r requirements.txt
python run_pipeline.py
# Veja resultados em figures/ e data/processed/
```

### Análise Customizada (30 minutos)
```bash
# 1. Modificar período em scripts/00_download_data.py
start_date = "2015-01-01"  # Seu período desejado

# 2. Adicionar novos ETFs
etfs = {
    'FXI': 'iShares China Large-Cap ETF',
    'EWZ': 'iShares MSCI Brazil ETF',  # Exemplo: adicionar Brasil
}

# 3. Re-executar
python run_pipeline.py
```

### Pesquisa Acadêmica (1-2 semanas)
```bash
# 1. Replicar framework base
python run_pipeline.py

# 2. Ler teoria completa
cat FRAMEWORK.md

# 3. Adaptar para seu contexto
# Editar scripts conforme IMPLEMENTATION_GUIDE.md

# 4. Escrever paper usando FRAMEWORK.md como template
```
## Extensões e Pesquisa Futura

### Replicação Geográfica

Aplicar protocolo a:
- Outras economias emergentes (Turquia, Brasil, Argentina)
- Economias desenvolvidas (Japão, Europa)
- Mercados de criptomoedas

### Extensões Temporais

- Análise histórica: Crise asiática 1997, Dot-com 2000, GFC 2008
- Análise em tempo real: Dashboard de monitoramento contínuo

### Melhorias Metodológicas

- Incorporar dados alternativos (satellite imagery, sentiment analysis)
- Modelos estruturais identificados com variáveis instrumentais
- Machine learning para detecção de padrões complexos

### Validação com Dados Proprietários

Colaborações com:
- Reguladores (acesso a dados de reporting obrigatório)
- Instituições financeiras (holdings detalhados)
- Provedores de dados (EPFR, Bloomberg)

---

## Publicação e Citação

### Onde Este Trabalho É Publicável

**Apropriado para:**
- SSRN / arXiv (working papers)
- Periódicos metodológicos (Journal of Economic Methodology)
- Think tanks (Brookings, Peterson Institute)
- Capítulos de livros analíticos

**Não apropriado para (sem validação empírica adicional):**
- Periódicos empíricos top-tier (JFE, RFS)
- Journals que exigem testes estatísticos com dados proprietários

### Como Citar

```bibtex
@misc{soares2024preparacao,
  author = {Soares, Gabriel W.},
  title = {Framework Teórico-Metodológico: Preparação Assimétrica e Crises Sistêmicas},
  year = {2024},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Open0Bit/Macro-Economia/tree/main/Assimetria-Macro}},
  note = {Versão 3.0}
}
```

---

## Contribuindo

Contribuições são bem-vindas! Áreas de interesse:

**Extensões analíticas:**
- Novos indicadores de estresse
- Algoritmos de detecção de eventos
- Visualizações interativas

**Replicações:**
- Outros países/períodos
- Validação com dados alternativos

**Melhorias de código:**
- Otimização de performance
- Testes unitários
- Documentação

**Processo:**
1. Fork o repositório
2. Crie branch para sua feature (`git checkout -b feature/NovaAnalise`)
3. Commit mudanças (`git commit -m 'Adiciona nova análise X'`)
4. Push para branch (`git push origin feature/NovaAnalise`)
5. Abra Pull Request

---

## Licença

MIT License - veja arquivo `LICENSE` para detalhes.

Copyright (c) 2024 Gabriel W. Soares

---

## Contato e Suporte

**Autor:** Gabriel W. Soares

**Issues:** Para reportar bugs ou sugerir melhorias, abra issue no GitHub.

**Discussões:** Para dúvidas sobre metodologia ou interpretação, utilize Discussions no GitHub.

---

## Reconhecimentos

Este framework integra insights de múltiplas disciplinas:

**Física de Sistemas Complexos:** Bak, Tang & Wiesenfeld (1987) - Criticalidade auto-organizada

**Teoria Financeira:** Diamond & Dybvig (1983) - Profecias autorrealizáveis; Reinhart & Rogoff (2009) - Padrões históricos de crises

**Comportamento Institucional:** Lakonishok et al. (1992) - Herding; Cohen et al. (2008) - Redes informacionais

**Economia Chinesa:** Walter & Howie (2011) - Fragilidades estruturais

Agradecimentos especiais à comunidade open-source de Python financeiro, particularmente desenvolvedores de pandas, statsmodels e yfinance.

---

## Changelog

### v3.0 (2024-12) - Revisão Metodológica Completa
- Reposicionamento como framework teórico-metodológico
- Implementação completa de análises (VAR, Granger, sincronização)
- Limitação a dados públicos exclusivamente
- Documentação expandida e transparente
- Pipeline automatizado funcional

### v2.0 (2024-11) - Versão Aspiracional
- Framework conceitual desenvolvido
- Referências a dados proprietários (não implementado)
- Scripts placeholder

### v1.0 (2024-10) - Versão Inicial
- Conceito básico de preparação assimétrica
- Estrutura de pastas

---

## FAQ (Perguntas Frequentes)

**P: Este framework prova que crises são causadas por investidores institucionais?**  
R: Não. O framework identifica padrões temporais consistentes com antecipação, mas não estabelece causalidade definitiva. Distinguir entre "causar" e "antecipar muito bem" requer dados mais granulares.

**P: Posso usar este código para trading?**  
R: Este é framework de pesquisa acadêmica, não sistema de trading. Padrões históricos não garantem resultados futuros. Use por sua conta e risco.

**P: Por que não usar dados proprietários (EPFR, Bloomberg)?**  
R: Deliberadamente limitamos a dados públicos para tornar pesquisa acessível e replicável. Validação com dados proprietários é extensão recomendada mas não essencial para framework metodológico.

**P: Os resultados são específicos à China?**  
R: A demonstração utiliza China como caso de estudo, mas metodologia é aplicável a qualquer contexto. Replicações em outras geografias são encorajadas.

**P: Quanto tempo demora para executar?**  
R: Pipeline completa em 5-10 minutos em computador padrão. Download de dados é a parte mais demorada (depende de conexão).

**P: Posso modificar o código?**  
R: Sim! Licença MIT permite modificação e redistribuição. Contribuições via pull request são bem-vindas.

---

**Última atualização:** Dezembro 2024  
**Versão:** 3.0 - Metodológica  
**Status:** ✅ Completo, Funcional e Replicável
