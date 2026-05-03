# NavalForge Validation Database v1

## Objetivo

Criar o primeiro banco de dados de validação do NavalForge com fontes reais rastreáveis.

Esta versão **não inventa resultados numéricos**. Ela registra fontes públicas e cria a estrutura para importar valores reais de resistência, hidrostática e estabilidade.

## Arquivos

```text
data/validation/reference_sources.json
data/validation/validation_cases_seed.json
src/navalforge/validation/database.py
examples/validation_database_demo.py
tests/test_validation_database.py
```

## Fontes reais registradas

### DSYHS 1981

**Geometry, resistance and stability of the Delft systematic yacht hull series**

Autores: J. Gerritsma, R. Onnink, A. Versluis.

Fonte original com resistência e estabilidade de 22 formas de casco sistematicamente variadas.

### TU Delft / 4TU dataset 2025

Dataset associado ao trabalho **Data-Driven Models for Yacht Hull Resistance Optimization**.

A descrição pública do dataset informa que contém dados de resistência hidrodinâmica, descritores geométricos, hidrostática, condições operacionais e resultados de resistência.

### DSYHS RAW coefficients 2022

Dataset de coeficientes RAW associado à Delft Systematic Yacht Hull Series. Útil para módulo futuro de resistência adicional em ondas.

## Status dos casos

Os casos atuais estão marcados como:

```text
metadata_only_pending_numeric_import
metadata_only_pending_dataset_download
```

Isso significa que eles **não devem ser usados ainda para aprovar/reprovar cálculo**.

## Próximo passo

A próxima etapa é importar os dados numéricos reais do dataset público para gerar casos como:

```json
{
  "case_id": "DSYHS_HULL_01_FN_030",
  "expected_results": {
    "resistance_n": 123.4
  },
  "tolerance_percent": 10.0
}
```

## Regra de confiança

Um método só deve ser considerado mais confiável quando:

1. o caso possuir fonte rastreável;
2. o dado numérico for importado sem alteração manual indevida;
3. o erro percentual estiver dentro da tolerância declarada;
4. o domínio de aplicação estiver explícito.
