from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Tuple

from .similarity import to_float


def linear_regression(records: Iterable[Dict[str, Any]], x_key: str, y_key: str, min_n: int = 8) -> Dict[str, Any]:
    pairs: List[Tuple[float, float]] = []
    for rec in records:
        x = to_float(rec.get(x_key))
        y = to_float(rec.get(y_key))
        if x is not None and y is not None and x > 0 and y > 0:
            pairs.append((x, y))

    n = len(pairs)
    if n < min_n:
        return {"n": n, "status": "não recomendado", "motivo": "poucos dados"}

    xs, ys = zip(*pairs)
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    ss_xx = sum((x - x_mean) ** 2 for x in xs)
    if ss_xx == 0:
        return {"n": n, "status": "não recomendado", "motivo": "x constante"}

    slope = sum((x - x_mean) * (y - y_mean) for x, y in pairs) / ss_xx
    intercept = y_mean - slope * x_mean
    y_hat = [intercept + slope * x for x in xs]
    ss_tot = sum((y - y_mean) ** 2 for y in ys)
    ss_res = sum((y - yh) ** 2 for y, yh in zip(ys, y_hat))
    r2 = 1 - ss_res / ss_tot if ss_tot else 0.0

    if r2 >= 0.80:
        status = "forte"
    elif r2 >= 0.60:
        status = "moderado"
    elif r2 >= 0.40:
        status = "fraco"
    else:
        status = "não recomendado"

    return {
        "n": n,
        "status": status,
        "x_key": x_key,
        "y_key": y_key,
        "slope": round(slope, 6),
        "intercept": round(intercept, 6),
        "r2": round(r2, 4),
        "equacao": f"{y_key} = {slope:.6g} * {x_key} + {intercept:.6g}",
    }
