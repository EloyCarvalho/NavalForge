# NavalForge Technical Core v3 to v7

## Objetivo

Adicionar os blocos técnicos que aproximam o NavalForge de uma ferramenta naval validável.

## v3 — Savitsky v1 preliminar

Arquivo:

```text
src/navalforge/resistance/savitsky_v1.py
```

Inclui estimativa preliminar de:

- trim;
- comprimento molhado;
- área molhada;
- resistência total;
- potência efetiva;
- potência de eixo.

Ainda não é um Savitsky completo validado.

## v4 — Curva GZ aproximada

Arquivo:

```text
src/navalforge/stability/gz_curve.py
```

Inclui uma curva GZ aproximada a partir do GM inicial.

Não substitui cálculo de estabilidade real por geometria inclinada.

## v5 — Validação

Arquivo:

```text
src/navalforge/validation/cases.py
```

Cria estrutura para comparar resultados calculados contra referências externas.

## v6 — Relatório técnico

Arquivo:

```text
src/navalforge/reporting/technical_report.py
```

Gera relatório Markdown rastreável com:

- hidrostática;
- estabilidade inicial;
- resistência;
- potência;
- limitações;
- validações requeridas.

## v7 — API para interface

Arquivo:

```text
src/navalforge/interface/core_api.py
```

Cria uma função de alto nível para a interface/web app consumir o núcleo técnico.

## Como rodar

```bash
python examples/technical_v3_to_v7_demo.py
pytest
```

## Limite de confiança

Esta etapa melhora a arquitetura e a rastreabilidade, mas o NavalForge ainda não deve ser tratado como equivalente ao Orca3D.

Para avançar em confiabilidade real, faltam:

1. validação contra casos publicados;
2. importação de geometria real de CAD;
3. Savitsky completo com iteração validada;
4. curva GZ por geometria inclinada;
5. comparação sistemática com softwares de referência;
6. calibração por prova de mar ou ensaio.
