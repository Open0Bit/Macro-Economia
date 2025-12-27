# Assimetria Macro: Estresse Financeiro e Fluxos Institucionais

**Autor:** Gabriel W. Soares  
**Status:** ✅ Concluído (Resultados Disponíveis)

Este framework analisa a relação de causalidade (**Lead-Lag**) e contágio (**Sincronização**) entre o estresse financeiro sistêmico da China e o posicionamento de investidores institucionais via ETFs globais.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📊 Principais Descobertas (Tese)

A aplicação deste framework revelou padrões estatísticos importantes sobre o risco sistêmico chinês (Baseado em dados de 2015-2024):

1.  **O Círculo Vicioso (Feedback Loop):**
    * Testes de Causalidade de Granger confirmaram que para *Large Caps* (FXI), o estresse financeiro causa saída de capital (p=0.0004), mas a saída de capital *também* retroalimenta o estresse (p=0.0003). Não há um "líder" claro; é um sistema reflexivo perigoso.
    
2.  **Divergência Setorial em Crises (Desacoplamento):**
    * Ao contrário do esperado, durante picos de estresse, houve uma **queda na correlação** entre o setor de Tecnologia (KWEB) e o mercado amplo (FXI). Enquanto o mercado geral reage ao pânico, Tech segue dinâmicas próprias, sugerindo que investidores tratam risco regulatório (Tech) de forma distinta de risco macroeconômico.

3.  **Estabilidade Regional:**
    * A análise de sincronização mostrou que a correlação entre China e Índia permanece estável mesmo em crises, sugerindo que a Índia ainda não atua como um hedge automático perfeito (substituto imediato) em momentos de pânico agudo.

---

## 🚀 Como Reproduzir a Análise (Automação)

Este projeto conta com um **Setup Automatizado** que configura o ambiente e um **Orquestrador** que roda toda a pipeline.

### 1. Instalação Rápida
```bash
git clone https://github.com/Open0Bit/Macro-Economia.git
cd Macro-Economia/Assimetria-Macro
python setup.py