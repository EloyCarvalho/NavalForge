from __future__ import annotations
from dataclasses import dataclass, asdict
from math import log10
from navalforge.constants import RHO_SEAWATER
from navalforge.hull import Hull

@dataclass
class DisplacementResistanceResult:
    reynolds_number: float
    friction_coefficient: float
    wetted_area_m2: float
    resistance_n: float
    effective_power_kw: float
    brake_power_kw: float
    method: str
    warning: str
    def to_dict(self): return asdict(self)

def estimate_wetted_area(hull: Hull) -> float:
    return hull.lwl * (2.0 * hull.draft + hull.beam) * 0.85 * hull.appendage_factor

def ittc57_cf(speed_ms: float, length_m: float, nu: float = 1.188e-6) -> float:
    re = max(speed_ms * length_m / nu, 1.0)
    return 0.075 / ((log10(re) - 2.0) ** 2)

def estimate_displacement_resistance(hull: Hull, form_factor: float = 1.25, residual_coeff: float = 0.0018) -> DisplacementResistanceResult:
    hull.validate()
    s = estimate_wetted_area(hull)
    cf = ittc57_cf(max(hull.speed_ms, 0.01), hull.lwl)
    re = max(hull.speed_ms * hull.lwl / 1.188e-6, 1.0)
    ct = form_factor * cf + residual_coeff
    r = 0.5 * RHO_SEAWATER * hull.speed_ms**2 * s * ct
    pe = r * hull.speed_ms / 1000.0
    pb = pe / hull.propulsive_efficiency
    return DisplacementResistanceResult(re, cf, s, r, pe, pb, "ITTC57_plus_preliminary_residual_coefficient", "Modelo preliminar de deslocamento; não substitui Holtrop-Mennen, CFD, ensaio ou prova de mar.")
