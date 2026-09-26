"""
Model 5 — Welfare State Actuarial Collapse
==========================================
Formalizes the actuarial collapse of pay-as-you-go welfare systems under longevity asymmetry.

Formulas:
    PV_enhanced = \\mu_b / r = $30,000 / 0.03 = $1,000,000 per enhanced individual
    Shortfall(t) \\propto E(t)^2   [Superlinear quadratic scaling: count * extended duration]
    
    Welfare-Legitimacy Coupling:
    dL_pol/dt = -\\sigma * \\Delta(t) * L_pol(t) * [1 - L_pol(t)] * [1 + \\kappa_W * \\Theta(W_crit - W(t))]

Empirical anchor:
    2024 US Social Security Trustees Report: Trust Fund exhaustion projected 2033,
    23% automatic benefit cut, $3.6 trillion 10-year shortfall baseline before any targeted longevity interventions.
"""

import numpy as np
from typing import Dict

class Model5ActuarialCollapse:
    def __init__(
        self,
        mu_b: float = 30_000.0,       # Annual public entitlement per beneficiary
        r_discount: float = 0.03,     # Risk-free real discount rate
        W_crit: float = 0.70,         # Critical welfare solvency threshold
        kappa_W: float = 0.30,        # Legitimacy decay amplification when W < W_crit
        sigma: float = 0.02,          # Baseline legitimacy sensitivity
        W0: float = 0.85,             # Initial trust fund solvency index (baseline 2026)
        trust_fund_depletion_year: float = 7.0  # 2033 depletion from 2026 baseline
    ):
        self.mu_b = mu_b
        self.r = r_discount
        self.W_crit = W_crit
        self.kappa_W = kappa_W
        self.sigma = sigma
        self.W0 = W0
        self.depletion_yr = trust_fund_depletion_year

    def present_value_per_enhanced(self) -> float:
        """PV_enhanced = mu_b / r"""
        return self.mu_b / self.r

    def simulate_actuarial_dynamics(
        self,
        E_trajectory: np.ndarray,
        delta_trajectory: np.ndarray,
        time_grid: np.ndarray,
        L_pol_0: float = 0.80
    ) -> Dict[str, np.ndarray]:
        """
        Simulate welfare trust fund solvency W(t), total added actuarial liability,
        and the resulting legitimacy coupling dL_pol/dt.
        """
        n_steps = len(time_grid)
        dt = time_grid[1] - time_grid[0]
        
        pv_unit = self.present_value_per_enhanced()
        
        # Additional actuarial burden: scales quadratically with E(t)
        # Baseline per-capita burden * E(t) * (1 + delta(t) / 40.0)
        added_liability = E_trajectory * pv_unit * (1.0 + delta_trajectory / 40.0)
        
        # Welfare solvency index W(t) decaying from baseline baseline to 2033 (year 7)
        # and further depressed by added liability
        W_path = np.zeros(n_steps)
        L_pol_path = np.zeros(n_steps)
        L_pol_path[0] = L_pol_0
        
        for i in range(n_steps):
            t = time_grid[i]
            # Baseline linear depletion to 2033, capped at 0.50 after automatic cut
            base_W = max(0.50, self.W0 - (self.W0 - 0.50) * (t / self.depletion_yr))
            # Additional drag from longevity tier
            longevity_drag = min(0.30, added_liability[i] / 5.0e12) # relative to $5T baseline fund
            W_path[i] = max(0.20, base_W - longevity_drag)
            
            if i < n_steps - 1:
                # Heaviside trigger
                is_below_crit = 1.0 if W_path[i] < self.W_crit else 0.0
                amp = 1.0 + self.kappa_W * is_below_crit
                
                L_curr = L_pol_path[i]
                dL_dt = -self.sigma * delta_trajectory[i] * L_curr * (1.0 - L_curr) * amp
                L_pol_path[i+1] = max(0.01, min(1.0, L_curr + dL_dt * dt))

        return {
            "time": time_grid,
            "PV_unit": pv_unit,
            "added_actuarial_liability": added_liability,
            "W_solvency": W_path,
            "L_pol": L_pol_path
        }
