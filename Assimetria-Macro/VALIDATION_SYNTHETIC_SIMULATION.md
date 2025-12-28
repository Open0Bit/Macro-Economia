# Validação por Simulação Sintética

Este documento descreve a estratégia de **validação por simulação sintética** do framework de Preparação Assimétrica, com o objetivo de avaliar sua **consistência interna, capacidade de detecção de padrões conhecidos e resistência a falsos positivos** em ambientes controlados.

A simulação sintética permite testar o comportamento do framework em cenários nos quais a estrutura subjacente dos dados é conhecida, reduzindo ambiguidades interpretativas presentes em dados reais.

---

## 1. Objetivo da Simulação Sintética

O principal objetivo desta validação é verificar se o framework:
- Identifica corretamente **assimetrias temporais induzidas artificialmente**
- Responde de forma consistente a **mudanças controladas de regime**
- Não gera sinais espúrios na ausência de estrutura sistêmica real

Essa abordagem permite separar **capacidade metodológica** de **contingência empírica**.

---

## 2. Construção dos Dados Sintéticos

Os dados sintéticos são gerados de forma a reproduzir propriedades estilizadas observadas em séries macroeconômicas e financeiras, incluindo:
- Tendências estocásticas
- Volatilidade variável
- Correlações dinâmicas
- Mudanças estruturais controladas

### 2.1 Estrutura Básica

São consideradas múltiplas séries temporais sintéticas representando setores ou ativos, construídas a partir de:
- Processos autoregressivos (AR)
- Componentes de ruído branco e ruído correlacionado
- Defasagens temporais conhecidas entre grupos de séries

---

### 2.2 Introdução de Assimetria Temporal

Para testar a capacidade de detecção do framework, são introduzidas:
- Defasagens temporais deliberadas entre subconjuntos de séries
- Choques exógenos simulados com impacto diferenciado no tempo
- Períodos de sincronização seguidos de dessicronização

Essas assimetrias são conhecidas *a priori*, permitindo validação direta dos resultados.

---

## 3. Metodologia de Validação

A validação sintética segue os seguintes passos:

1. Geração de múltiplos cenários sintéticos com parâmetros variados  
2. Aplicação integral do pipeline do framework em cada cenário  
3. Comparação entre padrões detectados e estruturas simuladas  
4. Avaliação da taxa de detecção correta e de falsos positivos  

A análise é conduzida de forma repetida para garantir **robustez estatística**.

---

## 4. Critérios de Avaliação

O desempenho do framework é avaliado com base nos seguintes critérios:

- **Consistência interna**: estabilidade dos resultados sob variação controlada de parâmetros  
- **Capacidade de detecção**: identificação correta de assimetrias conhecidas  
- **Especificidade**: ausência de sinais relevantes quando nenhuma estrutura assimétrica é introduzida  
- **Sensibilidade a regimes**: resposta adequada a mudanças estruturais simuladas  

Esses critérios permitem avaliar o equilíbrio entre sensibilidade e robustez do framework.

---

## 5. Interpretação dos Resultados

Os resultados da simulação sintética devem ser interpretados como:

- Evidência de que o framework responde a **estruturas temporais reais**, e não a ruído aleatório  
- Confirmação de que sinais de preparação assimétrica emergem apenas sob condições sistêmicas específicas  
- Indicação de que o modelo possui **capacidade discriminatória** entre regimes sincronizados e dessicronizados  

A ausência de detecção em cenários sem assimetria é considerada um resultado positivo.

---

## 6. Limitações da Simulação Sintética

Apesar de sua utilidade, a simulação sintética apresenta limitações inerentes:
- Simplificação da complexidade econômica real
- Ausência de instituições, políticas e expectativas adaptativas completas
- Dependência da escolha dos processos geradores de dados

Por esse motivo, os resultados sintéticos **complementam, mas não substituem**, validações empíricas com dados reais.

---

## 7. Implicações Metodológicas

A validação por simulação sintética reforça que:
- O framework possui coerência lógica e estatística
- Seus sinais não são artefatos aleatórios
- A detecção de preparação assimétrica depende de estruturas temporais reais

Esse tipo de validação é particularmente relevante para avaliações acadêmicas e institucionais, nas quais a distinção entre sinal e ruído é crítica.

---

## 8. Síntese

A validação por simulação sintética demonstra que o framework de Preparação Assimétrica:
- Detecta assimetrias temporais quando elas existem
- Mantém comportamento estável sob variações controladas
- Evita geração sistemática de falsos positivos

Esses resultados fortalecem a credibilidade metodológica do framework e ampliam sua aceitação científica e institucional.
