from navalforge.hydrodynamics.savitsky import PlaningHullInput, SavitskyModel


def test_heavier_displacement_increases_hydrodynamic_outputs() -> None:
    light = PlaningHullInput(length_m=8.0, beam_m=2.6, speed_knots=28.0, displacement_kg=4922.0)
    heavy = PlaningHullInput(length_m=8.0, beam_m=2.6, speed_knots=28.0, displacement_kg=5430.0)

    model = SavitskyModel()
    light_result = model.compute(light)
    heavy_result = model.compute(heavy)

    assert heavy_result["lift_coeff"] > light_result["lift_coeff"]
    assert heavy_result["resistance_n"] > light_result["resistance_n"]
    assert heavy_result["effective_power_kw"] > light_result["effective_power_kw"]
