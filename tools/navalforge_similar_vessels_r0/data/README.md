# Dados — Embarcações Semelhantes R0

Este diretório deve receber a base de dados exportada do Banco Geral de Embarcações NavalForge.

Arquivo sugerido:

- `navalforge_embarcacoes_semelhantes_r0.csv`

A planilha `.xlsx` completa continua sendo o artefato principal de trabalho. O CSV é recomendado para execução rápida do módulo Python.

## Escopo da base R0

- embarcações de aproximadamente 4 m a 20 m;
- uso preliminar para comparação de semelhantes;
- uso estatístico apenas com segmentação por grupo, material, propulsão e faixa de LOA.

## Observação técnica

A base foi construída com dados públicos de fabricantes, catálogos e páginas técnicas. Campos em branco indicam informação não encontrada ou não validada na fonte disponível.

Não usar como certificação, norma ou substituto de cálculo técnico.

## Como exportar

Na planilha principal do banco NavalForge, exporte a aba `Fichas_Reais_v31_v100` como CSV e salve neste diretório com o nome:

```text
navalforge_embarcacoes_semelhantes_r0.csv
```
