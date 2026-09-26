"""
Model 10 — Composite Lock-in Trajectory: Enhanced State Vector
==============================================================
Integrates all sub-systems into an 11-dimensional state vector:
    X+(t) = [
        A(t),          # 0: ARSI Frontier Capability Level
        L(t),          # 1: Longevity Frontier Capability Level
        \\Delta(t),     # 2: Biological Age Gap (epigenetic divergence)
        G_total(t),    # 3: Stock of Latent Political Grievance
        L_pol(t),      # 4: Institutional Legitimacy Index
        W(t),          # 5: Welfare Solvency Index
        E(t),          # 6: Enhanced Elite Population Count
        I_dam(t),      # 7: Dam Integrity Index (Mortality Equalizer)
        \\eta(t),       # 8: Symbol-Body Fusion Index (Marie Antoinette)
        C_love(t),     # 9: Love Commodification Index
        S_FM2(t)       # 10: FM2 Saturation Index (Regulatory Impairment)
    ]

Critical Inequality:
    dG_total/dt * (1 + C_love(t)) > dG_adapt^effective/dt * (1 - S_FM2(t))
    Demonstrates that the gap between grievance generation and institutional
    adaptive capacity widens monotonically over the window.
"""

import numpy as np
from typing import Dict, List, Tuple

class Model10CompositeTrajectory:
    def __init__(
        self,
        t_max: float = 30.0,
        dt: float = 0.1
    ):
        self.t_max = t_max
        self.dt = dt

    def simulate_state_vector(
        self,
        seed: int = 42
    ) -> Dict[str, np.ndarray]:
        """Integrate the coupled 11-dimensional dynamical system."""
        time_grid = np.arange(0, self.t_max + self.dt, self.dt)
        n_steps = len(time_grid)
        
        # State vector array: shape (n_steps, 11)
        X = np.zeros((n_steps, 11))
        
        # Initial conditions at t=0 (2026 baseline)
        X[0, 0] = 1.0       # A(0) = 1.0 (frontier baseline)
        X[0, 1] = 1.0       # L(0) = 1.0 (early reprogramming)
        X[0, 2] = 7.3       # Delta(0) = 7.3 biological years (Belsky 2022)
        X[0, 3] = 1.0e7     # G_total(0) initial grievance background
        X[0, 4] = 0.85      # L_pol(0) = 0.85
        X[0, 5] = 0.85      # W(0) = 0.85 trust fund baseline
        X[0, 6] = 10_000.0  # E(0) = 10,000 initial cohort
        X[0, 7] = 0.95      # I_dam(0) = 0.95
        X[0, 8] = 0.10      # eta(0)
        X[0, 9] = 250.0     # C_love(0) ≈ 250x median income
        X[0, 10] = 0.45     # S_FM2(0) ≈ 0.45 initial saturation
        
        left_side = np.zeros(n_steps)
        right_side = np.zeros(n_steps)
        critical_ratio = np.zeros(n_steps)
        
        for i in range(n_steps - 1):
            t = time_grid[i]
            x = X[i]
            
            A, L, delta, G, L_pol, W, E, I_dam, eta, C_love, S_FM2 = x
            
            # Sub-system dynamics
            # 0: dA/dt = r_A * A
            dA = 0.40 * A
            
            # 1: dL/dt = r_L * L * (1 + 0.2 * A)
            dL = 0.15 * L * (1.0 + 0.2 * A)
            
            # 2: dDelta/dt = 0.90 * (1.02 - 0.35) ≈ 0.60 yrs/yr
            ddelta = 0.60
            
            # 6: dE/dt = 0.02 * E
            dE = 0.02 * E
            
            # 7: dI_dam/dt = -0.05 * (E / 1e5) * I_dam
            dI_dam = -0.015 * (E / 10_000.0) * I_dam
            
            # 8: eta = delta * (E / 100_000) * (1 - L_pol)
            eta_val = delta * min(1.0, E / 50_000.0) * (1.0 - L_pol + 0.1)
            
            # 9: C_love dynamics (price remains sticky around $3M-$4M, median income slow)
            c_love_val = 250.0 * (1.0 + 0.02 * t)
            
            # 10: S_FM2 = tanh(Lambda / Lambda_crit), Lambda compounding with A
            Lambda_curr = 12.0 * (1.0 + 0.35 * A)
            S_FM2_val = np.tanh(Lambda_curr / 20.0)
            
            # 3: dG_total/dt
            # Grievance inflow amplified by preventable mortality awareness
            dG = (6.0 * 6e7 * 0.008 * 0.15 * (1.0 + 0.05 * t)) * (0.35 + 0.65 * np.exp(-0.516 * 0.5))
            
            # 5: dW/dt
            dW = -0.04 - 0.01 * (E / 10_000.0)
            
            # 4: dL_pol/dt
            sigma_eff = 0.02 * (1.0 + 0.5 * (E / 100_000.0))
            is_w_crit = 1.0 if W < 0.70 else 0.0
            dL_pol = -sigma_eff * delta * L_pol * (1.0 - L_pol) * (1.0 + 0.30 * is_w_crit)
            
            # Update next step
            X[i+1, 0] = A + dA * self.dt
            X[i+1, 1] = L + dL * self.dt
            X[i+1, 2] = delta + ddelta * self.dt
            X[i+1, 3] = G + dG * self.dt
            X[i+1, 4] = max(0.01, min(1.0, L_pol + dL_pol * self.dt))
            X[i+1, 5] = max(0.10, W + dW * self.dt)
            X[i+1, 6] = E + dE * self.dt
            X[i+1, 7] = max(0.01, I_dam + dI_dam * self.dt)
            X[i+1, 8] = eta_val
            X[i+1, 9] = c_love_val
            X[i+1, 10] = S_FM2_val
            
            # Evaluate Critical Inequality terms:
            # LHS: dG_total/dt * (1 + C_love)
            lhs = dG * (1.0 + c_love_val)
            # RHS: nominal governance capacity (normalized) * (1 - S_FM2)
            rhs = 1.0e8 * (1.0 - S_FM2_val)
            
            left_side[i] = lhs
            right_side[i] = rhs
            critical_ratio[i] = lhs / max(1.0, rhs)
            
        left_side[-1] = left_side[-2]
        right_side[-1] = right_side[-2]
        critical_ratio[-1] = critical_ratio[-2]
        
        return {
            "time": time_grid,
            "state_matrix": X,
            "A_frontier_capability": X[:, 0],
            "L_longevity_capability": X[:, 1],
            "delta_gap": X[:, 2],
            "G_grievance": X[:, 3],
            "L_pol_legitimacy": X[:, 4],
            "W_solvency": X[:, 5],
            "E_elite": X[:, 6],
            "I_dam": X[:, 7],
            "eta_fusion": X[:, 8],
            "C_love": X[:, 9],
            "S_FM2": X[:, 10],
            "critical_inequality_LHS": left_side,
            "critical_inequality_RHS": right_side,
            "critical_ratio": critical_ratio
        }
