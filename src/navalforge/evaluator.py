from __future__ import annotations
from dataclasses import dataclass, asdict
from .hull import Hull
from .hydrostatics import evaluate_hydrostatics
from .stability import estimate_initial_stability
from .resistance import estimate_resistance
from .validation import validate_design_inputs

@dataclass
class EvaluationResult:
    hull: dict
    hydrostatics: dict
    stability: dict
    resistance: dict
    validation: list[dict]
    score: float
    status: str
    recommendations: list[str]
    limitations: list[str]
    def to_dict(self): return asdict(self)

def evaluate_hull(hull: Hull, resistance_method: str = "auto") -> EvaluationResult:
    issues = validate_design_inputs(hull)
    hydro = evaluate_hydrostatics(hull).to_dict()
    stab = estimate_initial_stability(hull).to_dict()
    res = estimate_resistance(hull, resistance_method).to_dict()
    score = 100.0
    recs: list[str] = []
    if any(i.level == "ERROR" for i in issues):
        score -= 60; recs.append("Corrigir erros de entrada antes de qualquer conclusão técnica.")
    if stab["status"] == "CRITICAL":
        score -= 45; recs.append("Estabilidade inicial crítica: revisar VCG, boca, calado e arranjo de pesos.")
    elif stab["status"] == "LOW_MARGIN":
        score -= 20; recs.append("Margem de GM baixa: calcular curvas GZ e revisar pesos.")
    if res["brake_power_kw"] > 600:
        score -= 15; recs.append("Potência preliminar elevada; revisar velocidade-alvo, forma do casco e eficiência propulsiva.")
    if res["regime"] == "PLANING" and "not_full_validation" in res["method"]:
        score -= 10; recs.append("Para casco planante, implementar Savitsky completo antes de decisão final.")
    score = max(0.0, min(100.0, score))
    status = "PRELIM_OK" if score >= 75 else ("REVIEW_REQUIRED" if score >= 45 else "CRITICAL")
    limitations = [
        "Modelo preliminar para triagem de conceito.",
        "Não substitui normas, responsabilidade técnica, modelo 3D, curvas hidrostáticas reais, CFD, FEA, ensaio ou prova de mar.",
        "Savitsky atual é scaffold de triagem, não implementação final validada.",
    ]
    return EvaluationResult(hull.to_dict(), hydro, stab, res, [i.to_dict() for i in issues], score, status, recs or ["Prosseguir para refinamento com dados de pesos, geometria 3D e critérios aplicáveis."], limitations)
