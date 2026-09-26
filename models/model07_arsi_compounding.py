"""
Model 7 — ARSI Capability Compounding with FM2 Saturation
=========================================================
Formalizes Frontier Mechanism 2 (FM2: Competitive Capability Acceleration)
and the collapse of effective regulatory enforcement capacity.

Formulas:
    S_FM2(t) = tanh(\\Lambda(t) / \\Lambda_crit), with \\Lambda_crit ≈ 20
    G_adapt^effective(t) = G_adapt^nominal(t) * (1 - S_FM2(t))

Square-Root Scaling Law for Enforcement Disparity:
    G_adapt^effective ≈ \\rho^{-1/2}
    Where \\rho = Hyperscaler Capex / Public Regulatory Budget
    At t = 2 (2026 baseline): \\rho = $725B / $1B = 725
    G_adapt^effective = (725)^{-1/2} ≈ 0.0371 ≈ 3.7%

Empirical anchor:
    Anthropic RSP withdrawal (February 24, 2026):
    “We didn’t really feel, with the rapid advance of AI, that it made sense for us
    to make unilateral commitments… if competitors are blazing ahead.”
"""

import numpy as np
from typing import Dict

class Model7ARSICompounding:
    def __init__(
        self,
        Lambda_crit: float = 20.0,
        hyperscaler_spend_b: float = 725.0,  # $725B hyperscaler capex
        enforcement_spend_b: float = 1.0,    # $1B EU AI Act / US safety budget
        Lambda_0: float = 12.0,              # Initial regulatory pressure parameter
        compounding_rate: float = 0.60       # ARSI capability growth rate
    ):
        self.Lambda_crit = Lambda_crit
        self.hyperscaler_spend = hyperscaler_spend_b
        self.enforcement_spend = enforcement_spend_b
        self.Lambda_0 = Lambda_0
        self.compounding_rate = compounding_rate

    def resource_disparity_ratio(self) -> float:
        """rho = Hyperscaler Spend / Regulatory Spend"""
        return self.hyperscaler_spend / self.enforcement_spend

    def square_root_enforcement_capacity(self) -> float:
        """Effective capacity = rho^(-1/2)"""
        rho = self.resource_disparity_ratio()
        return 1.0 / np.sqrt(rho)

    def saturation_index(self, Lambda_val: float) -> float:
        """S_FM2(t) = tanh(Lambda(t) / Lambda_crit)"""
        return np.tanh(Lambda_val / self.Lambda_crit)

    def simulate_saturation(
        self,
        t_max: float = 10.0,
        dt: float = 0.2
    ) -> Dict[str, np.ndarray]:
        """Simulate FM2 saturation and governance degradation over time."""
        time_grid = np.arange(0, t_max + dt, dt)
        
        # Capability compounding Lambda(t)
        Lambda_path = self.Lambda_0 * np.exp(self.compounding_rate * time_grid)
        
        # Saturation S_FM2(t)
        S_FM2_path = np.tanh(Lambda_path / self.Lambda_crit)
        
        # Effective adaptation capacity fraction
        G_eff_nominal = 1.0 - S_FM2_path
        
        # Resource-bounded capacity
        # Hyperscaler capex compounds over time
        rho_path = self.resource_disparity_ratio() * np.exp(0.25 * time_grid)
        G_eff_scaling = 1.0 / np.sqrt(rho_path)
        
        return {
            "time": time_grid,
            "Lambda_pressure": Lambda_path,
            "S_FM2_saturation": S_FM2_path,
            "effective_governance_capacity": G_eff_nominal,
            "scaling_law_capacity": G_eff_scaling,
            "year2_saturation": float(S_FM2_path[int(2.0 / dt)]),
            "year2_effective_capacity": float(G_eff_nominal[int(2.0 / dt)])
        }
