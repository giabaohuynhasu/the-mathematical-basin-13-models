"""
Model 11 — Dam Integrity Field
==============================
Formalizes the Dam Paradox: Mortality as the historical equalizer of concentrated power,
and how biological asymmetry subjects this equalizer to the same stratification it historically corrected.

Formulas:
    I_dam(t) = exp(- \\int_{t0}^t \\epsilon(\\tau) * [E(\\tau) / N_total] d\\tau)
    \\delta_dam(t) = I_dam(t) * \\delta_dam_0

    Impact on Node 5 Capture Probability:
    p5(t) = p5_base + (1 - p5_base) * (1 - \\delta_dam(t) / \\delta_dam_0)
    When I_dam -> 1.0 (thick dam): p5 = 0.72 (28% chance of genuine redistribution).
    When I_dam -> 0.0 (broken dam): p5 -> 1.0 (entropy reset fully captured by elite structures).

Empirical anchor:
    Belsky et al. (2022): 7.3-year biological age gradient across income quintiles by DunedinPACE
    before targeted intervention, establishing I_dam < 1.0 at t0.
"""

import numpy as np
from typing import Dict

class Model11DamIntegrity:
    def __init__(
        self,
        p5_base: float = 0.72,
        delta_dam_0: float = 1.0,
        epsilon: float = 1.2e-4,     # Scaling parameter for elite biological decoupling impact
        N_total: float = 8.1e9
    ):
        self.p5_base = p5_base
        self.delta_dam_0 = delta_dam_0
        self.epsilon = epsilon
        self.N_total = N_total

    def compute_integrity(
        self,
        time_grid: np.ndarray,
        E_trajectory: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """Compute I_dam(t) and capture probability p5(t)."""
        dt = time_grid[1] - time_grid[0]
        n_steps = len(time_grid)
        
        cumulative_exposure = np.zeros(n_steps)
        integral_sum = 0.0
        
        for i in range(1, n_steps):
            rate = self.epsilon * (E_trajectory[i] / 10_000.0)
            integral_sum += rate * dt
            cumulative_exposure[i] = integral_sum
            
        I_dam_path = np.exp(-cumulative_exposure)
        delta_dam_path = I_dam_path * self.delta_dam_0
        
        # p5(t) = p5_base + (1 - p5_base) * (1 - delta_dam(t) / delta_dam_0)
        p5_path = self.p5_base + (1.0 - self.p5_base) * (1.0 - delta_dam_path / self.delta_dam_0)
        
        return {
            "time": time_grid,
            "I_dam": I_dam_path,
            "delta_dam": delta_dam_path,
            "p5_capture_probability": p5_path,
            "p5_at_t0": float(p5_path[0]),
            "p5_final": float(p5_path[-1])
        }
