from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9+/ ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def to_float(value: Any) -> Optional[float]:
    if value in ("", None):
        return None
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def numeric_score(target: Optional[float], actual: Optional[float], tolerance_ratio: float) -> float:
    """Score 0-100 com tolerância proporcional ao valor alvo."""
    if target is None or actual is None or target <= 0:
        return 50.0
    tolerance = abs(target) * tolerance_ratio
    if tolerance <= 0:
        return 50.0
    error = abs(actual - target)
    score = max(0.0, 100.0 * (1.0 - error / tolerance))
    return round(score, 2)


def category_score(target: str, actual: str, default: float = 50.0) -> float:
    t = normalize_text(target)
    a = normalize_text(actual)
    if not t or not a:
        return default
    if t == a:
        return 100.0
    if t in a or a in t:
        return 85.0
    t_words = set(t.split())
    a_words = set(a.split())
    if not t_words or not a_words:
        return default
    overlap = len(t_words & a_words) / max(len(t_words | a_words), 1)
    return round(max(default, 100.0 * overlap), 2)


@dataclass
class SimilarityConfig:
    loa_tolerance_ratio: float = 0.35
    beam_tolerance_ratio: float = 0.35
    weight_loa: float = 0.30
    weight_beam: float = 0.18
    weight_group: float = 0.22
    weight_material: float = 0.12
    weight_propulsion: float = 0.10
    weight_regime: float = 0.08


def compute_similarity(target: Any, rec: Dict[str, Any], config: SimilarityConfig | None = None) -> Dict[str, float]:
    cfg = config or SimilarityConfig()
    loa = to_float(rec.get("LOA_m") or rec.get("loa_m") or rec.get("Comprimento_m"))
    beam = to_float(rec.get("B_m") or rec.get("b_m") or rec.get("Boca_m"))

    score_loa = numeric_score(target.loa_m, loa, cfg.loa_tolerance_ratio)
    score_beam = numeric_score(target.b_m, beam, cfg.beam_tolerance_ratio)
    score_group = category_score(target.grupo_navalforge, rec.get("Grupo_NavalForge", rec.get("grupo_navalforge", "")))
    score_material = category_score(target.material_normalizado, rec.get("Material_Normalizado", rec.get("material_normalizado", "")))
    score_prop = category_score(target.propulsao_normalizada, rec.get("Propulsao_Normalizada", rec.get("propulsao_normalizada", "")))
    score_regime = category_score(target.regime_principal, rec.get("Regime_Principal", rec.get("regime_principal", "")))

    total = (
        score_loa * cfg.weight_loa
        + score_beam * cfg.weight_beam
        + score_group * cfg.weight_group
        + score_material * cfg.weight_material
        + score_prop * cfg.weight_propulsion
        + score_regime * cfg.weight_regime
    )

    return {
        "Score_LOA": score_loa,
        "Score_Boca": score_beam,
        "Score_Grupo": score_group,
        "Score_Material": score_material,
        "Score_Propulsao": score_prop,
        "Score_Regime": score_regime,
        "Similaridade_%": round(total, 2),
    }
