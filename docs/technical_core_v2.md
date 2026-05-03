# NavalForge Technical Core v2

## Objetivo

A v2 avança o NavalForge para uma base mais confiável ao permitir importar geometrias por seções reais em CSV e gerar curvas velocidade × potência.

## Novos recursos

### 1. Importação de seções via CSV

Arquivo:

```text
src/navalforge/io/sections_csv.py
```

Formato esperado:

```csv
x,y,z
0.0,0.0,0.0
0.0,0.25,0.25
0.0,0.55,0.50
```

Onde:

- `x` = posição longitudinal da seção;
- `y` = meia-boca local;
- `z` = altura vertical a partir da linha de base.

A geometria é assumida simétrica em relação ao plano diametral.

### 2. Casco de exemplo

Arquivo:

```text
data/sections/lancha_12m_sections.csv
```

Este casco serve para teste e demonstração. Não representa uma geometria validada para projeto real.

### 3. Curva velocidade × potência

Arquivo:

```text
src/navalforge/performance/speed_power.py
```

Gera uma lista de pontos com:

- velocidade;
- número de Froude;
- regime;
- resistência;
- potência efetiva;
- potência de eixo;
- potência instalada.

### 4. Exportação CSV

A curva pode ser exportada para:

```text
reports/speed_power_curve_v2.csv
```

## Como rodar

```bash
python examples/sectional_csv_demo.py
python examples/speed_power_curve_demo.py
pytest
```

## Limitações

Esta v2 ainda é preliminar.

Não substitui:

- Orca3D;
- Rhino;
- Savitsky completo;
- Holtrop-Mennen;
- CFD;
- ensaio de tanque;
- curva GZ;
- prova de mar;
- responsabilidade técnica.

## Próximos passos rumo a confiabilidade

1. Criar formato JSON de projeto.
2. Implementar Savitsky completo para casco planante.
3. Implementar curva GZ aproximada.
4. Criar casos de validação com referência externa.
5. Criar relatórios técnicos rastreáveis.
