from pathlib import Path

from navalforge.visualization.dashboard import generate_speed_sweep_dashboard


def test_generate_dashboard_creates_html(tmp_path: Path) -> None:
    output = tmp_path / "dashboard.html"

    generated_path = generate_speed_sweep_dashboard(output_path=str(output))

    assert Path(generated_path).exists()


def test_generate_dashboard_contains_custom_inputs(tmp_path: Path) -> None:
    output = tmp_path / "dashboard_custom.html"

    generate_speed_sweep_dashboard(
        output_path=str(output),
        length_m=9.5,
        beam_m=2.9,
        target_speed_knots=31.0,
        passengers=8,
        fuel_capacity_l=420.0,
        material="aluminum",
        speed_start_knots=16.0,
        speed_end_knots=34.0,
        speed_step_knots=3.0,
    )

    html = output.read_text(encoding="utf-8")

    assert "Missão de entrada" in html
    assert "9.5 m" in html
    assert "2.9 m" in html
    assert "31.0 kn" in html
    assert "8" in html
    assert "420.0 L" in html
    assert "aluminum" in html
    assert "16.0 a 34.0 kn (passo 3.0 kn)" in html
