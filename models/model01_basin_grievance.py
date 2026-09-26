"""
Model 1 — The Basin: A5 Grievance Accumulation
==============================================
Biological Zero-Day Jump Process, Social Media Amplification, and Love-Activation Field.

Governing equation:
    G(t) = k * D * \\int_0^t p(\\tau) * \\lambda_{threat} * e^{-\\lambda_{grief}(t - \\tau)} d\\tau + L_{love}(t)

Where:
    p(t) = p0 + \\sum_{i=1}^{N(t)} J_i * H(t - \\tau_i)   [Compound Poisson Jump Process]
    L_{love}(t) = \\alpha * k * N_{total} * p(t) * \\lambda_{threat} / (\\lambda_{grief} + \\alpha_e)

Core calibration:
    D = 165,000 deaths/day (UN WPP 2024 medium variant)
    p0 = 0.001
    \\lambda_{bz} = 0.5 year^-1 (two BZM events in 5 months: ER-100 Jan 2026, NewLimit Jun 2026)
    E[J_i] = \\mu_J = 0.008
    k = 6 (Dunbar/Fischer/Marsden intimate network)
    \\lambda_{grief} = 0.516 year^-1 (Bonanno 2004 resilience cohort; 35% non-decaying prolonged grief)
    \\lambda_{threat} = 0.15 year^-1 (Bowlby 1969/1973)
    \\alpha = 3.0 (social media amplification)
    G* = 2.0e9 (political activation threshold; reached at ~Year 23 under stochastic realization)
"""

import numpy as np
from typing import Dict, Tuple, Optional

class Model1BasinGrievance:
    def __init__(
        self,
        D: float = 165_000.0 * 365.25,  # Annualized global mortality
        p0: float = 0.001,
        lambda_bz: float = 0.5,
        mu_J: float = 0.008,
        k: float = 6.0,
        lambda_grief: float = 0.516,
        lambda_threat: float = 0.15,
        alpha: float = 3.0,
        alpha_e: float = 0.10,
        N_total: float = 8.1e9,
        prolonged_grief_fraction: float = 0.35,
        G_star: float = 2.0e9
    ):
        self.D = D
        self.p0 = p0
        self.lambda_bz = lambda_bz
        self.mu_J = mu_J
        self.k = k
        self.lambda_grief = lambda_grief
        self.lambda_threat = lambda_threat
        self.alpha = alpha
        self.alpha_e = alpha_e
        self.N_total = N_total
        self.prolonged_fraction = prolonged_grief_fraction
        self.G_star = G_star

    def expected_preventable_fraction(self, t: float) -> float:
        """E[p(t)] = p0 + lambda_bz * mu_J * t"""
        return self.p0 + self.lambda_bz * self.mu_J * t

    def love_activation_field(self, p_t: float) -> float:
        """L_love(t) = alpha * k * N_total * p(t) * lambda_threat / (lambda_grief + alpha_e)"""
        denom = self.lambda_grief + self.alpha_e
        return (self.alpha * self.k * self.N_total * p_t * self.lambda_threat) / denom

    def simulate_trajectory(
        self,
        t_max: float = 35.0,
        dt: float = 0.1,
        seed: Optional[int] = 42
    ) -> Dict[str, np.ndarray]:
        """
        Simulate the grievance trajectory G(t) taking into account:
        1. Resilient grief cohort (65%) with exponential decay lambda_grief
        2. Prolonged grief cohort (35%) without decay
        3. Love-Activation Field L_love(t)
        4. Compound Poisson jumps in p(t)
        """
        if seed is not None:
            np.random.seed(seed)

        time_grid = np.arange(0, t_max + dt, dt)
        n_steps = len(time_grid)

        # Generate BZM jumps
        p_path = np.zeros(n_steps)
        p_path[0] = self.p0
        
        current_p = self.p0
        for i in range(1, n_steps):
            n_jumps = np.random.poisson(self.lambda_bz * dt)
            if n_jumps > 0:
                jumps = np.random.exponential(self.mu_J, size=n_jumps)
                current_p += np.sum(jumps)
            p_path[i] = current_p

        f_norm = 1.0 - self.prolonged_fraction
        f_prol = self.prolonged_fraction

        G_accum = np.zeros(n_steps)
        grief_decaying = 0.0
        grief_permanent = 0.0

        for i in range(1, n_steps):
            inflow = self.k * self.D * p_path[i] * self.lambda_threat * dt
            grief_decaying = grief_decaying * np.exp(-self.lambda_grief * dt) + f_norm * inflow
            grief_permanent = grief_permanent + f_prol * inflow
            L_love = self.love_activation_field(p_path[i])
            G_accum[i] = grief_decaying + grief_permanent + L_love

        # Expected smooth trajectory
        expected_p = np.array([self.expected_preventable_fraction(t) for t in time_grid])
        expected_G = np.zeros(n_steps)
        exp_dec = 0.0
        exp_perm = 0.0
        for i in range(1, n_steps):
            inf = self.k * self.D * expected_p[i] * self.lambda_threat * dt
            exp_dec = exp_dec * np.exp(-self.lambda_grief * dt) + f_norm * inf
            exp_perm = exp_perm + f_prol * inf
            expected_G[i] = exp_dec + exp_perm + self.love_activation_field(expected_p[i])

        # Crossing year under stochastic jump realization
        crossing_stoch_idx = np.where(G_accum >= self.G_star)[0]
        crossing_year_stoch = time_grid[crossing_stoch_idx[0]] if len(crossing_stoch_idx) > 0 else None

        # Crossing year under continuous expected mean
        crossing_exp_idx = np.where(expected_G >= self.G_star)[0]
        crossing_year_exp = time_grid[crossing_exp_idx[0]] if len(crossing_exp_idx) > 0 else None

        return {
            "time": time_grid,
            "p_stochastic": p_path,
            "p_expected": expected_p,
            "G_stochastic": G_accum,
            "G_expected": expected_G,
            "G_star": self.G_star,
            "crossing_year": crossing_year_stoch,
            "crossing_year_expected": crossing_year_exp
        }
