from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EngineeringDiagnostic:
    severity: str
    title: str
    message: str
    recommendation: str


def build_diagnostics(
    required_power_kw: float,
    trim_deg: float,
    warnings: list[str],
    target_speed_knots: float | None = None,
) -> list[EngineeringDiagnostic]:
    diagnostics: list[EngineeringDiagnostic] = []

    if required_power_kw < 300:
        diagnostics.append(
            EngineeringDiagnostic(
                severity="info",
                title="Potência em faixa moderada",
                message="A potência requerida está em faixa preliminarmente moderada para esta configuração.",
                recommendation="Manter análise e verificar margem de potência instalada.",
            )
        )
    elif required_power_kw <= 600:
        diagnostics.append(
            EngineeringDiagnostic(
                severity="warning",
                title="Potência elevada",
                message="A potência requerida já é relevante e pode impactar custo, peso e arranjo de máquinas.",
                recommendation="Avaliar redução de peso, ajuste de casco ou potência instalada.",
            )
        )
    else:
        diagnostics.append(
            EngineeringDiagnostic(
                severity="critical",
                title="Potência muito alta",
                message="A potência requerida ultrapassa o limite preliminar de alerta.",
                recommendation="Revisar velocidade alvo, deslocamento, forma do casco ou missão.",
            )
        )

    if trim_deg < 2.5:
        diagnostics.append(
            EngineeringDiagnostic(
                severity="warning",
                title="Trim baixo",
                message="O trim previsto está abaixo da faixa preferida.",
                recommendation="Avaliar LCG, geometria de fundo e condição de operação.",
            )
        )
    elif trim_deg <= 6.0:
        diagnostics.append(
            EngineeringDiagnostic(
                severity="info",
                title="Trim em faixa aceitável",
                message="O trim previsto está dentro da faixa preliminar preferida.",
                recommendation="Manter verificação em modelo físico mais refinado.",
            )
        )
    else:
        diagnostics.append(
            EngineeringDiagnostic(
                severity="critical",
                title="Trim elevado",
                message="O trim previsto está acima da faixa preferida.",
                recommendation="Avaliar LCG, deadrise, peso e velocidade alvo.",
            )
        )

    for warning in warnings:
        diagnostics.append(
            EngineeringDiagnostic(
                severity="warning",
                title="Alerta do modelo",
                message=warning,
                recommendation="Revisar os parâmetros associados ao alerta.",
            )
        )

    return diagnostics
