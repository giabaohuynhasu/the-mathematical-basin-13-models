"""
Master Runner for The Mathematical Basin (13 Models)
====================================================
Executes all 13 models, evaluates equilibrium thresholds, and saves
comprehensive simulation outputs to data/simulated_trajectories_master.csv.

Author: Gia Bao Huynh
ORCID: 0009-0008-2372-5852
Collaborator: Claude (Anthropic)
"""

import sys
import os
import pandas as pd
import numpy as np

# Ensure models can be imported
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

def run_master_pipeline():
    print("=" * 80)
    print("THE MATHEMATICAL BASIN: THIRTEEN FORMAL MODELS")
    print("Author: Gia Bao Huynh (ORCID: 0009-0008-2372-5852)")
    print("Stance: Challenging the unchecked power and epistemic asymmetries of non-state actors")
    print("=" * 80)

    # 1. Model 1
    print("\n--- Running Model 1: A5 Grievance Accumulation ---")
    m1 = Model1BasinGrievance()
    res1 = m1.simulate_trajectory(t_max=35.0, dt=0.1, seed=42)
    print(f"  Crossing Year (Stochastic): Year {res1['crossing_year']:.1f}")
    print(f"  G*(Year 23): {res1['G_stochastic'][int(23/0.1)]:.3e} (Threshold G* = {res1['G_star']:.1e})")

    # 2. Model 2
    print("\n--- Running Model 2: The Impossibility Lemma (ALRP) ---")
    m2 = Model2ALRPImpossibility()
    res2 = m2.evaluate_grid(resolution=50)
    print(f"  Intersection Area: {res2['intersection_area']} (Empty parameter space verified)")
    print(f"  Cost Floor to Median Income Ratio: {res2['cost_floor_ratio']:.1f}x")

    # 3. Model 3 & 3b
    print("\n--- Running Model 3 & 3b: Conditional Chain & Marie Antoinette Modifier ---")
    m3 = Model3LockinChain()
    p_dict = m3.calculate_probabilities()
    mc_dict = m3.simulate_monte_carlo(n_sims=100_000, seed=42)
    print(f"  Analytical: P(lock-in)={p_dict['P_lockin']:.4f}, P(F2)={p_dict['P_F2_exit']:.4f}, "
          f"P(Late Escape)={p_dict['P_late_escape']:.4f}, P(Early)={p_dict['P_early_resolution']:.4f}")
    print(f"  Monte Carlo (N=100k): P(lock-in)={mc_dict['MC_lockin']:.4f}, P(Late Escape)={mc_dict['MC_late_escape']:.4f}")

    m3b = Model3bMarieAntoinette()
    eta_yr20 = m3b.eta(delta=14.0)
    p4_mod = m3b.modified_p4(eta_yr20)
    print(f"  Marie Antoinette Modifier at Year 20: eta={eta_yr20:.1f}, p4={p4_mod:.4f}")

    # 4. Model 4
    print("\n--- Running Model 4: Epigenetic Divergence & Biological Gini ---")
    m4 = Model4EpigeneticDivergence(delta_0=7.3)
    res4 = m4.simulate_divergence(t_max=35.0, dt=0.5)
    print(f"  Delta(0) = {res4['delta_biological_gap'][0]:.1f} yrs (Belsky baseline)")
    print(f"  Delta(20) = {res4['delta_at_year_20']:.1f} yrs")
    print(f"  Biological Gini(35) = {res4['G_bio'][-1]:.4e}")

    # 5. Model 5
    print("\n--- Running Model 5: Actuarial Collapse ---")
    m5 = Model5ActuarialCollapse()
    time_5 = np.linspace(0, 30, 301)
    E_5 = 10_000 * np.exp(0.02 * time_5)
    delta_5 = 7.3 + 0.60 * time_5
    res5 = m5.simulate_actuarial_dynamics(E_5, delta_5, time_5)
    print(f"  Present Value per enhanced individual: ${res5['PV_unit']:,.0f}")
    print(f"  Welfare Solvency W(30): {res5['W_solvency'][-1]:.3f} (W_crit = {m5.W_crit})")
    print(f"  Institutional Legitimacy L_pol(30): {res5['L_pol'][-1]:.3f}")

    # 6. Model 6 & 6b
    print("\n--- Running Model 6 & 6b: Governance Legitimacy Dissolution ---")
    m6 = Model6LegitimacyDissolution()
    tau_crit = m6.theoretical_traversal_time()
    res6 = m6.simulate_automaton(time_5, delta_5)
    print(f"  Theoretical Phase 2 Traversal Time: {tau_crit:.2f} years")
    print(f"  Simulated Phase 2 Traversal Time: {res6['simulated_traversal_time']:.2f} years")
    m6b = Model6bGovernanceEliteOverlap()
    print(f"  Legitimacy sensitivity with complete overlap: sigma={m6b.sensitivity(1.0):.4f} (baseline {m6b.sigma_0:.4f})")

    # 7. Model 7
    print("\n--- Running Model 7: ARSI Compounding & FM2 Saturation ---")
    m7 = Model7ARSICompounding()
    res7 = m7.simulate_saturation(t_max=10.0, dt=0.1)
    print(f"  Resource Disparity Ratio rho: {m7.resource_disparity_ratio():.1f}x")
    print(f"  Square-Root Enforcement Capacity: {m7.square_root_enforcement_capacity():.3%}")
    print(f"  Year 2 FM2 Saturation S_FM2(2): {res7['year2_saturation']:.3f}")
    print(f"  Year 2 Effective Governance Capacity: {res7['year2_effective_capacity']:.3%}")

    # 8. Model 8
    print("\n--- Running Model 8: Longevity Cost Diffusion (Wright's Law) ---")
    m8 = Model8CostDiffusion()
    comp_tech = m8.compare_technologies()
    for tech, stats in comp_tech.items():
        print(f"  {tech:<35}: b={stats['b_exponent']:.2f}, -{stats['reduction_per_doubling']*100:.1f}%/doubling, "
              f"3yr={stats['years_at_3yr_doubling']:.1f}yr, 2yr={stats['years_at_2yr_doubling']:.1f}yr")

    # 9. Model 9
    print("\n--- Running Model 9: Stratification Reproduction Through Love ---")
    m9 = Model9StratificationLove()
    p_traj = m8.trajectory(0.15, 3.0, time_5)
    res9 = m9.simulate_dynamics(time_5, p_traj)
    print(f"  Love Commodification Index C_love(0): {res9['C_love_t0']:.1f}x median income")
    print(f"  Elite population at Year 100: {res9['E_100']:,.0f} individuals")

    # 10. Model 10
    print("\n--- Running Model 10: Composite Trajectory (11 State Variables) ---")
    m10 = Model10CompositeTrajectory(t_max=30.0, dt=0.1)
    res10 = m10.simulate_state_vector()
    print(f"  State matrix shape: {res10['state_matrix'].shape} (11 coupled variables)")
    print(f"  Critical Inequality Ratio (Year 30): {res10['critical_ratio'][-1]:.2f} (LHS > RHS)")

    # 11. Model 11
    print("\n--- Running Model 11: Dam Integrity Field ---")
    m11 = Model11DamIntegrity()
    res11 = m11.compute_integrity(time_5, E_5)
    print(f"  I_dam(0): {res11['I_dam'][0]:.3f} -> I_dam(30): {res11['I_dam'][-1]:.3f}")
    print(f"  p5 Capture Probability: {res11['p5_at_t0']:.3f} -> {res11['p5_final']:.3f} (approaching lock-in)")

    # 12. Model 12
    print("\n--- Running Model 12: Intra-Elite Fracture Field ---")
    m12 = Model12IntraEliteFracture()
    res12 = m12.simulate_fracture_dynamics(time_5)
    print(f"  Harmonic Mean Duration tau_frag: {res12['harmonic_mean_tau']:.2f} years")
    print(f"  Ratio kappa_F / lambda_F: {res12['kappa_over_lambda']:.2f}")

    # 13. Model 13
    print("\n--- Running Model 13: Terminal Logic Field ---")
    m13 = Model13TerminalLogic()
    omega_final = m13.compute_omega(L_pol_system=0.04, G_total=3.5e9, F_open_flags=[False, False, False, False])
    active_grammars = m13.evaluate_active_grammars(omega_final)
    print(f"  Terminal Logic Boundary Parameter Omega: {omega_final:.3f}")
    for name, thresh, is_act in active_grammars:
        print(f"    - {name:<15} (V_th={thresh:.2f}): {'ACTIVATED' if is_act else 'INACTIVE'}")

    # Stability & Lyapunov Proof
    print("\n--- Running Lyapunov Stability & Attractor Proof ---")
    lyap = LyapunovBasinStability()
    lyap_eval = lyap.evaluate_lyapunov(E=20_000, I_dam=0.75, L_pol=0.30)
    print(f"  V(x) = {lyap_eval['V']:.2f}")
    print(f"  V_dot(x) = {lyap_eval['V_dot']:.4f} (Strictly positive: {lyap_eval['strictly_positive']})")
    print(f"    - Term 1 (Elite expansion): +{lyap_eval['term1_elite_expansion']:.4f}")
    print(f"    - Term 2 (Dam erosion):     +{lyap_eval['term2_dam_erosion']:.4f}")
    print(f"    - Term 3 (Legitimacy decay): +{lyap_eval['term3_legitimacy_collapse']:.4f}")

    # Export master simulation dataset to CSV
    master_df = pd.DataFrame({
        "time_years": time_5,
        "A_frontier_ai": res10["A_frontier_capability"],
        "L_frontier_longevity": res10["L_longevity_capability"],
        "delta_biological_years": res10["delta_gap"],
        "G_grievance_stock": res10["G_grievance"],
        "L_pol_legitimacy": res10["L_pol_legitimacy"],
        "W_welfare_solvency": res10["W_solvency"],
        "E_enhanced_elite": res10["E_elite"],
        "I_dam_integrity": res10["I_dam"],
        "eta_marie_antoinette": res10["eta_fusion"],
        "C_love_commodification": res10["C_love"],
        "S_FM2_saturation": res10["S_FM2"],
        "p5_capture_probability": res11["p5_capture_probability"],
        "fracture_index": res12["fracture_index"]
    })

    out_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "simulated_trajectories_master.csv"))
    master_df.to_csv(out_csv, index=False)
    print(f"\n[OK] Master simulation dataset successfully written to {out_csv} ({len(master_df)} rows)")

if __name__ == "__main__":
    run_master_pipeline()
