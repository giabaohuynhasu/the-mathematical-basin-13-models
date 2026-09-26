"""
Model 3 & Model 3b — The Conditional Chain: Lock-in Probability Tree & Marie Antoinette Modifier
=================================================================================================
Formalizes the 5-node conditional logic chain and the Symbol-Body Fusion non-linearity.

Nodes:
    p1 = 0.87: ARSI-Longevity Resonance consolidates
    p2 = 0.88: Stratification becomes structurally persistent (Wright's Law vs 23-yr window)
    p3 = 0.90: A5 activates at political scale
    p4 = 0.85: Institutional paralysis (Three-phase legitimacy dissolution)
    p5 = 0.72: Lock-in becomes irreversible (Dam Paradox + Generative Paradox)

Derived outcomes (partition summing to 1.0):
    P(lock-in)         = p1 * p2 * p3 * p4 * p5 = 0.4206 ≈ 0.42
    P(F2 exit, Node 3) = p1 * p2 * (1 - p3)     = 0.0766 ≈ 0.08
    P(Late Escape)     = p1 * p2 * p3 * [(1 - p4) + p4 * (1 - p5)] = 0.2673 ≈ 0.27
    P(Early Resolution)= 1 - P(lock-in) - P(F2) - P(Late Escape)   = 0.2355 ≈ 0.23

Model 3b Modifier:
    \\eta(t) = \\Delta(t) * L_vis(t) * I_body(t)
    p4(\\eta) = p4_base + (1 - p4_base) * min(1, \\eta / \\eta_crit)
    Where p4_base = 0.85, \\eta_crit = 1.0.
"""

import numpy as np
from typing import Dict, List, Tuple

class Model3LockinChain:
    def __init__(
        self,
        p1: float = 0.87,
        p2: float = 0.88,
        p3: float = 0.90,
        p4_base: float = 0.85,
        p5_base: float = 0.72
    ):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4_base = p4_base
        self.p5_base = p5_base

    def calculate_probabilities(self, p4: float = None, p5: float = None) -> Dict[str, float]:
        """Calculates derived branch probabilities summing to 1.0."""
        p4_val = self.p4_base if p4 is None else p4
        p5_val = self.p5_base if p5 is None else p5

        p_lockin = self.p1 * self.p2 * self.p3 * p4_val * p5_val
        p_f2 = self.p1 * self.p2 * (1.0 - self.p3)
        p_late_escape = self.p1 * self.p2 * self.p3 * ((1.0 - p4_val) + p4_val * (1.0 - p5_val))
        p_early = 1.0 - (p_lockin + p_f2 + p_late_escape)

        return {
            "P_lockin": p_lockin,
            "P_F2_exit": p_f2,
            "P_late_escape": p_late_escape,
            "P_early_resolution": p_early,
            "sum": p_lockin + p_f2 + p_late_escape + p_early
        }

    def simulate_monte_carlo(self, n_sims: int = 100_000, seed: int = 42) -> Dict[str, float]:
        """Empirical Monte Carlo path sampling through the 5 nodes."""
        np.random.seed(seed)
        
        # Node 1
        n1 = np.random.rand(n_sims) < self.p1
        # Node 2 (given N1)
        n2 = n1 & (np.random.rand(n_sims) < self.p2)
        # Early resolution before Node 3
        early_res = ~n2
        
        # Node 3 (given N2)
        n3 = n2 & (np.random.rand(n_sims) < self.p3)
        f2_exit = n2 & ~n3
        
        # Node 4 (given N3)
        n4 = n3 & (np.random.rand(n_sims) < self.p4_base)
        late_escape_n4 = n3 & ~n4
        
        # Node 5 (given N4)
        n5 = n4 & (np.random.rand(n_sims) < self.p5_base)
        late_escape_n5 = n4 & ~n5
        
        lockin = n5
        late_escape = late_escape_n4 | late_escape_n5

        return {
            "MC_lockin": float(np.mean(lockin)),
            "MC_F2_exit": float(np.mean(f2_exit)),
            "MC_late_escape": float(np.mean(late_escape)),
            "MC_early_resolution": float(np.mean(early_res)),
            "MC_sum": float(np.mean(lockin) + np.mean(f2_exit) + np.mean(late_escape) + np.mean(early_res))
        }


class Model3bMarieAntoinette:
    def __init__(self, p4_base: float = 0.85, eta_crit: float = 1.0):
        self.p4_base = p4_base
        self.eta_crit = eta_crit

    def eta(self, delta: float, L_vis: float = 1.0, I_body: float = 1.0) -> float:
        """Symbol-Body Fusion non-linearity: eta(t) = delta(t) * L_vis(t) * I_body(t)"""
        return delta * L_vis * I_body

    def modified_p4(self, eta_val: float) -> float:
        """p4(eta) = p4_base + (1 - p4_base) * min(1.0, eta / eta_crit)"""
        ratio = min(1.0, max(0.0, eta_val / self.eta_crit))
        return self.p4_base + (1.0 - self.p4_base) * ratio
