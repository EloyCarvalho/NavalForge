from __future__ import annotations
from pathlib import Path
import pandas as pd

def generate_html_dashboard(df: pd.DataFrame, output_path: str | Path = "reports/navalforge_dashboard.html") -> Path:
    p=Path(output_path); p.parent.mkdir(parents=True, exist_ok=True)
    top=df.head(20).copy()
    html=f"""<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>NavalForge Dashboard</title><style>body{{font-family:Arial;margin:32px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:8px}}th{{background:#eee}}</style></head><body><h1>NavalForge Dashboard</h1><p>Ranking preliminar de variantes. Não substitui validação técnica.</p>{top.to_html(index=False)}<h2>Limitação</h2><p>MVP preliminar. Savitsky atual é scaffold de triagem, não cálculo final validado.</p></body></html>"""
    p.write_text(html, encoding="utf-8")
    return p

def generate_power_curve_csv(df: pd.DataFrame, output_path: str | Path = "reports/power_curve.csv") -> Path:
    p=Path(output_path); p.parent.mkdir(parents=True, exist_ok=True)
    cols=[c for c in ["speed_knots","power_kw","score","status","regime"] if c in df.columns]
    df[cols].sort_values("speed_knots").to_csv(p, index=False)
    return p
