from __future__ import annotations

def classify_regime(froude_number: float) -> str:
    if froude_number < 0.35:
        return "DISPLACEMENT"
    if froude_number < 0.75:
        return "SEMI_DISPLACEMENT"
    return "PLANING"
