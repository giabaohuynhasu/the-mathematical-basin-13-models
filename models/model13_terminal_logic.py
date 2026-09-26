"""
Model 13 — Terminal Logic Field
===============================
Boundary condition analysis specifying what grammars of action become structurally available
when the predictive architecture has exhausted its exit pathways.

Formula:
    \\Omega(t) = [1 - L_pol^system(t)] * \\Theta(G_total(t) - G*) * \\prod_{i=1}^4 (1 - F_i(t))

Where:
    \\Omega(t) approaches 1.0 when:
    1. Institutional legitimacy approaches zero (L_pol -> 0);
    2. Grievance stock exceeds political activation threshold (G_total >= G*);
    3. Falsification exits F1-F4 are evaluated and found closed.

Ordering of Grammar Activation Thresholds:
    V_S (0.65: Sorelian mythic strike)
    < V_B (0.80: Benjaminian divine violence / pure strike)
    < V_F (0.85: Fanonian decolonial counter-violence)
    < V_D (0.90: Islamic Darura jurisprudential necessity)
    < V_J (0.95: Walzerian Just War last-resort armed defense)
"""

import numpy as np
from typing import Dict, List, Tuple

class Model13TerminalLogic:
    def __init__(
        self,
        G_star: float = 2.0e9,
        thresholds: Dict[str, float] = None
    ):
        self.G_star = G_star
        if thresholds is None:
            self.thresholds = {
                "Sorelian": 0.65,
                "Benjaminian": 0.80,
                "Fanonian": 0.85,
                "Darura": 0.90,
                "Just_War": 0.95
            }
        else:
            self.thresholds = thresholds

    def compute_omega(
        self,
        L_pol_system: float,
        G_total: float,
        F_open_flags: List[bool]
    ) -> float:
        """
        Compute Omega(t) = (1 - L_pol) * Theta(G - G*) * Prod(1 - F_i)
        Where F_open_flags indicates whether an exit F_i remains open (True) or closed (False).
        """
        # If any exit remains genuinely open, the lock-in closure is incomplete
        if any(F_open_flags):
            return 0.0
            
        # Heaviside Theta
        heaviside = 1.0 if G_total >= self.G_star else 0.0
        
        omega = (1.0 - np.clip(L_pol_system, 0.0, 1.0)) * heaviside
        return float(omega)

    def evaluate_active_grammars(self, omega_val: float) -> List[Tuple[str, float, bool]]:
        """Determine which resistance action grammars are activated at given Omega."""
        active = []
        for grammar, threshold in self.thresholds.items():
            is_active = omega_val >= threshold
            active.append((grammar, threshold, is_active))
        return active
