# NavalForge — Níveis 2 a 10 implementados no MVP

## Nível 2 — Métodos navais separados
- Regime: deslocante, semi-deslocante, planante.
- Método preliminar de deslocamento baseado em ITTC57 + coeficiente residual simplificado.
- Scaffold de Savitsky para triagem planante, explicitamente não validado como cálculo final.

## Nível 3 — Validação de dados
- Checagens de L/B, B/T, VCG, coeficientes e eficiência propulsiva.
- Alertas classificados em INFO, WARNING e ERROR.

## Nível 4 — Avaliador técnico
- Score preliminar.
- Status: PRELIM_OK, REVIEW_REQUIRED ou CRITICAL.
- Recomendações automáticas.

## Nível 5 — Variantes e exploração do espaço de projeto
- Geração de famílias de casco.
- Comparação por score e potência.
- Exportação CSV.

## Nível 6 — Relatórios
- Relatório Markdown.
- Relatório HTML.
- Limitações e ressalvas técnicas incluídas.

## Nível 7 — Dashboard
- Dashboard HTML com ranking das melhores variantes.
- CSV auxiliar para curva de potência.

## Nível 8 — Persistência de projetos
- Salvar e carregar casco em JSON.
- Exemplo em data/projects.

## Nível 9 — CLI profissional
- Comandos evaluate, variants, save e load-evaluate.
- Parâmetros técnicos via terminal.

## Nível 10 — Base para produto com IA
- Regras de assistente técnico.
- Estrutura pronta para interface Flet/NiceGUI/FastAPI.
- GitHub Actions e testes automatizados.
