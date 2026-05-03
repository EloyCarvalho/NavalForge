from __future__ import annotations
from dataclasses import dataclass, asdict
from .hull import Hull
from .hydrostatics import displaced_volume

@dataclass
class StabilityResult:
    kb_m: float
    bm_transverse_m: float
    km_transverse_m: float
    gm_transverse_m: float
    roll_period_estimate_s: float | None
    status: str
    warning: str
    def to_dict(self): return asdict(self)

def estimate_initial_stability(hull: Hull) -> StabilityResult:
    hull.validate()
    vol = displaced_volume(hull)
    kb = 0.53 * hull.draft
    i_t = (hull.lwl * hull.beam**3 * hull.cwp) / 12.0
    bm = i_t / vol if vol > 0 else 0.0
    km = kb + bm
    gm = km - hull.vcg
    roll = 0.75 * hull.beam / (gm ** 0.5) if gm > 0 else None
    status = "CRITICAL" if gm <= 0 else ("LOW_MARGIN" if gm < 0.35 else "PRELIM_OK")
    return StabilityResult(kb, bm, km, gm, roll, status, "Estimativa inicial simplificada. Requer curvas hidrostáticas, GZ e critérios aplicáveis.")
