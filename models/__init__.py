"""
The Mathematical Basin: Thirteen Formal Models of Longevity Asymmetry and Systemic Lock-in
========================================================================================

Author: Gia Bao Huynh
ORCID: 0009-0008-2372-5852
Email: huynhbao@asu.edu
Research Stance: Challenging the unchecked power, epistemic asymmetries, and monopolized
governance of non-state actors across frontier technologies.
Collaborator: Claude (Anthropic)
Date: June 2026

Formal derivation from Huynh (2026a), "Till Death Tear Us Apart", Chapter IX.
"""

from .model01_basin_grievance import Model1BasinGrievance
from .model02_alrp_impossibility import Model2ALRPImpossibility
from .model03_lockin_chain import Model3LockinChain, Model3bMarieAntoinette
from .model04_epigenetic_divergence import Model4EpigeneticDivergence
from .model05_actuarial_collapse import Model5ActuarialCollapse
from .model06_legitimacy_dissolution import Model6LegitimacyDissolution, Model6bGovernanceEliteOverlap
from .model07_arsi_compounding import Model7ARSICompounding
from .model08_cost_diffusion import Model8CostDiffusion
from .model09_stratification_love import Model9StratificationLove
from .model10_composite_trajectory import Model10CompositeTrajectory
from .model11_dam_integrity import Model11DamIntegrity
from .model12_intra_elite_fracture import Model12IntraEliteFracture
from .model13_terminal_logic import Model13TerminalLogic
from .stability_lyapunov import LyapunovBasinStability

__all__ = [
    "Model1BasinGrievance",
    "Model2ALRPImpossibility",
    "Model3LockinChain",
    "Model3bMarieAntoinette",
    "Model4EpigeneticDivergence",
    "Model5ActuarialCollapse",
    "Model6LegitimacyDissolution",
    "Model6bGovernanceEliteOverlap",
    "Model7ARSICompounding",
    "Model8CostDiffusion",
    "Model9StratificationLove",
    "Model10CompositeTrajectory",
    "Model11DamIntegrity",
    "Model12IntraEliteFracture",
    "Model13TerminalLogic",
    "LyapunovBasinStability"
]
