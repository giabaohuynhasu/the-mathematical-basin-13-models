"""
Model 12 — Intra-Elite Fracture Field
=====================================
Formalizes the fracture and consolidation dynamics within the biologically enhanced elite.

Formulas:
    dF/dt = \\kappa_F * [(E - E_inner) / E] - \\lambda_F * F
    Where:
        \\kappa_F = 0.15 year^-1 (fracture generation rate)
        \\lambda_F = 0.05 year^-1 (consolidation rate)
        Ratio \\kappa_F / \\lambda_F = 3.0 implies fracture generation is 3x faster than consolidation.

Harmonic Mean Duration (Historical Benchmark):
    \\tau_frag = 4 / (1/5.8 + 1/27.8 + 1/9.1 + 1/3.6) ≈ 6.5 years

Historical Cases:
    1. Warlord China (1916-1928): duration 12 yr, tau = 5.8 yr (Nationalist consolidation)
    2. Sengoku Japan (1467-1615): duration 148 yr, tau = 27.8 yr (Tokugawa consolidation)
    3. French Revolution (1789-1799): duration 10 yr, tau = 9.1 yr (Napoleonic consolidation)
    4. Russian Civil War (1917-1922): duration 5 yr, tau = 3.6 yr (Bolshevik consolidation)
"""

import numpy as np
from typing import Dict, List

class Model12IntraEliteFracture:
    def __init__(
        self,
        kappa_F: float = 0.15,
        lambda_F: float = 0.05,
        inner_fraction: float = 0.20 # E_inner = 20% inner core of enhanced elite
    ):
        self.kappa_F = kappa_F
        self.lambda_F = lambda_F
        self.inner_fraction = inner_fraction

    @staticmethod
    def historical_harmonic_mean() -> float:
        """Harmonic mean of historical multi-faction fracture episodes."""
        durations = [5.8, 27.8, 9.1, 3.6]
        return len(durations) / sum(1.0 / d for d in durations)

    def simulate_fracture_dynamics(
        self,
        time_grid: np.ndarray,
        F0: float = 0.05
    ) -> Dict[str, np.ndarray]:
        """Simulate ODE dF/dt = kappa_F * (1 - inner_fraction) - lambda_F * F."""
        dt = time_grid[1] - time_grid[0]
        n_steps = len(time_grid)
        
        F_path = np.zeros(n_steps)
        F_path[0] = F0
        
        outer_fraction = 1.0 - self.inner_fraction
        
        for i in range(n_steps - 1):
            dF_dt = self.kappa_F * outer_fraction - self.lambda_F * F_path[i]
            F_next = F_path[i] + dF_dt * dt
            F_path[i+1] = max(0.0, F_next)
            
        steady_state = (self.kappa_F * outer_fraction) / self.lambda_F
        
        return {
            "time": time_grid,
            "fracture_index": F_path,
            "steady_state": steady_state,
            "harmonic_mean_tau": self.historical_harmonic_mean(),
            "kappa_over_lambda": self.kappa_F / self.lambda_F
        }
