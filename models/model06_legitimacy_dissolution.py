"""
Model 6 & Model 6b — Governance Legitimacy Dissolution: Three-Phase Automaton & Elite Overlap
=============================================================================================
Formalizes the three-phase collapse of institutional legitimacy and the governance-elite overlap amplifier.

Phase 1 (L_pol > 0.50, \\sigma_1 = 0.015):
    dL_pol/dt = -\\sigma_1 * \\Delta(t) * L_pol * (1 - L_pol) * (1 - I_A5)

Phase 2 (0.35 < L_pol <= 0.50, \\sigma_2 = 0.025):
    dL_pol/dt = -\\sigma_2 * \\Delta(t) * L_pol * (1 - L_pol) * I_A5 * (1 - R_trap)

Phase 3 (L_pol <= 0.35, \\sigma_3 = 0.035, recursive trap):
    dL_pol/dt = -\\sigma_3 * \\Delta(t) * L_pol * (1 - L_pol) * I_A5 * R_trap * (1 + \\kappa_inst)

Phase 2 Traversal Time:
    \\Delta t_crit = 0.15 / (0.025 * 4.5 * 0.25) ≈ 5.3 years

Civilizational Vector:
    L_pol^system = min_i L_pol,i

Model 6b:
    O_eg(t) = E_governance(t) / E_total(t)
    \\sigma(t) = \\sigma_0 * (1 + \\chi * O_eg(t)), with \\sigma_0 = 0.02, \\chi = 0.50.
"""

import numpy as np
from typing import Dict, List, Tuple

class Model6LegitimacyDissolution:
    def __init__(
        self,
        sigma_1: float = 0.015,
        sigma_2: float = 0.025,
        sigma_3: float = 0.035,
        kappa_inst: float = 0.20,
        L_crit_phase2: float = 0.50,
        L_crit_phase3: float = 0.35
    ):
        self.sigma_1 = sigma_1
        self.sigma_2 = sigma_2
        self.sigma_3 = sigma_3
        self.kappa_inst = kappa_inst
        self.L_crit_phase2 = L_crit_phase2
        self.L_crit_phase3 = L_crit_phase3

    def theoretical_traversal_time(self, delta_mean: float = 4.5) -> float:
        """\\Delta t_crit = 0.15 / (sigma_2 * delta * 0.25)"""
        denom = self.sigma_2 * delta_mean * 0.25
        return 0.15 / denom

    def simulate_automaton(
        self,
        time_grid: np.ndarray,
        delta_path: np.ndarray,
        A5_activation_time: float = 10.0,
        R_trap_activation_time: float = 18.0,
        L_pol_0: float = 0.85
    ) -> Dict[str, np.ndarray]:
        """Simulate piecewise 3-phase ODE."""
        n_steps = len(time_grid)
        dt = time_grid[1] - time_grid[0]
        
        L_path = np.zeros(n_steps)
        L_path[0] = L_pol_0
        phases = np.zeros(n_steps, dtype=int)
        
        phase2_start = None
        phase3_start = None
        
        for i in range(n_steps - 1):
            t = time_grid[i]
            L = L_path[i]
            delta = delta_path[i]
            
            # Indicator variables
            I_A5 = 1.0 if t >= A5_activation_time else 0.0
            R_trap = 1.0 if t >= R_trap_activation_time else 0.0
            
            logistic_term = L * (1.0 - L)
            
            if L > self.L_crit_phase2:
                phases[i] = 1
                # Phase 1: Institutional habituation
                rate = -self.sigma_1 * delta * logistic_term * (1.0 - 0.5 * I_A5)
            elif L > self.L_crit_phase3:
                phases[i] = 2
                if phase2_start is None:
                    phase2_start = t
                # Phase 2: Reform acceleration paradox
                rate = -self.sigma_2 * delta * logistic_term * max(0.5, I_A5) * (1.0 - 0.3 * R_trap)
            else:
                phases[i] = 3
                if phase3_start is None:
                    phase3_start = t
                # Phase 3: Recursive legitimacy trap
                rate = -self.sigma_3 * delta * logistic_term * (1.0 + self.kappa_inst)
                
            L_next = L + rate * dt
            L_path[i+1] = max(0.02, min(1.0, L_next))
            
        phases[-1] = phases[-2]
        
        traversal_time = (phase3_start - phase2_start) if (phase2_start and phase3_start) else None
        
        return {
            "time": time_grid,
            "L_pol": L_path,
            "phases": phases,
            "phase2_start": phase2_start,
            "phase3_start": phase3_start,
            "simulated_traversal_time": traversal_time
        }


class Model6bGovernanceEliteOverlap:
    def __init__(self, sigma_0: float = 0.02, chi: float = 0.50):
        self.sigma_0 = sigma_0
        self.chi = chi

    def sensitivity(self, O_eg: float) -> float:
        """sigma(t) = sigma_0 * (1 + chi * O_eg(t))"""
        return self.sigma_0 * (1.0 + self.chi * np.clip(O_eg, 0.0, 1.0))
