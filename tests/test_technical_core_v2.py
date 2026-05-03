from pathlib import Path

from navalforge.io.sections_csv import load_sectional_hull_from_csv, write_sectional_hull_to_csv
from navalforge.performance.speed_power import speed_power_curve, write_speed_power_csv
from navalforge.hydrostatics.sectional import calculate_sectional_hydrostatics

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "sections" / "lancha_12m_sections.csv"


def test_load_sectional_hull_from_csv():
    hull = load_sectional_hull_from_csv(
        CSV_PATH,
        name="Test_CSV_Hull",
        waterline_z=0.55,
        vcg=1.10,
        speed_knots=22.0,
    )
    assert hull.name == "Test_CSV_Hull"
    assert len(hull.sections) >= 5
    assert hull.lwl > 0
    assert hull.max_beam > 0


def test_csv_hydrostatics_positive():
    hull = load_sectional_hull_from_csv(
        CSV_PATH,
        name="Test_CSV_Hull",
        waterline_z=0.55,
        vcg=1.10,
        speed_knots=22.0,
    )
    hs = calculate_sectional_hydrostatics(hull)
    assert hs.volume_m3 > 0
    assert hs.displacement_kg > 0
    assert hs.waterplane_area_m2 > 0
    assert hs.gm_initial_m != 0


def test_write_sectional_hull_to_csv_roundtrip(tmp_path):
    hull = load_sectional_hull_from_csv(
        CSV_PATH,
        name="Roundtrip_Hull",
        waterline_z=0.55,
        vcg=1.10,
        speed_knots=22.0,
    )
    out = tmp_path / "roundtrip.csv"
    write_sectional_hull_to_csv(hull, out)
    loaded = load_sectional_hull_from_csv(
        out,
        name="Reloaded_Hull",
        waterline_z=0.55,
        vcg=1.10,
        speed_knots=22.0,
    )
    assert len(loaded.sections) == len(hull.sections)
    assert loaded.lwl == hull.lwl


def test_speed_power_curve_is_monotonic_enough():
    hull = load_sectional_hull_from_csv(
        CSV_PATH,
        name="SpeedPower_Hull",
        waterline_z=0.55,
        vcg=1.10,
        speed_knots=22.0,
    )
    points = speed_power_curve(hull, [6, 10, 14, 18, 22])
    assert len(points) == 5
    assert all(p.installed_power_kw >= 0 for p in points)
    assert points[-1].installed_power_kw > points[0].installed_power_kw


def test_write_speed_power_csv(tmp_path):
    hull = load_sectional_hull_from_csv(
        CSV_PATH,
        name="Export_Hull",
        waterline_z=0.55,
        vcg=1.10,
        speed_knots=22.0,
    )
    points = speed_power_curve(hull, [8, 12, 16])
    out = write_speed_power_csv(points, tmp_path / "speed_power.csv")
    assert out.exists()
    assert "speed_knots" in out.read_text(encoding="utf-8")
