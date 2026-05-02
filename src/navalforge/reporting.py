from __future__ import annotations
from pathlib import Path
from .evaluator import EvaluationResult

def write_markdown_report(result: EvaluationResult, output_path: str | Path) -> Path:
    p=Path(output_path); p.parent.mkdir(parents=True, exist_ok=True)
    h=result.hull; hydro=result.hydrostatics; stab=result.stability; res=result.resistance
    lines=[f"# NavalForge Preliminary Report — {h['name']}","",f"Status: **{result.status}**",f"Score: **{result.score:.1f}/100**","","## Dados principais",f"- LWL: {h['lwl']} m",f"- Boca: {h['beam']} m",f"- Calado: {h['draft']} m",f"- Velocidade: {h['speed_knots']} kn","","## Hidrostática",f"- Deslocamento: {hydro['displacement_kg']:.1f} kg",f"- Froude: {hydro['froude_number']:.3f}","","## Estabilidade inicial",f"- GMt preliminar: {stab['gm_transverse_m']:.3f} m",f"- Status: {stab['status']}","","## Resistência e potência",f"- Regime: {res['regime']}",f"- Método: {res['method']}",f"- Resistência: {res['estimated_resistance_n']:.1f} N",f"- Potência estimada: {res['brake_power_kw']:.1f} kW",f"- Aviso: {res['warning']}","","## Recomendações",*[f"- {x}" for x in result.recommendations],"","## Limitações",*[f"- {x}" for x in result.limitations]]
    p.write_text("\n".join(lines), encoding="utf-8")
    return p

def write_html_report(result: EvaluationResult, output_path: str | Path) -> Path:
    md_path = Path(output_path).with_suffix(".md")
    md = write_markdown_report(result, md_path).read_text(encoding="utf-8")
    html = "<html><head><meta charset='utf-8'><title>NavalForge Report</title><style>body{font-family:Arial;margin:40px;max-width:960px}h1,h2{color:#111827}</style></head><body>"
    for line in md.splitlines():
        if line.startswith("# "): html += f"<h1>{line[2:]}</h1>"
        elif line.startswith("## "): html += f"<h2>{line[3:]}</h2>"
        elif line.startswith("- "): html += f"<p>• {line[2:]}</p>"
        elif line.strip(): html += f"<p>{line}</p>"
        else: html += "<br>"
    html += "</body></html>"
    p=Path(output_path); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(html, encoding="utf-8"); return p
