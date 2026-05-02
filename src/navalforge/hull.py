from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
from .units import knots_to_ms

@dataclass
class Hull:
    """Basic hull definition for preliminary naval architecture calculations.

    Units:
    - length/beam/draft/centers: m
    - speed: knots
    - displacement: kg
    - angles: degrees
    """
    name: str
    lwl: float
    beam: float
    draft: float
    cb: float
    cp: float
    cwp: float
    lcb: float
    lcg: float
    vcg: float
    speed_knots: float
    displacement_kg: float | None = None
    deadrise_deg: float = 15.0
    trim_deg: float | None = None
    chine_beam: float | None = None
    propulsive_efficiency: float = 0.55
    appendage_factor: float = 1.05
    notes: str = ""

    def validate(self) -> None:
        positive = {"lwl": self.lwl, "beam": self.beam, "draft": self.draft, "speed_knots": self.speed_knots}
        for k, v in positive.items():
            if v < 0 or (k != "speed_knots" and v == 0):
                raise ValueError(f"{k} must be positive; speed can be zero.")
        for attr in ["cb", "cp", "cwp"]:
            value = getattr(self, attr)
            if not (0 < value <= 1):
                raise ValueError(f"{attr} must be in the interval (0, 1].")
        if self.vcg < 0:
            raise ValueError("vcg must not be negative in this simplified model.")
        if self.propulsive_efficiency <= 0 or self.propulsive_efficiency > 1:
            raise ValueError("propulsive_efficiency must be in (0, 1].")

    @property
    def speed_ms(self) -> float:
        return knots_to_ms(self.speed_knots)

    @property
    def length_beam_ratio(self) -> float:
        return self.lwl / self.beam

    @property
    def beam_draft_ratio(self) -> float:
        return self.beam / self.draft

    @property
    def effective_chine_beam(self) -> float:
        return self.chine_beam or self.beam

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Hull":
        return cls(**data)
