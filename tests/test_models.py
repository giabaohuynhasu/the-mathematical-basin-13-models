"""
Comprehensive Unit Test Suite for The Mathematical Basin (13 Models)
====================================================================
Tests every formal derivation, boundary condition, and empirical anchor from the monograph.
"""

import pytest
import numpy as np
import os
import sys

# Ensure models directory is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import (
    Model1BasinGrievance,
    Model2ALRPImpossibility,
    Model3LockinChain,
    Model3bMarieAntoinette,
    Model4EpigeneticDivergence,
    Model5ActuarialCollapse,
    Model6LegitimacyDissolution,
    Model6bGovernanceEliteOverlap,
    Model7ARSICompounding,
    Model8CostDiffusion,
    Model9StratificationLove,
    Model10CompositeTrajectory,
    Model11DamIntegrity,
    Model12IntraEliteFracture,
    Model13TerminalLogic,
    LyapunovBasinStability
)

def test_model1_basin_grievance():
    m1 = Model1BasinGrievance()
    res = m1.simulate_trajectory(t_max=35.0, dt=0.1, seed=42)
    
    assert res["crossing_year"] is not None
    # Central paper derivation: crosses G* around Year 21 - 25 (~Year 23)
    assert 20.0 <= res["crossing_year"] <= 25.0
    assert res["G_stochastic"][-1] > m1.G_star
    assert len(res["p_stochastic"]) == len(res["time"])


def test_model2_alrp_impossibility():
    m2 = Model2ALRPImpossibility()
    grid_res = m2.evaluate_grid(resolution=50)
    
    # Theorem: Intersection of safe governance and fast democratization is empty
    assert grid_res["intersection_area"] == 0.0
    # Cost floor ratio > 15x median income
    assert grid_res["cost_floor_ratio"] > 15.0


def test_model3_lockin_chain():
    m3 = Model3LockinChain()
    probs = m3.calculate_probabilities()
    
    assert np.isclose(probs["P_lockin"], 0.42, atol=0.01)
    assert np.isclose(probs["P_F2_exit"], 0.08, atol=0.01)
    assert np.isclose(probs["P_late_escape"], 0.27, atol=0.01)
    assert np.isclose(probs["P_early_resolution"], 0.23, atol=0.01)
    assert np.isclose(probs["sum"], 1.0, atol=1e-6)

    # Test Monte Carlo convergence
    mc = m3.simulate_monte_carlo(n_sims=50_000, seed=42)
    assert np.isclose(mc["MC_lockin"], 0.42, atol=0.02)
    assert np.isclose(mc["MC_sum"], 1.0, atol=1e-6)


def test_model3b_marie_antoinette():
    m3b = Model3bMarieAntoinette(p4_base=0.85, eta_crit=1.0)
    
    eta_0 = m3b.eta(delta=0.0)
    assert eta_0 == 0.0
    assert m3b.modified_p4(eta_0) == 0.85
    
    # At Year 20, delta ~ 14, eta exceeds eta_crit
    eta_high = m3b.eta(delta=14.0, L_vis=1.0, I_body=1.0)
    assert eta_high == 14.0
    assert m3b.modified_p4(eta_high) == 1.0


def test_model4_epigenetic_divergence():
    m4 = Model4EpigeneticDivergence(delta_0=7.3)
    res = m4.simulate_divergence(t_max=50.0, dt=0.5)
    
    # Belsky baseline
    assert res["delta_biological_gap"][0] == 7.3
    # Monotonically diverging
    assert res["delta_at_year_20"] > 15.0
    assert res["delta_at_year_50"] > 30.0
    assert np.all(np.diff(res["delta_biological_gap"]) > 0)


def test_model5_actuarial_collapse():
    m5 = Model5ActuarialCollapse(mu_b=30_000, r_discount=0.03)
    assert m5.present_value_per_enhanced() == 1_000_000.0
    
    time_grid = np.linspace(0, 30, 61)
    E_traj = 10_000 * np.exp(0.02 * time_grid)
    delta_traj = 7.3 + 0.60 * time_grid
    
    res = m5.simulate_actuarial_dynamics(E_traj, delta_traj, time_grid)
    # Trust fund depletes below W_crit
    assert np.min(res["W_solvency"]) < m5.W_crit
    # Legitimacy decays
    assert res["L_pol"][-1] < res["L_pol"][0]


def test_model6_legitimacy_dissolution():
    m6 = Model6LegitimacyDissolution(sigma_2=0.025)
    tau = m6.theoretical_traversal_time(delta_mean=4.5)
    # Monograph derivation: Delta t_crit ≈ 5.3 years
    assert np.isclose(tau, 5.33, atol=0.1)

    time_grid = np.linspace(0, 30, 301)
    delta_path = 7.3 + 0.60 * time_grid
    res = m6.simulate_automaton(time_grid, delta_path)
    assert res["phase2_start"] is not None
    assert res["phase3_start"] is not None
    assert res["phase3_start"] > res["phase2_start"]


def test_model6b_overlap():
    m6b = Model6bGovernanceEliteOverlap(sigma_0=0.02, chi=0.50)
    assert m6b.sensitivity(O_eg=0.0) == 0.02
    assert m6b.sensitivity(O_eg=1.0) == 0.03  # 50% increase


def test_model7_arsi_compounding():
    m7 = Model7ARSICompounding(hyperscaler_spend_b=725.0, enforcement_spend_b=1.0)
    assert m7.resource_disparity_ratio() == 725.0
    
    cap = m7.square_root_enforcement_capacity()
    # Monograph: (725)^(-1/2) ≈ 0.0371 ≈ 3.7%
    assert np.isclose(cap, 0.0371, atol=0.005)
    
    res = m7.simulate_saturation(t_max=5.0, dt=0.1)
    assert res["year2_saturation"] > 0.90


def test_model8_cost_diffusion():
    m8 = Model8CostDiffusion(P_initial=4_250_000, P_target=10_000, b_biologics=0.15)
    
    red = m8.cost_reduction_per_doubling(0.15)
    assert np.isclose(red, 0.0987, atol=0.005) # ~9.9%
    
    n_req = m8.required_doublings(0.15)
    assert np.isclose(n_req, 58.2, atol=0.5) # ~58.2 doublings
    
    t_3yr = m8.timeline_years(n_req, 3.0)
    t_2yr = m8.timeline_years(n_req, 2.0)
    assert np.isclose(t_3yr, 174.6, atol=1.5)
    assert np.isclose(t_2yr, 116.4, atol=1.5)


def test_model9_stratification_love():
    m9 = Model9StratificationLove(E0=10_000, f_E=0.01) # 1% net kinship expansion yields ~27,048
    assert np.isclose(m9.E0 * np.exp(m9.f_E * 100), 27_048, atol=150)
    
    c_love_0 = m9.love_commodification_index(4_250_000, 12_500)
    assert 140 <= c_love_0 <= 425


def test_model10_composite_trajectory():
    m10 = Model10CompositeTrajectory(t_max=25.0, dt=0.2)
    res = m10.simulate_state_vector()
    
    assert res["state_matrix"].shape[1] == 11
    # Critical inequality LHS > RHS over time
    assert res["critical_ratio"][-1] > 1.0


def test_model11_dam_integrity():
    m11 = Model11DamIntegrity(p5_base=0.72)
    time_grid = np.linspace(0, 30, 100)
    E_traj = 10_000 * np.exp(0.02 * time_grid)
    
    res = m11.compute_integrity(time_grid, E_traj)
    assert res["I_dam"][0] == 1.0
    assert res["I_dam"][-1] < 1.0
    assert res["p5_capture_probability"][-1] > 0.72


def test_model12_intra_elite_fracture():
    m12 = Model12IntraEliteFracture(kappa_F=0.15, lambda_F=0.05)
    # Ratio kappa / lambda = 3.0
    assert np.isclose(m12.kappa_F / m12.lambda_F, 3.0)
    
    # Harmonic mean of historical cases ≈ 6.5 - 6.7 years
    tau = m12.historical_harmonic_mean()
    assert 6.0 <= tau <= 7.0


def test_model13_terminal_logic():
    m13 = Model13TerminalLogic(G_star=2.0e9)
    
    # If any F exit is open, Omega = 0
    omega_open = m13.compute_omega(L_pol_system=0.10, G_total=3.0e9, F_open_flags=[False, True, False, False])
    assert omega_open == 0.0
    
    # When all F exits closed and G > G*
    omega_closed = m13.compute_omega(L_pol_system=0.05, G_total=3.0e9, F_open_flags=[False, False, False, False])
    assert omega_closed == 0.95
    
    # At Omega = 0.95, Walzerian Just War threshold (0.95) is reached
    active = m13.evaluate_active_grammars(omega_closed)
    assert all(is_act for _, _, is_act in active)


def test_lyapunov_basin_stability():
    lyap = LyapunovBasinStability()
    res = lyap.evaluate_lyapunov(E=15_000, I_dam=0.80, L_pol=0.40)
    
    assert res["strictly_positive"] is True
    assert res["V_dot"] > 0.0
    assert res["term1_elite_expansion"] > 0
    assert res["term2_dam_erosion"] > 0
    assert res["term3_legitimacy_collapse"] > 0
    
    eig_res = lyap.verify_absorbing_eigenvalues()
    assert eig_res["has_absorbing_eigenvalue"] is True
