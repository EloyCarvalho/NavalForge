from __future__ import annotations

from dataclasses import dataclass
import math

KNOT_TO_MPS = 0.514444
WATER_DENSITY = 1025.0  # kg/m^3 (sea water)
GRAVITY = 9.80665


@dataclass(slots=True)
class PlaningHullInput:
    """Inputs for a simplified Savitsky-like planing resistance estimation."""

    length_m: float
    beam_m: float
    speed_knots: float
    displacement_kg: float


class SavitskyModel:
    """Simplified hydrodynamic model for planing hull preliminary studies."""

    def __init__(self, hull_input: PlaningHullInput) -> None:
        self.hull_input = hull_input

    def compute(self) -> dict:
        speed_mps = self.hull_input.speed_knots * KNOT_TO_MPS
        wetted_area = 0.6 * self.hull_input.length_m * self.hull_input.beam_m

        dynamic_pressure = 0.5 * WATER_DENSITY * speed_mps**2
        lift_coeff = self.hull_input.displacement_kg * GRAVITY / (
            dynamic_pressure * wetted_area
        )

        trim_deg = max(2.0, min(7.0, 4.2 + 1.5 * (lift_coeff - 0.2)))

        froude_beam = speed_mps / math.sqrt(GRAVITY * self.hull_input.beam_m)
        resistance_coeff = 0.006 + 0.0015 * froude_beam

        resistance_n = resistance_coeff * dynamic_pressure * wetted_area
        effective_power_w = resistance_n * speed_mps
        shaft_power_w = effective_power_w / 0.62

        return {
            "speed_mps": speed_mps,
            "resistance_n": resistance_n,
            "power_kw": shaft_power_w / 1000.0,
            "trim_deg": trim_deg,
            "froude_beam": froude_beam,
        }
