from pathlib import Path

from navalforge.io.sections_csv import load_sectional_hull_from_csv
from navalforge.resistance.savitsky_v1 import estimate_savitsky_v1
from navalforge.stability.gz_curve import approximate_gz_curve
from navalforge.validation.cases import ValidationCase, summarize_validation
from navalforge.interface.core_api import evaluate_from_csv_project
from navalforge.reporting.technical_report import technical_result_to_markdown
from navalforge.technical_core import TechnicalCoreResult

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "sections" / "lancha_12m_sections.csv"


def test_savitsky_v1_returns_positive_power():
    hull = load_sectional_hull_from_csv(CSV_PATH, name="Hull", waterline_z=0.55, vcg=1.10, speed_knots=22.0)
    result = estimate_savitsky_v1(hull)
    assert result.total_resistance_n > 0
    assert result.brake_power_kw > 0
    assert result.wetted_length_m > 0


def test_approximate_gz_curve_has_points():
    hull = load_sectional_hull_from_csv(CSV_PATH, name="Hull", waterline_z=0.55, vcg=1.10, speed_knots=22.0)
    result = approximate_gz_curve(hull)
    assert len(result.points) >= 5
    assert result.angle_at_max_gz_deg >= 0


def test_validation_summary():
    cases = [
        ValidationCase("demo", "displacement_kg", 100.0, 104.0, 5.0, "synthetic"),
        ValidationCase("demo_fail", "gm_initial_m", 1.0, 1.2, 5.0, "synthetic"),
    ]
    summary = summarize_validation(cases)
    assert summary["total_cases"] == 2
    assert summary["passed"] == 1


def test_interface_core_api():
    result = evaluate_from_csv_project(CSV_PATH, name="API_Hull", waterline_z=0.55, vcg=1.10, speed_knots=22.0)
    assert result["status"] == "preliminary_screening_only"
    assert result["core"]["hydrostatics"]["displacement_kg"] > 0
    assert result["speed_power_curve"]
    assert result["gz_curve"]["points"]
    assert result["savitsky_v1"]["brake_power_kw"] > 0


def test_report_markdown():
    result = evaluate_from_csv_project(CSV_PATH, name="Report_Hull", waterline_z=0.55, vcg=1.10, speed_knots=22.0)
    core = TechnicalCoreResult(**result["core"])
    md = technical_result_to_markdown(core)
    assert "NavalForge Technical Report" in md
    assert "Hydrostatics" in md
    assert "Limitations" in md
