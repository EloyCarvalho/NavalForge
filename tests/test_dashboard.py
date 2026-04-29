from pathlib import Path

from navalforge.visualization.dashboard import (
    generate_speed_sweep_dashboard,
    generate_speed_sweep_svg,
)


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
    assert "Score Técnico" in html
    assert "Status" in html
    assert "Diagnóstico técnico" in html
    assert "Recomendações" in html
    assert "Aprovado com atenção" in html


def test_generate_svg_creates_file_and_core_tags(tmp_path: Path) -> None:
    output = tmp_path / "dashboard.svg"

    generated_path = generate_speed_sweep_svg(output_path=str(output))

    assert Path(generated_path).exists()
    svg = output.read_text(encoding="utf-8")
    assert "<svg" in svg
    assert "NavalForge — Dashboard Visual" in svg
    assert "Vista esquemática da embarcação" in svg
    assert "Vista lateral" in svg
    assert "Vista superior" in svg
    assert "L =" in svg
    assert "B =" in svg
    assert "18.0" in svg
    assert "36.0" in svg


def test_generate_svg_contains_custom_parameters(tmp_path: Path) -> None:
    output = tmp_path / "dashboard_custom.svg"

    generate_speed_sweep_svg(
        output_path=str(output),
        length_m=9.9,
        beam_m=3.1,
        target_speed_knots=30.0,
        passengers=10,
        fuel_capacity_l=410.0,
        material="aluminum",
        speed_start_knots=20.0,
        speed_end_knots=38.0,
        speed_step_knots=2.0,
    )

    svg = output.read_text(encoding="utf-8")
    assert "9.9 m" in svg
    assert "3.1 m" in svg
    assert "30.0 kn" in svg
    assert "Passageiros: 10" in svg
    assert "410.0 L" in svg
    assert "Material: aluminum" in svg
    assert "20.0 → 38.0 kn (passo 2.0)" in svg
