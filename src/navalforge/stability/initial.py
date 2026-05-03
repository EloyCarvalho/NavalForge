from __future__ import annotations

from dataclasses import dataclass, asdict

from navalforge.geometry.sections import SectionalHull
from navalforge.hydrostatics.sectional import calculate_sectional_hydrostatics


@dataclass
class InitialStabilityResult:
    kb_m: float
    bmt_m: float
    kmt_m: float
    vcg_m: float
    gm_initial_m: float
    status: str
    warning: str

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate_initial_stability(hull: SectionalHull) -> InitialStabilityResult:
    hs = calculate_sectional_hydrostatics(hull)
    gm = hs.gm_initial_m
    status = "CRITICAL" if gm <= 0 else ("LOW_MARGIN" if gm < 0.35 else "PRELIM_OK")
    return InitialStabilityResult(
        kb_m=hs.kb_m,
        bmt_m=hs.bmt_m,
        kmt_m=hs.kmt_m,
        vcg_m=hull.vcg,
        gm_initial_m=gm,
        status=status,
        warning="Initial GM only. A real stability study requires loading conditions, free surface effects and GZ curves.",
    )
