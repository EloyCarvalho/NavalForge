from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional
import statistics

from .models import ProjectTarget
from .regression import linear_regression
from .similarity import SimilarityConfig, compute_similarity, to_float
from .xlsx_reader import read_csv, read_xlsx_sheet

DEFAULT_SHEET = "Fichas_Reais_v31_v100"


def _percentile(sorted_values: List[float], p: float) -> Optional[float]:
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]
    k = (len(sorted_values) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_values) - 1)
    if f == c:
        return sorted_values[f]
    return sorted_values[f] + (sorted_values[c] - sorted_values[f]) * (k - f)


class NavalForgeBenchmark:
    """Motor de benchmark por embarcações semelhantes."""

    def __init__(self, records: List[Dict[str, Any]], config: SimilarityConfig | None = None):
        self.records = records
        self.config = config or SimilarityConfig()

    @classmethod
    def from_xlsx(cls, path: str | Path, sheet_name: str = DEFAULT_SHEET) -> "NavalForgeBenchmark":
        return cls(read_xlsx_sheet(path, sheet_name))

    @classmethod
    def from_csv(cls, path: str | Path) -> "NavalForgeBenchmark":
        return cls(read_csv(path))

    @classmethod
    def from_file(cls, path: str | Path, sheet_name: str = DEFAULT_SHEET) -> "NavalForgeBenchmark":
        path = Path(path)
        if path.suffix.lower() == ".csv":
            return cls.from_csv(path)
        if path.suffix.lower() == ".xlsx":
            return cls.from_xlsx(path, sheet_name=sheet_name)
        raise ValueError(f"Formato não suportado: {path.suffix}")

    def top_similar(self, target: ProjectTarget, n: int = 20) -> List[Dict[str, Any]]:
        ranked: List[Dict[str, Any]] = []
        for rec in self.records:
            scored = dict(rec)
            scored.update(compute_similarity(target, rec, self.config))
            ranked.append(scored)
        ranked.sort(key=lambda r: to_float(r.get("Similaridade_%")) or 0.0, reverse=True)
        return ranked[:n]

    def recommended_ranges(self, records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Optional[float]]]:
        mapping = {
            "LOA_m": "LOA_m",
            "B_m": "B_m",
            "Peso_leve_kg": "Peso_leve_kg",
            "HP_max": "HP_max",
            "Combustivel_L": "Combustivel_L",
            "Pessoas": "Pessoas",
        }
        result: Dict[str, Dict[str, Optional[float]]] = {}
        for label, key in mapping.items():
            vals = sorted(v for v in (to_float(r.get(key)) for r in records) if v is not None)
            if vals:
                result[label] = {
                    "min": round(vals[0], 3),
                    "p10": round(_percentile(vals, 0.10) or 0, 3),
                    "mediana": round(statistics.median(vals), 3),
                    "p90": round(_percentile(vals, 0.90) or 0, 3),
                    "max": round(vals[-1], 3),
                    "n": len(vals),
                }
            else:
                result[label] = {"min": None, "p10": None, "mediana": None, "p90": None, "max": None, "n": 0}
        return result

    def regressions(self, records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        return {
            "LOA_Boca": linear_regression(records, "LOA_m", "B_m"),
            "LOA_Peso": linear_regression(records, "LOA_m", "Peso_leve_kg"),
            "LOA_HP": linear_regression(records, "LOA_m", "HP_max"),
            "LOA_Combustivel": linear_regression(records, "LOA_m", "Combustivel_L"),
        }

    def benchmark_report(self, target: ProjectTarget, n: int = 20) -> Dict[str, Any]:
        top = self.top_similar(target, n=n)
        similarities = [to_float(r.get("Similaridade_%")) or 0.0 for r in top]
        maior = max(similarities) if similarities else 0.0
        mediana = statistics.median(similarities) if similarities else 0.0
        if mediana >= 80:
            classificacao = "base forte de benchmark"
        elif mediana >= 65:
            classificacao = "boa base de benchmark preliminar"
        elif mediana >= 50:
            classificacao = "base moderada; revisar filtros"
        else:
            classificacao = "base fraca; buscar mais semelhantes"

        return {
            "target": asdict(target),
            "total_registros": len(self.records),
            "top_n": len(top),
            "maior_similaridade_pct": round(maior, 2),
            "mediana_similaridade_pct": round(mediana, 2),
            "classificacao": classificacao,
            "top_similares": top,
            "faixas_recomendadas": self.recommended_ranges(top),
            "regressoes_top": self.regressions(top),
        }

    def report_to_markdown(self, report: Dict[str, Any]) -> str:
        t = report["target"]
        lines = [
            "# NavalForge Similar Vessels R0 — Relatório de Benchmark",
            "",
            f"**Projeto-alvo:** {t.get('nome', '')}",
            f"**LOA:** {t.get('loa_m')} m  |  **Boca:** {t.get('b_m')} m",
            f"**Grupo:** {t.get('grupo_navalforge', '')}",
            f"**Material:** {t.get('material_normalizado', '')}",
            f"**Propulsão:** {t.get('propulsao_normalizada', '')}",
            "",
            f"**Classificação:** {report['classificacao']}",
            f"**Maior similaridade:** {report['maior_similaridade_pct']}%",
            f"**Mediana TOP:** {report['mediana_similaridade_pct']}%",
            "",
            "## TOP semelhantes",
            "| Rank | Fabricante | Modelo | LOA (m) | Boca (m) | Similaridade |",
            "|---:|---|---|---:|---:|---:|",
        ]
        for i, rec in enumerate(report["top_similares"], 1):
            lines.append(
                f"| {i} | {rec.get('Fabricante', '')} | {rec.get('Modelo', '')} | "
                f"{rec.get('LOA_m', '')} | {rec.get('B_m', '')} | {rec.get('Similaridade_%', '')}% |"
            )
        lines += ["", "## Faixas recomendadas"]
        lines.append("| Parâmetro | Mín | P10 | Mediana | P90 | Máx | n |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for key, vals in report["faixas_recomendadas"].items():
            lines.append(
                f"| {key} | {vals['min']} | {vals['p10']} | {vals['mediana']} | {vals['p90']} | {vals['max']} | {vals['n']} |"
            )
        lines += ["", "## Regressões preliminares sobre o TOP"]
        for key, reg in report["regressoes_top"].items():
            lines.append(f"- **{key}:** {reg.get('status')} | n={reg.get('n')} | R²={reg.get('r2')} | {reg.get('equacao', '')}")
        lines += [
            "",
            "## Limitação técnica",
            "Este relatório é preliminar e serve para benchmark conceitual. Não substitui responsabilidade técnica, normas, cálculo completo, CFD, FEA, ensaio ou prova de mar.",
        ]
        return "\n".join(lines) + "\n"
