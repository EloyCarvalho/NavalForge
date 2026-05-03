from __future__ import annotations

from dataclasses import dataclass, asdict

from navalforge.geometry.sections import SectionalHull
from navalforge.hydrostatics.sectional import calculate_sectional_hydrostatics
from navalforge.stability.initial import evaluate_initial_stability
from navalforge.resistance.preliminary import estimate_sectional_resistance
from navalforge.propulsion.power import estimate_installed_power


@dataclass
class TechnicalCoreResult:
    hull_name: str
    hydrostatics: dict
    stability: dict
    resistance: dict
    installed_power: dict
    limitations: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate_technical_core(hull: SectionalHull, margin_factor: float = 1.15) -> TechnicalCoreResult:
    hydro = calculate_sectional_hydrostatics(hull)
    stability = evaluate_initial_stability(hull)
    resistance = estimate_sectional_resistance(hull)
    installed = estimate_installed_power(
        resistance.effective_power_kw,
        propulsive_efficiency=hull.propulsive_efficiency,
        margin_factor=margin_factor,
    )
    return TechnicalCoreResult(
        hull_name=hull.name,
        hydrostatics=hydro.to_dict(),
        stability=stability.to_dict(),
        resistance=resistance.to_dict(),
        installed_power=installed.to_dict(),
        limitations=[
            "Sectional geometry is preliminary unless imported/validated from CAD.",
            "Initial GM does not replace a full stability booklet or GZ curve.",
            "Resistance method is a screening bridge, not final Savitsky/Holtrop/CFD validation.",
            "Engineering decisions require applicable rules, loading conditions and professional review.",
        ],
    )
