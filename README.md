# NavalForge

**NavalForge** é um MVP técnico de engenharia naval, simulação preliminar e suporte à decisão para fase inicial de projeto de embarcações.

> Aviso: esta ferramenta é preliminar. Não substitui responsabilidade técnica, normas aplicáveis, cálculo completo, modelo 3D, CFD, FEA, ensaio ou prova de mar.

## Instalação

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

## Rodar

```bash
pytest
python examples/run_single_case.py
python examples/run_variants.py
python examples/generate_dashboard.py
```

## CLI

```bash
navalforge evaluate --name Lancha_12m --lwl 12 --beam 3.2 --draft 0.55 --speed 22 --html
navalforge variants --name Lancha_12m --lwl 12 --beam 3.2 --draft 0.55 --speed 22
navalforge save --name Lancha_12m --out data/projects/lancha_12m_saved.json
navalforge load-evaluate data/projects/lancha_12m.json
```

## Arquitetura

A arquitetura oficial agora é `src/navalforge/`. A estrutura antiga de pacote na raiz foi removida para evitar duplicidade.
