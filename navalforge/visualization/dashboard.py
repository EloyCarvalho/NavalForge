from __future__ import annotations

from html import escape
from pathlib import Path

from navalforge.analysis import run_speed_sweep
from navalforge.pipeline.design_loop import DesignLoop, MissionInput


def _format_float(value: float) -> str:
    return f"{value:.1f}"


def generate_speed_sweep_dashboard(
    output_path: str = "reports/navalforge_dashboard.html",
    length_m: float = 8.0,
    beam_m: float = 2.6,
    target_speed_knots: float = 28.0,
    passengers: int = 6,
    fuel_capacity_l: float = 300.0,
    material: str = "fiberglass",
    speed_start_knots: float = 18.0,
    speed_end_knots: float = 36.0,
    speed_step_knots: float = 2.0,
) -> str:
    mission = MissionInput(
        length_m=length_m,
        beam_m=beam_m,
        target_speed_knots=target_speed_knots,
        passengers=passengers,
        fuel_capacity_l=fuel_capacity_l,
        material=material,
    )

    baseline_result = DesignLoop().run(mission)
    sweep_results = run_speed_sweep(
        base_mission=mission,
        speed_start_knots=speed_start_knots,
        speed_end_knots=speed_end_knots,
        speed_step_knots=speed_step_knots,
    )

    speeds = [item.speed_knots for item in sweep_results]
    power = [item.required_power_kw for item in sweep_results]
    resistance = [item.resistance_n for item in sweep_results]
    trim = [item.trim_deg for item in sweep_results]

    rows = "\n".join(
        (
            "<tr>"
            f"<td>{item.speed_knots:.1f}</td>"
            f"<td>{item.required_power_kw:.1f}</td>"
            f"<td>{item.resistance_n:.1f}</td>"
            f"<td>{item.trim_deg:.2f}</td>"
            f"<td>{escape('; '.join(item.warnings)) if item.warnings else '-'}</td>"
            "</tr>"
        )
        for item in sweep_results
    )

    html = f"""<!doctype html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>NavalForge Dashboard</title>
  <script src=\"https://cdn.plot.ly/plotly-2.35.2.min.js\"></script>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #0f172a; }}
    h1, h2 {{ margin: 0 0 12px 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(260px, 1fr)); gap: 12px; margin-bottom: 24px; }}
    .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; }}
    .stats {{ display: grid; grid-template-columns: repeat(3, minmax(180px, 1fr)); gap: 12px; margin-bottom: 18px; }}
    .stat {{ background: #eef2ff; border-radius: 8px; padding: 12px; }}
    .stat strong {{ display: block; font-size: 0.95rem; color: #334155; }}
    .stat span {{ font-size: 1.3rem; font-weight: 700; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 8px; text-align: left; font-size: 0.9rem; }}
    th {{ background: #e2e8f0; }}
    #chart {{ width: 100%; height: 560px; }}
  </style>
</head>
<body>
  <h1>NavalForge · Dashboard de Speed Sweep</h1>

  <h2>Missão de entrada</h2>
  <div class=\"grid\">
    <div class=\"card\"><strong>Comprimento:</strong> {_format_float(length_m)} m</div>
    <div class=\"card\"><strong>Boca:</strong> {_format_float(beam_m)} m</div>
    <div class=\"card\"><strong>Velocidade alvo:</strong> {_format_float(target_speed_knots)} kn</div>
    <div class=\"card\"><strong>Passageiros:</strong> {passengers}</div>
    <div class=\"card\"><strong>Combustível:</strong> {_format_float(fuel_capacity_l)} L</div>
    <div class=\"card\"><strong>Material:</strong> {escape(material)}</div>
    <div class=\"card\" style=\"grid-column: 1 / -1;\"><strong>Faixa do speed sweep:</strong>
      {_format_float(speed_start_knots)} a {_format_float(speed_end_knots)} kn (passo {_format_float(speed_step_knots)} kn)
    </div>
  </div>

  <h2>Resultado na velocidade alvo</h2>
  <div class=\"stats\">
    <div class=\"stat\"><strong>Deslocamento estimado</strong><span>{baseline_result['estimated_weight_kg']:.1f} kg</span></div>
    <div class=\"stat\"><strong>Resistência</strong><span>{baseline_result['resistance_n']:.1f} N</span></div>
    <div class=\"stat\"><strong>Potência requerida</strong><span>{baseline_result['power_kw']:.1f} kW</span></div>
  </div>

  <div id=\"chart\"></div>

  <h2>Tabela do sweep</h2>
  <table>
    <thead>
      <tr>
        <th>Velocidade (kn)</th>
        <th>Potência (kW)</th>
        <th>Resistência (N)</th>
        <th>Trim (deg)</th>
        <th>Warnings</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>

  <script>
    const speeds = {speeds};
    const power = {power};
    const resistance = {resistance};
    const trim = {trim};

    const traces = [
      {{ x: speeds, y: power, name: 'Power (kW)', type: 'scatter', mode: 'lines+markers', yaxis: 'y' }},
      {{ x: speeds, y: resistance, name: 'Resistance (N)', type: 'scatter', mode: 'lines+markers', yaxis: 'y2' }},
      {{ x: speeds, y: trim, name: 'Trim (deg)', type: 'scatter', mode: 'lines+markers', yaxis: 'y3' }},
    ];

    const layout = {{
      title: 'Speed Sweep',
      xaxis: {{ title: 'Velocidade (kn)' }},
      yaxis: {{ title: 'Potência (kW)' }},
      yaxis2: {{ title: 'Resistência (N)', overlaying: 'y', side: 'right' }},
      yaxis3: {{ title: 'Trim (deg)', anchor: 'free', overlaying: 'y', side: 'right', position: 0.95 }},
      legend: {{ orientation: 'h', y: 1.15 }},
      margin: {{ t: 60 }},
    }};

    Plotly.newPlot('chart', traces, layout, {{ responsive: true }});
  </script>
</body>
</html>
"""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return str(output)


def export_html_to_png(html_path: str, png_path: str) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Para exportar PNG, instale: pip install playwright && python -m playwright install chromium"
        )
        return False

    html_file = Path(html_path).resolve()
    png_file = Path(png_path)
    png_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1600, "height": 1000})
            page.goto(html_file.as_uri(), wait_until="networkidle")
            page.screenshot(path=str(png_file), full_page=True)
            browser.close()
        return True
    except Exception:
        return False
