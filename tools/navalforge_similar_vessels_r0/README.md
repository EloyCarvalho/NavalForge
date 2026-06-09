# NavalForge Similar Vessels R0

Motor Python inicial para **benchmark preliminar por embarcações semelhantes** dentro do projeto NavalForge.

Esta release R0 nasceu a partir do Banco Geral de Embarcações NavalForge, usado para comparar embarcações reais de aproximadamente **4 m a 20 m** e apoiar estudos conceituais de arquitetura naval.

> Aviso técnico: esta ferramenta é preliminar. Não substitui responsabilidade técnica, norma aplicável, cálculo completo, modelo 3D, CFD, FEA, ensaio ou prova de mar.

## Objetivo

Responder, de forma estruturada:

> Tenho uma embarcação-alvo com determinado comprimento, boca, grupo, material e propulsão. Quais embarcações reais são mais semelhantes? Quais faixas preliminares de boca, peso, potência e combustível devo esperar?

## O que o módulo faz

- Lê banco NavalForge em `.xlsx` ou `.csv`;
- recebe um projeto-alvo em JSON ou Python;
- calcula score de semelhança;
- retorna TOP N embarcações semelhantes;
- calcula faixas recomendadas dos semelhantes;
- calcula regressão linear preliminar;
- gera relatório em Markdown e JSON.

## Nome da release

Nome técnico sugerido:

**`navalforge_similar_vessels_r0`**

Nome funcional em português:

**Dados de Embarcações Semelhantes R0**

## Estrutura

```text
tools/navalforge_similar_vessels_r0/
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── pyproject.toml
├── data/
│   └── README.md
├── examples/
│   ├── projeto_alvo_dgs_frb_85m.json
│   └── run_benchmark.py
└── navalforge_benchmark/
    ├── __init__.py
    ├── benchmark.py
    ├── cli.py
    ├── models.py
    ├── regression.py
    ├── similarity.py
    └── xlsx_reader.py
```

## Uso rápido

A partir desta pasta:

```bash
python -m navalforge_benchmark.cli \
  --input data/navalforge_embarcacoes_semelhantes_r0.csv \
  --target-json examples/projeto_alvo_dgs_frb_85m.json \
  --out-md outputs/relatorio_similar_vessels_r0.md \
  --out-json outputs/relatorio_similar_vessels_r0.json
```

Também funciona apontando para uma planilha `.xlsx` do banco NavalForge:

```bash
python -m navalforge_benchmark.cli \
  --input NavalForge_Banco_Geral_Embarcacoes_4a20m_v119_teste_real_aplicado_1000_fichas.xlsx \
  --sheet Fichas_Reais_v31_v100 \
  --target-json examples/projeto_alvo_dgs_frb_85m.json \
  --out-md outputs/relatorio_similar_vessels_r0.md
```

## Uso em Python

```python
from navalforge_benchmark import NavalForgeBenchmark, ProjectTarget

bench = NavalForgeBenchmark.from_xlsx("banco.xlsx")

target = ProjectTarget(
    nome="Lancha SAR 8,5 m",
    loa_m=8.50,
    b_m=2.80,
    grupo_navalforge="RIB / Inflável rígido",
    material_normalizado="RIB/GRP+tubo",
    propulsao_normalizada="motor de popa",
    regime_principal="Planante",
)

report = bench.benchmark_report(target, n=20)
print(bench.report_to_markdown(report))
```

## Critério de uso

Use para:

- benchmark preliminar;
- seleção de semelhantes;
- faixas de referência;
- apoio a estudos conceituais;
- preparação de estudos de pesos, centros, potência e arranjo.

Não use sozinho para:

- certificação;
- aprovação normativa;
- inferência global sem segmentação;
- substituição de cálculo naval completo;
- substituição da decisão técnica do engenheiro responsável.

## Próximas releases previstas

- R1: normalização de materiais e grupos, principalmente RIBs;
- R2: conexão com módulo de pesos e centros;
- R3: dashboard HTML/Plotly;
- R4: integração com `src/navalforge/`;
- R5: API local para NAVIA/NavalForge.
