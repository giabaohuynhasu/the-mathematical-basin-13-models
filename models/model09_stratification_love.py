"""
Model 9 — Stratification Reproduction Through Love
==================================================
Formalizes the kinship-driven transmission of biological advantage through Hamilton's Rule
and the Love Commodification Index.

Formulas:
    Hamilton's Rule:
        r * B > C
        For parent-child: r = 0.5.
        When B represents mortal biological survival (B -> ∞),
        p_L = 1.0 for any finite economic cost C.
        Every enhanced parent will allocate whatever resources are necessary to procure access for offspring.

    Love Commodification Index:
        C_love(t) = E(t) * p_L * P_long(t) / Y_median(t)
        At t0: P_long ∈ [$2.125M, $4.25M], Y_median ∈ [$10,000, $15,000]
        C_love(t0) ∈ [140, 425]  (normalized per capita multiple)

    Kinship Transmission Dynamics:
        E(t) = E0 * exp(f_E * t)
        At f_E = 0.02: E(100) = 27,048 from E0 = 10,000.
        The primary driver of inequality is not elite headcount E(t),
        but the epigenetic divergence Delta(t).
"""

import numpy as np
from typing import Dict, Tuple

class Model9StratificationLove:
    def __init__(
        self,
        E0: float = 10_000.0,
        f_E: float = 0.02,
        r_hamilton: float = 0.50,
        p_L: float = 1.0,
        P_long_0: float = 4_250_000.0,
        Y_median_0: float = 12_500.0,
        g_income: float = 0.015
    ):
        self.E0 = E0
        self.f_E = f_E
        self.r_hamilton = r_hamilton
        self.p_L = p_L
        self.P_long_0 = P_long_0
        self.Y_median_0 = Y_median_0
        self.g_income = g_income

    def love_commodification_index(self, P_long: float, Y_median: float) -> float:
        """Normalized price-to-median-income multiple representing love commodification pressure."""
        return (self.p_L * P_long) / Y_median

    def simulate_dynamics(
        self,
        time_grid: np.ndarray,
        price_trajectory: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """Simulate elite expansion E(t), median income Y(t), and C_love(t)."""
        E_path = self.E0 * np.exp(self.f_E * time_grid)
        Y_median_path = self.Y_median_0 * np.exp(self.g_income * time_grid)
        
        C_love_path = (self.p_L * price_trajectory) / Y_median_path
        
        return {
            "time": time_grid,
            "E_elite": E_path,
            "Y_median": Y_median_path,
            "P_long": price_trajectory,
            "C_love": C_love_path,
            "C_love_t0": float(C_love_path[0]),
            "E_100": float(self.E0 * np.exp(self.f_E * 100.0))
        }
