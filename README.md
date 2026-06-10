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

## Ferramentas complementares

### NavalForge Similar Vessels R0

Pasta: `tools/navalforge_similar_vessels_r0/`

Motor Python inicial para **benchmark preliminar por embarcações semelhantes**. Ele lê uma base `.xlsx` ou `.csv`, recebe um projeto-alvo e retorna:

- TOP N embarcações semelhantes;
- score de similaridade;
- faixas recomendadas;
- regressões preliminares;
- relatório em Markdown e JSON.

Nome funcional: **Dados de Embarcações Semelhantes R0**.

Uso rápido:

```bash
cd tools/navalforge_similar_vessels_r0
python -m navalforge_benchmark.cli \
  --input data/navalforge_embarcacoes_semelhantes_r0.csv \
  --target-json examples/projeto_alvo_dgs_frb_85m.json \
  --out-md outputs/relatorio_similar_vessels_r0.md
```

## Arquitetura

A arquitetura oficial agora é `src/navalforge/`. A estrutura antiga de pacote na raiz foi removida para evitar duplicidade.

Ferramentas experimentais e módulos auxiliares ficam em `tools/` até serem integrados oficialmente ao pacote principal.

## Validação

O projeto possui workflow de testes em `.github/workflows/tests.yml` para validar instalação e execução de `pytest`.
