from __future__ import annotations
from dataclasses import dataclass, asdict
from .constants import RHO_SEAWATER, G
from .hull import Hull

@dataclass
class HydrostaticsResult:
    volume_m3: float
    displacement_kg: float
    waterplane_area_m2: float
    midship_area_m2: float
    block_coefficient: float
    prismatic_coefficient: float
    waterplane_coefficient: float
    froude_number: float
    length_beam_ratio: float
    beam_draft_ratio: float

    def to_dict(self):
        return asdict(self)

def displaced_volume(hull: Hull) -> float:
    hull.validate()
    if hull.displacement_kg is not None:
        return hull.displacement_kg / RHO_SEAWATER
    return hull.lwl * hull.beam * hull.draft * hull.cb

def displacement_mass(hull: Hull, rho: float = RHO_SEAWATER) -> float:
    hull.validate()
    if hull.displacement_kg is not None:
        return hull.displacement_kg
    return displaced_volume(hull) * rho

def waterplane_area(hull: Hull) -> float:
    return hull.lwl * hull.beam * hull.cwp

def midship_area(hull: Hull) -> float:
    return hull.beam * hull.draft * (hull.cb / max(hull.cp, 1e-9))

def froude_number(hull: Hull) -> float:
    return hull.speed_ms / (G * hull.lwl) ** 0.5

def evaluate_hydrostatics(hull: Hull) -> HydrostaticsResult:
    return HydrostaticsResult(displaced_volume(hull), displacement_mass(hull), waterplane_area(hull), midship_area(hull), hull.cb, hull.cp, hull.cwp, froude_number(hull), hull.length_beam_ratio, hull.beam_draft_ratio)
