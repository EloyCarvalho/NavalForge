from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class PowerEstimate:
    effective_power_kw: float
    brake_power_kw: float
    installed_power_kw: float
    propulsive_efficiency: float
    margin_factor: float
    warning: str

    def to_dict(self) -> dict:
        return asdict(self)


def estimate_installed_power(effective_power_kw: float, propulsive_efficiency: float = 0.55, margin_factor: float = 1.15) -> PowerEstimate:
    if propulsive_efficiency <= 0:
        raise ValueError("propulsive_efficiency must be positive")
    if margin_factor < 1.0:
        raise ValueError("margin_factor should be >= 1.0")
    brake = effective_power_kw / propulsive_efficiency
    installed = brake * margin_factor
    return PowerEstimate(
        effective_power_kw=effective_power_kw,
        brake_power_kw=brake,
        installed_power_kw=installed,
        propulsive_efficiency=propulsive_efficiency,
        margin_factor=margin_factor,
        warning="Preliminary power estimate. Propeller, gear ratio, engine curve and sea margin require dedicated analysis.",
    )
