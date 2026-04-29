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
    deadrise_deg: float = 18.0
    lcg_from_transom_m: float | None = None


class SavitskyModel:
    """Simplified hydrodynamic model for planing hull preliminary studies."""

    def __init__(self, hull_input: PlaningHullInput | None = None) -> None:
        self.hull_input = hull_input

    def compute(self, hull_input: PlaningHullInput | None = None) -> dict:
        data = hull_input or self.hull_input
        if data is None:
            raise ValueError("SavitskyModel.compute() requires a PlaningHullInput.")

        speed_mps = data.speed_knots * KNOT_TO_MPS
        froude_beam = speed_mps / math.sqrt(GRAVITY * data.beam_m)

        lcg_ratio = (
            (data.lcg_from_transom_m / data.length_m)
            if data.lcg_from_transom_m is not None
            else 0.4
        )
        trim_deg = max(
            2.0,
            min(7.5, 3.4 + 0.75 * froude_beam + 0.02 * (data.deadrise_deg - 15.0) - 2.5 * (lcg_ratio - 0.4)),
        )

        wetted_length_ratio = max(0.45, min(0.92, 0.88 - 0.025 * trim_deg + 0.03 * (1.2 - froude_beam)))
        wetted_length_m = wetted_length_ratio * data.length_m
        wetted_area = wetted_length_m * data.beam_m

        dynamic_pressure = 0.5 * WATER_DENSITY * speed_mps**2
        lift_coeff = data.displacement_kg * GRAVITY / (dynamic_pressure * wetted_area)

        resistance_coeff = 0.0058 + 0.0015 * froude_beam + 0.00008 * data.deadrise_deg
        # Preliminary loading correction (still not a full Savitsky implementation):
        # - Increase drag sensitivity above a reference lift coefficient.
        # - Add a mild displacement scaling referenced to hull dimensions.
        reference_cl = 0.012
        lift_penalty_gain = 10.0
        load_factor = 1.0 + lift_penalty_gain * max(lift_coeff - reference_cl, 0.0)

        reference_displacement_kg = WATER_DENSITY * data.length_m * (data.beam_m**2) * 0.12
        displacement_factor = max(0.8, (data.displacement_kg / reference_displacement_kg) ** 0.25)

        resistance_n = (
            resistance_coeff
            * dynamic_pressure
            * wetted_area
            * load_factor
            * displacement_factor
        )

        effective_power_w = resistance_n * speed_mps
        shaft_power_w = effective_power_w / 0.62

        warnings: list[str] = []
        if froude_beam < 0.8:
            warnings.append("Low planing Froude number; regime may be semi-displacement.")
        if trim_deg >= 7.0:
            warnings.append("High trim angle predicted; verify longitudinal balance and appendages.")
        if not (0.08 <= lift_coeff <= 0.4):
            warnings.append("Lift coefficient outside typical preliminary Savitsky calibration range.")

        return {
            "speed_mps": speed_mps,
            "froude_beam": froude_beam,
            "froude_number": froude_beam,
            "trim_deg": trim_deg,
            "wetted_length_m": wetted_length_m,
            "lift_coeff": lift_coeff,
            "resistance_n": resistance_n,
            "effective_power_kw": effective_power_w / 1000.0,
            "power_kw": shaft_power_w / 1000.0,
            "warnings": warnings,
        }
