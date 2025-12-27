# Documentacao dos Dados

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
