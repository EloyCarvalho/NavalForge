from navalforge.geometry.sections import create_simple_planing_hull
from navalforge.hydrostatics.sectional import calculate_sectional_hydrostatics
from navalforge.stability.initial import evaluate_initial_stability
from navalforge.resistance.preliminary import estimate_sectional_resistance
from navalforge.technical_core import evaluate_technical_core


def test_sectional_hydrostatics_positive():
    hull = create_simple_planing_hull(stations=11)
    result = calculate_sectional_hydrostatics(hull)
    assert result.volume_m3 > 0
    assert result.displacement_kg > 0
    assert result.waterplane_area_m2 > 0
    assert result.waterplane_it_m4 > 0
    assert result.froude_number > 0


def test_initial_stability_result():
    hull = create_simple_planing_hull(stations=11)
    result = evaluate_initial_stability(hull)
    assert result.kmt_m > result.kb_m
    assert result.status in {"PRELIM_OK", "LOW_MARGIN", "CRITICAL"}


def test_sectional_resistance_result():
    hull = create_simple_planing_hull(stations=11)
    result = estimate_sectional_resistance(hull)
    assert result.total_resistance_n > 0
    assert result.effective_power_kw > 0
    assert result.brake_power_kw > 0
    assert result.regime in {"DISPLACEMENT", "SEMI_DISPLACEMENT", "PLANING"}


def test_technical_core_evaluation():
    hull = create_simple_planing_hull(stations=13)
    result = evaluate_technical_core(hull)
    assert result.hydrostatics["displacement_kg"] > 0
    assert result.resistance["total_resistance_n"] > 0
    assert result.installed_power["installed_power_kw"] >= result.installed_power["brake_power_kw"]
    assert result.limitations
