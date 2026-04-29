from __future__ import annotations

from dataclasses import dataclass

from navalforge.evaluation import evaluate_design_result
from navalforge.hydrodynamics import PlaningHullInput, SavitskyModel

FUEL_DENSITY_KG_L = 0.74
PASSENGER_MASS_KG = 90.0


@dataclass(slots=True)
class MissionInput:
    length_m: float
    beam_m: float
    target_speed_knots: float
    passengers: int
    fuel_capacity_l: float
    material: str  # "fiberglass", "aluminum"


def estimate_weight(mission: MissionInput) -> float:
    """Estimate total displacement (kg) from mission-level inputs.

    This is a preliminary conceptual estimate for early design iterations.
    """

    material_factor = {
        "fiberglass": 1.0,
        "aluminum": 0.88,
    }
    factor = material_factor.get(mission.material.lower())
    if factor is None:
        raise ValueError("material must be 'fiberglass' or 'aluminum'")

    structural_base_kg = 520.0 * mission.length_m * factor
    passenger_weight_kg = mission.passengers * PASSENGER_MASS_KG
    fuel_weight_kg = mission.fuel_capacity_l * FUEL_DENSITY_KG_L

    return structural_base_kg + passenger_weight_kg + fuel_weight_kg


class DesignLoop:
    """First simplified engineering pipeline integrating mission, weight and hydrodynamics."""

    def run(self, mission: MissionInput) -> dict:
        estimated_weight_kg = estimate_weight(mission)

        hull_input = PlaningHullInput(
            length_m=mission.length_m,
            beam_m=mission.beam_m,
            speed_knots=mission.target_speed_knots,
            displacement_kg=estimated_weight_kg,
        )

        hydro_result = SavitskyModel(hull_input).compute()

        warnings: list[str] = []
        if hydro_result["power_kw"] > 600.0:
            warnings.append(
                "High installed power predicted (>600 kW). Review hull efficiency and mission targets."
            )

        trim = hydro_result["trim_deg"]
        if trim < 2.5 or trim > 6.0:
            warnings.append(
                f"Trim angle outside preferred range (2.5-6.0 deg): {trim:.2f} deg."
            )

        evaluation = evaluate_design_result(
            required_power_kw=hydro_result["power_kw"],
            trim_deg=trim,
            warnings=warnings,
            target_speed_knots=mission.target_speed_knots,
        )

        return {
            "estimated_weight_kg": estimated_weight_kg,
            "resistance_n": hydro_result["resistance_n"],
            "power_kw": hydro_result["power_kw"],
            "trim_deg": trim,
            "warnings": warnings,
            "score": evaluation.score,
            "status": evaluation.status,
            "status_label": evaluation.status_label,
            "evaluation_summary": evaluation.summary,
            "recommendations": evaluation.recommendations,
            "diagnostics": [
                {
                    "severity": diag.severity,
                    "title": diag.title,
                    "message": diag.message,
                    "recommendation": diag.recommendation,
                }
                for diag in evaluation.diagnostics
            ],
        }
