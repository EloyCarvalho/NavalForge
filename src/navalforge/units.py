from .constants import KNOT_TO_MS

def knots_to_ms(knots: float) -> float:
    return knots * KNOT_TO_MS

def ms_to_knots(ms: float) -> float:
    return ms / KNOT_TO_MS

def kg_to_tonnes(kg: float) -> float:
    return kg / 1000.0
