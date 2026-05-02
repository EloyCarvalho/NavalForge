from __future__ import annotations
from dataclasses import dataclass, asdict
from math import radians, tan, cos
from navalforge.constants import RHO_SEAWATER, G
from navalforge.hull import Hull
from navalforge.hydrostatics import displacement_mass

@dataclass
class SavitskyScreeningResult:
    lift_coefficient: float
    beam_loading: float
    assumed_trim_deg: float
    wetted_length_beam_ratio: float
    wetted_area_m2: float
    resistance_n: float
    effective_power_kw: float
    brake_power_kw: float
    method: str
    warning: str
    def to_dict(self): return asdict(self)

def savitsky_screening(hull: Hull, trim_deg: float | None = None) -> SavitskyScreeningResult:
    """Planing-craft screening inspired by Savitsky variables.

    IMPORTANT: This is not a full validated Savitsky implementation.
    Use as software scaffold and relative comparison only.
    """
    hull.validate()
    beta = radians(hull.deadrise_deg)
    tau_deg = trim_deg if trim_deg is not None else (hull.trim_deg if hull.trim_deg is not None else 4.0)
    tau = radians(tau_deg)
    b = hull.effective_chine_beam
    v = max(hull.speed_ms, 0.01)
    weight_n = displacement_mass(hull) * G
    beam_loading = weight_n / (RHO_SEAWATER * G * b**3)
    cl_beta = weight_n / (0.5 * RHO_SEAWATER * v**2 * b**2)
    lambda_ratio = max(0.8, min(5.0, 1.2 + 1.8 * beam_loading / max(tan(tau), 0.05)))
    wetted_area = lambda_ratio * b**2 / max(cos(beta), 0.1)
    pressure_drag = weight_n * tan(tau)
    friction_drag = 0.0045 * 0.5 * RHO_SEAWATER * v**2 * wetted_area
    deadrise_penalty = 1.0 + 0.01 * max(hull.deadrise_deg - 12.0, 0.0)
    resistance = (pressure_drag + friction_drag) * deadrise_penalty
    pe = resistance * v / 1000.0
    pb = pe / hull.propulsive_efficiency
    return SavitskyScreeningResult(cl_beta, beam_loading, tau_deg, lambda_ratio, wetted_area, resistance, pe, pb, "savitsky_screening_scaffold_not_full_validation", "Triagem inspirada em variáveis de Savitsky. Não usar como cálculo final sem implementação validada e comparação técnica.")
