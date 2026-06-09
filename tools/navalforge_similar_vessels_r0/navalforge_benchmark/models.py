from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ProjectTarget:
    """Dados mínimos do projeto-alvo para busca de embarcações semelhantes."""

    nome: str = "Projeto alvo"
    loa_m: Optional[float] = None
    b_m: Optional[float] = None
    grupo_navalforge: str = ""
    material_normalizado: str = ""
    propulsao_normalizada: str = ""
    regime_principal: str = ""
    uso: str = ""
    peso_leve_kg: Optional[float] = None
    potencia_max_hp: Optional[float] = None
    combustivel_l: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectTarget":
        def first(*keys: str, default=None):
            for key in keys:
                if key in data and data[key] not in ("", None):
                    return data[key]
            return default

        def num(*keys: str):
            value = first(*keys)
            if value in ("", None):
                return None
            try:
                return float(str(value).replace(",", "."))
            except (TypeError, ValueError):
                return None

        return cls(
            nome=str(first("nome", "Nome", "projeto", default="Projeto alvo")),
            loa_m=num("loa_m", "LOA_m", "LOA", "Comprimento_m"),
            b_m=num("b_m", "B_m", "Boca_m", "Boca"),
            grupo_navalforge=str(first("grupo_navalforge", "Grupo_NavalForge", default="")),
            material_normalizado=str(first("material_normalizado", "Material_Normalizado", default="")),
            propulsao_normalizada=str(first("propulsao_normalizada", "Propulsao_Normalizada", default="")),
            regime_principal=str(first("regime_principal", "Regime_Principal", default="")),
            uso=str(first("uso", "Uso", "Categoria", default="")),
            peso_leve_kg=num("peso_leve_kg", "Peso_leve_kg"),
            potencia_max_hp=num("potencia_max_hp", "HP_max", "Potencia_max_hp"),
            combustivel_l=num("combustivel_l", "Combustivel_L", "Fuel_L"),
        )
