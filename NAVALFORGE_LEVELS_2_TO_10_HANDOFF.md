# NavalForge — Handoff técnico dos níveis 2 a 10

Este arquivo registra a entrega gerada pelo EloyBot Naval IA para evolução do NavalForge do nível 2 ao nível 10.

## Objetivo

Transformar o NavalForge em um MVP técnico organizado para engenharia naval preliminar, simulação, suporte à decisão e evolução com IA.

## Estrutura proposta

```text
src/navalforge/
├── methods/
│   ├── regime.py
│   ├── displacement.py
│   └── savitsky.py
├── io/
│   └── project_store.py
├── ai/
│   └── assistant_rules.py
├── hull.py
├── hydrostatics.py
├── stability.py
├── resistance.py
├── validation.py
├── evaluator.py
├── variants.py
├── reporting.py
├── dashboard.py
└── cli.py

examples/
├── run_single_case.py
├── run_variants.py
├── generate_dashboard.py
└── batch_from_json.py

tests/
└── test_basic.py

docs/
├── levels_2_to_10.md
├── concept.md
├── technical_limits.md
└── roadmap.md
```

## Níveis implementados no pacote local

### Nível 2 — Métodos navais separados
- Classificação de regime por Froude.
- Método preliminar deslocante.
- Scaffold responsável para triagem planante/Savitsky.

### Nível 3 — Validação técnica
- Checagem de dimensões básicas.
- Avisos para razão L/B, B/T, coeficientes e velocidade.

### Nível 4 — Avaliador técnico
- Score preliminar.
- Status: aprovado, aprovado com atenção, atenção ou reprovado.
- Recomendações automáticas.

### Nível 5 — Variantes
- Geração de variações de boca, calado e velocidade.
- Exportação para CSV.

### Nível 6 — Relatórios
- Relatório Markdown.
- Relatório HTML.
- Ressalvas técnicas explícitas.

### Nível 7 — Dashboard
- Dashboard HTML simples.
- Visualização de tabela e resultados principais.

### Nível 8 — Persistência
- Leitura e gravação de projetos em JSON.

### Nível 9 — CLI
- `evaluate`
- `variants`
- `save`
- `load-evaluate`

### Nível 10 — Base para IA técnica
- Regras para assistente técnico.
- Roadmap para acoplar LLM sem substituir responsabilidade técnica.

## Ressalva técnica

O módulo `savitsky.py` entregue no pacote é um scaffold de triagem preliminar, não uma implementação final validada do método de Savitsky. Ele serve para estruturar a arquitetura e preparar a evolução técnica do NavalForge.

## Comandos previstos

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
python examples/run_single_case.py
python examples/run_variants.py
python examples/generate_dashboard.py
pytest
```

## Próximo commit recomendado

Adicionar os arquivos completos do pacote gerado localmente:

```bash
git checkout eloybot/navalforge-levels-2-to-10
git add .
git commit -m "Upgrade NavalForge levels 2 to 10"
git push
```

## Observação operacional

O pacote ZIP completo foi gerado no ambiente local da conversa como `navalforge_project_levels_2_to_10.zip`. A integração atual do GitHub no ChatGPT permitiu criar branch, arquivo e PR, mas não expôs upload direto de ZIP/árvore completa em um único comando estável nesta execução.
