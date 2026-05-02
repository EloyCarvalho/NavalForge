# NavalForge

**NavalForge** é um MVP técnico de engenharia naval, simulação preliminar e suporte à decisão para fase inicial de projeto de embarcações.

> Aviso: esta ferramenta é preliminar. Não substitui responsabilidade técnica, normas aplicáveis, cálculo completo, modelo 3D, CFD, FEA, ensaio ou prova de mar.

## Instalação

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
# source .venv/bin/activate
pip install -e .
```

## Rodar caso único

```bash
python examples/run_single_case.py
```

## Gerar variantes

```bash
python examples/run_variants.py
```

## Dashboard

```bash
python examples/generate_dashboard.py
```

## CLI

```bash
navalforge evaluate --name Lancha_12m --lwl 12 --beam 3.2 --draft 0.55 --speed 22 --html
navalforge variants --name Lancha_12m --lwl 12 --beam 3.2 --draft 0.55 --speed 22
navalforge save --name Lancha_12m --out data/projects/lancha_12m_saved.json
navalforge load-evaluate data/projects/lancha_12m.json
```

## Testes

```bash
pip install -e .[dev]
pytest
```

## O que foi implementado — níveis 2 a 10

Veja `docs/levels_2_to_10.md`.
