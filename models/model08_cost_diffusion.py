"""
Model 8 — Longevity Cost Diffusion: Why F1 Fails
================================================
Wright's Law learning curve analysis demonstrating the structural failure of
the market diffusion / democratization hypothesis (Falsification Condition 1 - F1).

Formulas:
    Cost reduction per cumulative doubling:
        \\Delta C / C = 1 - 2^{-b}
        For biologics: b ≈ 0.15 => 1 - 2^{-0.15} ≈ 9.87% ≈ 9.9%
        For compute:   b ≈ 0.50 => 1 - 2^{-0.50} ≈ 29.29% ≈ 29.3%

    Required doublings from initial price P_init to accessible price P_target:
        n = ln(P_target / P_init) / ln(1 - (1 - 2^{-b})) = ln(P_target / P_init) / (-b * ln(2))
        From $4.25M (Lenmeldy 2024) to $10,000 (accessible):
        n = ln(0.002353) / ln(0.9013) = -6.052 / -0.1039 ≈ 58.2 doublings

    Timeline required:
        At 3-year doubling: 58.2 * 3 = 174.6 years
        At 2-year doubling: 58.2 * 2 = 116.4 years
        Both exceed the ~23-year political activation window (Model 1) by a factor of 5-8x.
"""

import numpy as np
from typing import Dict, List, Tuple

class Model8CostDiffusion:
    def __init__(
        self,
        P_initial: float = 4_250_000.0,  # Lenmeldy 2024 price
        P_target: float = 10_000.0,      # Mass democratization target price
        b_biologics: float = 0.15,
        b_compute: float = 0.50,
        b_solar: float = 0.32,
        b_batteries: float = 0.18
    ):
        self.P_initial = P_initial
        self.P_target = P_target
        self.b_biologics = b_biologics
        self.b_compute = b_compute
        self.b_solar = b_solar
        self.b_batteries = b_batteries

    def cost_reduction_per_doubling(self, b: float) -> float:
        """Percentage cost reduction per production doubling = 1 - 2^(-b)"""
        return 1.0 - 2.0**(-b)

    def required_doublings(self, b: float) -> float:
        """n = ln(P_target / P_init) / (-b * ln(2))"""
        ratio = self.P_target / self.P_initial
        return np.log(ratio) / (-b * np.log(2.0))

    def timeline_years(self, doublings: float, doubling_period_years: float) -> float:
        """Years = doublings * doubling_period"""
        return doublings * doubling_period_years

    def compare_technologies(self) -> Dict[str, Dict[str, float]]:
        """Compare Wright's Law metrics across compute, solar, batteries, and biologics."""
        techs = {
            "Compute hardware": self.b_compute,
            "Solar panels": self.b_solar,
            "Lithium-ion batteries": self.b_batteries,
            "Biologics (literature upper bound)": self.b_biologics,
            "Gene therapies (Kymriah empirical)": 0.001
        }
        
        results = {}
        for name, b in techs.items():
            red = self.cost_reduction_per_doubling(b)
            n_req = self.required_doublings(b)
            t_3yr = self.timeline_years(n_req, 3.0)
            t_2yr = self.timeline_years(n_req, 2.0)
            results[name] = {
                "b_exponent": b,
                "reduction_per_doubling": red,
                "required_doublings": n_req,
                "years_at_3yr_doubling": t_3yr,
                "years_at_2yr_doubling": t_2yr
            }
        return results

    def trajectory(self, b: float, doubling_period: float, years: np.ndarray) -> np.ndarray:
        """Price trajectory P(t) over time under Wright's Law."""
        n_doublings = years / doubling_period
        decay_factor = 2.0**(-b * n_doublings)
        return self.P_initial * decay_factor
