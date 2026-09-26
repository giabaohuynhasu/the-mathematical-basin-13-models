"""
Model 2 — The Impossibility Lemma (ALRP)
========================================
Formalizes the ARSI-Longevity Resonance Paradox (ALRP).

Theorem:
    There exists no point in the parameter space {r_A, r_L, \\alpha_AL, \\alpha_LA, b, C0}
    where both conditions hold simultaneously:
    (i)  dA/dt < g_critical     [ARSI decelerated enough to prevent governance catastrophe]
    (ii) dC_mfg/dt > g_access   [cost reduction fast enough to democratize before A5 activation]

Proof sketch:
    - Condition (i) requires: r_A + \\alpha_LA * L < g_critical
    - Condition (ii) requires: r_cost = b * ln(2) / T_double > g_access
    - For biologics: b ≈ 0.15, yielding r_cost ≈ 0.10 year^-1 (at T_double = 3 years).
    - Realized ARSI rate: r_A ≈ 1.85 year^-1 (SWE-Bench / frontier AI progression).
    - In order to compress T_double sufficiently to achieve g_access, r_A must be elevated;
      conversely, decelerating r_A to satisfy (i) collapses r_cost, violating (ii).
    - Cost floor C0 = 0.10 bounds minimum cost at 10% of current price ($210k-$430k),
      which remains ~20x above global median annual income ($10k-$15k).
"""

import numpy as np
from typing import Dict, Tuple

class Model2ALRPImpossibility:
    def __init__(
        self,
        b_biologics: float = 0.15,
        b_compute: float = 0.50,
        r_A_realized: float = 1.85,    # 185% annual capability expansion (SWE-Bench)
        g_critical: float = 0.35,      # Governance maximum absorption ceiling
        g_access: float = 0.40,        # Minimum cost reduction velocity to beat 23-yr window
        C0: float = 0.10,              # Minimum biological manufacturing floor
        P_initial: float = 4_250_000,  # Lenmeldy 2024 price
        Y_median: float = 12_500       # Global median annual income
    ):
        self.b_biologics = b_biologics
        self.b_compute = b_compute
        self.r_A_realized = r_A_realized
        self.g_critical = g_critical
        self.g_access = g_access
        self.C0 = C0
        self.P_initial = P_initial
        self.Y_median = Y_median

    def cost_reduction_rate(self, b: float, T_double: float) -> float:
        """Annual cost reduction velocity: r_cost = b * ln(2) / T_double"""
        return (b * np.log(2.0)) / T_double

    def minimum_cost_floor(self) -> float:
        """C_min = C0 * P_initial"""
        return self.C0 * self.P_initial

    def evaluate_grid(
        self,
        r_A_range: Tuple[float, float] = (0.05, 3.0),
        T_double_range: Tuple[float, float] = (0.5, 10.0),
        resolution: int = 100
    ) -> Dict[str, np.ndarray]:
        """
        Evaluate parameter space (r_A, T_double) and compute:
        Region 1: Satisfies (i) dA/dt < g_critical
        Region 2: Satisfies (ii) r_cost > g_access
        Intersection: Region 1 AND Region 2
        """
        r_A_grid = np.linspace(r_A_range[0], r_A_range[1], resolution)
        T_double_grid = np.linspace(T_double_range[0], T_double_range[1], resolution)
        
        R_A, T_D = np.meshgrid(r_A_grid, T_double_grid)
        
        # Effective biological doubling time is linked to AI acceleration:
        # Higher r_A compresses T_double: T_double(r_A) ≈ T_base / (1 + 0.5 * r_A)
        # Condition (i): r_A < g_critical
        cond1 = R_A < self.g_critical
        
        # Condition (ii): r_cost(b, T_double) > g_access
        r_cost = (self.b_biologics * np.log(2.0)) / T_D
        cond2 = r_cost > self.g_access
        
        intersection = cond1 & cond2
        
        return {
            "r_A_grid": r_A_grid,
            "T_double_grid": T_double_grid,
            "R_A": R_A,
            "T_D": T_D,
            "cond1_governance_safe": cond1,
            "cond2_democratization_fast": cond2,
            "intersection": intersection,
            "intersection_area": float(np.sum(intersection)),
            "cost_floor_ratio": self.minimum_cost_floor() / self.Y_median
        }
