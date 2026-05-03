# NavalForge Technical Core v1

## Objetivo

Criar a primeira base técnica do NavalForge para evoluir de protótipo visual para motor naval validável.

Esta versão introduz cálculos por seções transversais, em vez de depender apenas de fórmulas globais como `L × B × T × Cb`.

## Módulos incluídos

```text
src/navalforge/geometry/sections.py
src/navalforge/hydrostatics/sectional.py
src/navalforge/stability/initial.py
src/navalforge/resistance/preliminary.py
src/navalforge/propulsion/power.py
src/navalforge/technical_core.py
```

## O que calcula

### Geometria

- casco simétrico por seções;
- pontos por meia-seção;
- interpolação de boca imersa por altura;
- área imersa da seção;
- centro vertical da seção.

### Hidrostática

- volume deslocado;
- deslocamento;
- LCB;
- KB;
- área do plano d’água;
- LCF;
- momento transversal do plano d’água;
- BMt;
- KMt;
- GMt inicial;
- Froude;
- Cb e Cwp derivados da geometria.

### Estabilidade inicial

- KB;
- BMt;
- KMt;
- GMt;
- status preliminar.

### Resistência preliminar

- área molhada aproximada por seções;
- Reynolds;
- coeficiente friccional ITTC-1957;
- coeficiente residual preliminar;
- resistência total preliminar;
- potência efetiva;
- potência de eixo.

### Propulsão

- potência efetiva;
- potência de eixo;
- potência instalada com margem.

## Limitações

Esta versão ainda não substitui:

- Orca3D;
- Rhino;
- curvas hidrostáticas reais de CAD;
- curva GZ completa;
- Savitsky validado;
- Holtrop-Mennen validado;
- CFD;
- ensaio de tanque;
- prova de mar;
- responsabilidade técnica.

## Próximos passos técnicos

1. Importar seções reais de CSV/JSON.
2. Implementar curva GZ aproximada por inclinação de seções.
3. Implementar Savitsky completo para casco planante.
4. Implementar curva velocidade × potência usando métodos selecionáveis.
5. Criar casos de validação com resultados conhecidos.
6. Gerar relatório técnico em Markdown/PDF.
