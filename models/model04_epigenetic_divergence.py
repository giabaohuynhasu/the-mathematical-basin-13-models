"""
Model 4 — A4 Biological Stratification: Epigenetic Age Divergence
==================================================================
Formalizes epigenetic age divergence and the Biological Gini Coefficient.

Formulas:
    d\\Delta / dt = \\epsilon(t) * [v_general(t) - v_E(t)]
    G_bio(t) = \\Delta(t) * E(t) / (B_general(t) * N_total)

Empirical anchor:
    Belsky et al. (2022): Pre-existing socioeconomic gradient of \\Delta(t0) = 7.3 biological years
    measured by DunedinPACE before any targeted cellular reprogramming intervention.
    v_general ≈ 1.0 biological years / chronological year.
    v_E ≈ 0.35 biological years / chronological year (NewLimit 2026 liver cell reversal).
"""

import numpy as np
from typing import Dict

class Model4EpigeneticDivergence:
    def __init__(
        self,
        delta_0: float = 7.3,            # Pre-existing biological age gap in years (Belsky 2022)
        v_general: float = 1.02,         # Aging velocity general population
        v_enhanced: float = 0.35,        # Aging velocity enhanced tier
        efficiency_epsilon: float = 0.90,# Intervention biological fidelity
        E0: float = 10_000,              # Initial enhanced cohort size
        f_E: float = 0.02,               # Elite population growth rate
        N_total: float = 8.1e9,          # Global general population
        B_general_0: float = 40.0        # Mean biological age of baseline population
    ):
        self.delta_0 = delta_0
        self.v_general = v_general
        self.v_enhanced = v_enhanced
        self.efficiency = efficiency_epsilon
        self.E0 = E0
        self.f_E = f_E
        self.N_total = N_total
        self.B_general_0 = B_general_0

    def simulate_divergence(
        self,
        t_max: float = 50.0,
        dt: float = 0.5
    ) -> Dict[str, np.ndarray]:
        """Simulate Delta(t) and Biological Gini G_bio(t) over time."""
        time_grid = np.arange(0, t_max + dt, dt)
        
        # dDelta/dt = epsilon * (v_general - v_enhanced)
        divergence_rate = self.efficiency * (self.v_general - self.v_enhanced)
        
        delta_path = self.delta_0 + divergence_rate * time_grid
        
        # Elite population growth: E(t) = E0 * exp(f_E * t)
        E_path = self.E0 * np.exp(self.f_E * time_grid)
        
        # General biological age path: B_general(t) = B0 + v_general * t
        B_gen_path = self.B_general_0 + self.v_general * time_grid
        
        # Biological Gini: G_bio(t) = Delta(t) * E(t) / (B_general(t) * N_total)
        # Scaled to capture relative biological inequality density
        G_bio_path = (delta_path * E_path) / (B_gen_path * self.N_total)
        
        return {
            "time": time_grid,
            "delta_biological_gap": delta_path,
            "E_elite_count": E_path,
            "B_general_age": B_gen_path,
            "G_bio": G_bio_path,
            "delta_at_year_20": float(delta_path[int(20 / dt)]),
            "delta_at_year_50": float(delta_path[-1])
        }
