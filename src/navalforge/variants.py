from __future__ import annotations
from dataclasses import replace
from typing import Iterable
import pandas as pd
from .hull import Hull
from .evaluator import evaluate_hull

def generate_variants(base_hull: Hull, beam_values: Iterable[float], draft_values: Iterable[float], speed_values: Iterable[float], deadrise_values: Iterable[float] | None = None) -> list[Hull]:
    variants=[]; idx=1
    deadrise_values = list(deadrise_values) if deadrise_values is not None else [base_hull.deadrise_deg]
    for b in beam_values:
        for t in draft_values:
            for v in speed_values:
                for beta in deadrise_values:
                    variants.append(replace(base_hull, name=f"{base_hull.name}_V{idx:03d}", beam=b, draft=t, speed_knots=v, deadrise_deg=beta))
                    idx += 1
    return variants

def evaluate_variants(variants: list[Hull], resistance_method: str = "auto") -> pd.DataFrame:
    rows=[]
    for h in variants:
        r=evaluate_hull(h, resistance_method=resistance_method)
        rows.append({"name": h.name, "lwl_m": h.lwl, "beam_m": h.beam, "draft_m": h.draft, "deadrise_deg": h.deadrise_deg, "speed_knots": h.speed_knots, "disp_kg": r.hydrostatics["displacement_kg"], "fn": r.hydrostatics["froude_number"], "regime": r.resistance["regime"], "gm_m": r.stability["gm_transverse_m"], "power_kw": r.resistance["brake_power_kw"], "score": r.score, "status": r.status, "method": r.resistance["method"]})
    return pd.DataFrame(rows).sort_values(["score","power_kw"], ascending=[False, True])
