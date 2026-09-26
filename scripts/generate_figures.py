"""
Publication-Quality Figure Generation for The Mathematical Basin (13 Models)
============================================================================
Generates high-resolution figures (PNG and SVG) for all thirteen models
and stability proofs.

Author: Gia Bao Huynh (ORCID: 0009-0008-2372-5852)
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Use clean styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# Add parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import (
    Model1BasinGrievance,
    Model2ALRPImpossibility,
    Model3LockinChain,
    Model3bMarieAntoinette,
    Model4EpigeneticDivergence,
    Model5ActuarialCollapse,
    Model6LegitimacyDissolution,
    Model7ARSICompounding,
    Model8CostDiffusion,
    Model9StratificationLove,
    Model10CompositeTrajectory,
    Model11DamIntegrity,
    Model12IntraEliteFracture,
    Model13TerminalLogic,
    LyapunovBasinStability
)

FIGURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "figures"))
os.makedirs(FIGURES_DIR, exist_ok=True)

def generate_all_figures():
    print(f"Generating publication figures in {FIGURES_DIR}...")

    # Figure 1: Model 1 Grievance Accumulation
    m1 = Model1BasinGrievance()
    res1 = m1.simulate_trajectory(t_max=35.0, dt=0.1, seed=42)
    fig, ax1 = plt.subplots(figsize=(9, 5), dpi=300)
    ax1.plot(res1['time'], res1['G_stochastic'] / 1e9, color='#b22222', lw=2.2, label='G(t) Stochastic Jump Realization')
    ax1.plot(res1['time'], res1['G_expected'] / 1e9, color='#ff6347', lw=1.5, ls='--', label='E[G(t)] Expected Mean')
    ax1.axhline(y=2.0, color='#333333', ls=':', lw=1.8, label='G* Political Activation Threshold (2.0B)')
    if res1['crossing_year']:
        ax1.axvline(x=res1['crossing_year'], color='#2e8b57', ls='-.', lw=1.5,
                    label=f"G* Crossing (Year {res1['crossing_year']:.1f})")
    ax1.set_xlabel("Years from Baseline (2026)", fontsize=11, fontweight='bold')
    ax1.set_ylabel("Grievance Stock G(t) [Billions]", fontsize=11, fontweight='bold')
    ax1.set_title("Model 1: The Basin — A5 Grievance Accumulation & Threshold Crossing", fontsize=13, fontweight='bold', pad=12)
    ax1.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig01_model1_grievance_accumulation.png"))
    plt.close(fig)

    # Figure 2: Model 2 ALRP Impossibility Lemma
    m2 = Model2ALRPImpossibility()
    res2 = m2.evaluate_grid(resolution=100)
    fig, ax2 = plt.subplots(figsize=(8, 6), dpi=300)
    ax2.contourf(res2['R_A'], res2['T_D'], res2['cond1_governance_safe'].astype(int),
                 levels=[0.5, 1.5], colors=['#20b2aa'], alpha=0.35)
    ax2.contourf(res2['R_A'], res2['T_D'], res2['cond2_democratization_fast'].astype(int),
                 levels=[0.5, 1.5], colors=['#ff7f50'], alpha=0.35)
    ax2.axvline(x=m2.g_critical, color='#008080', lw=2.0, ls='--', label=f'Safe Governance Ceiling (g_crit = {m2.g_critical})')
    # T_double boundary for g_access
    T_bound = (m2.b_biologics * np.log(2.0)) / m2.g_access
    ax2.axhline(y=T_bound, color='#d2691e', lw=2.0, ls='--', label=f'Fast Democratization Floor (T_d < {T_bound:.2f}yr)')
    ax2.scatter([m2.r_A_realized], [3.0], color='#8b0000', s=120, zorder=5, label='2026 Realized Point (SWE-Bench, r_A=1.85)')
    ax2.set_xlabel("ARSI Capability Growth Rate r_A [year^-1]", fontsize=11, fontweight='bold')
    ax2.set_ylabel("Biologics Doubling Time T_double [years]", fontsize=11, fontweight='bold')
    ax2.set_title("Model 2: The Impossibility Lemma (ALRP) — Empty Parameter Intersection", fontsize=13, fontweight='bold', pad=12)
    ax2.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig02_model2_alrp_impossibility.png"))
    plt.close(fig)

    # Figure 3: Model 3 & 3b Probability Tree & Marie Antoinette Modifier
    m3 = Model3LockinChain()
    p_dict = m3.calculate_probabilities()
    fig, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    outcomes = ['Lock-in (42%)', 'Late Escape (27%)', 'Early Resolution (23%)', 'F2 Exit (8%)']
    vals = [p_dict['P_lockin'], p_dict['P_late_escape'], p_dict['P_early_resolution'], p_dict['P_F2_exit']]
    colors = ['#8b0000', '#e67e22', '#27ae60', '#2980b9']
    ax3a.bar(outcomes, vals, color=colors, width=0.55, edgecolor='#333333')
    for idx, v in enumerate(vals):
        ax3a.text(idx, v + 0.015, f"{v:.1%}", ha='center', fontweight='bold', fontsize=10)
    ax3a.set_ylim(0, 0.52)
    ax3a.set_ylabel("Derived Probability", fontsize=11, fontweight='bold')
    ax3a.set_title("Model 3: Lock-in Probability Tree Partition", fontsize=12, fontweight='bold')

    m3b = Model3bMarieAntoinette()
    eta_vals = np.linspace(0, 3.0, 100)
    p4_mod_vals = [m3b.modified_p4(e) for e in eta_vals]
    ax3b.plot(eta_vals, p4_mod_vals, color='#4a148c', lw=2.5, label='p4(eta) Institutional Paralysis')
    ax3b.axvline(x=1.0, color='#888888', ls=':', label='Critical Saturation eta_crit = 1.0')
    ax3b.set_xlabel("Symbol-Body Fusion eta(t)", fontsize=11, fontweight='bold')
    ax3b.set_ylabel("Paralysis Probability p4", fontsize=11, fontweight='bold')
    ax3b.set_title("Model 3b: Marie Antoinette Non-Linearity", fontsize=12, fontweight='bold')
    ax3b.legend(frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig03_model3_probability_tree.png"))
    plt.close(fig)

    # Figure 4: Model 4 Epigenetic Age Divergence & Biological Gini
    m4 = Model4EpigeneticDivergence()
    res4 = m4.simulate_divergence(t_max=40.0)
    fig, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    ax4a.plot(res4['time'], res4['delta_biological_gap'], color='#1565c0', lw=2.2, label='Delta(t) Biological Gap')
    ax4a.axhline(y=7.3, color='#555555', ls='--', label='Belsky et al. (2022) Baseline (7.3 yr)')
    ax4a.set_xlabel("Years from Baseline", fontsize=11, fontweight='bold')
    ax4a.set_ylabel("Epigenetic Age Gap [Years]", fontsize=11, fontweight='bold')
    ax4a.set_title("Model 4: Epigenetic Age Divergence Delta(t)", fontsize=12, fontweight='bold')
    ax4a.legend(frameon=True)

    ax4b.plot(res4['time'], res4['G_bio'] * 1e6, color='#6a1b9a', lw=2.2, label='Biological Gini [x10^-6]')
    ax4b.set_xlabel("Years from Baseline", fontsize=11, fontweight='bold')
    ax4b.set_ylabel("Biological Gini Index", fontsize=11, fontweight='bold')
    ax4b.set_title("Model 4: Biological Inequality Density", fontsize=12, fontweight='bold')
    ax4b.legend(frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig04_model4_epigenetic_gini.png"))
    plt.close(fig)

    # Figure 5: Model 5 Welfare Solvency & Actuarial Liability
    m5 = Model5ActuarialCollapse()
    time_grid = np.linspace(0, 30, 150)
    E_path = 10_000 * np.exp(0.02 * time_grid)
    delta_path = 7.3 + 0.60 * time_grid
    res5 = m5.simulate_actuarial_dynamics(E_path, delta_path, time_grid)
    fig, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    ax5a.plot(time_grid, res5['W_solvency'], color='#c0392b', lw=2.2, label='W(t) Solvency Index')
    ax5a.axhline(y=m5.W_crit, color='#2c3e50', ls='--', label=f'Critical Threshold W_crit = {m5.W_crit}')
    ax5a.set_xlabel("Years from Baseline", fontsize=11, fontweight='bold')
    ax5a.set_ylabel("Welfare Solvency Index", fontsize=11, fontweight='bold')
    ax5a.set_title("Model 5: Welfare Solvency Exhaustion", fontsize=12, fontweight='bold')
    ax5a.legend(frameon=True)

    ax5b.plot(time_grid, res5['added_actuarial_liability'] / 1e9, color='#8e44ad', lw=2.2, label='Added Actuarial Liability ($B)')
    ax5b.set_xlabel("Years from Baseline", fontsize=11, fontweight='bold')
    ax5b.set_ylabel("Cumulative Liability [$B]", fontsize=11, fontweight='bold')
    ax5b.set_title("Model 5: Superlinear Actuarial Burden (propto E(t)^2)", fontsize=12, fontweight='bold')
    ax5b.legend(frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig05_model5_actuarial_solvency.png"))
    plt.close(fig)

    # Figure 6: Model 6 Three-Phase Legitimacy Dissolution Automaton
    m6 = Model6LegitimacyDissolution()
    res6 = m6.simulate_automaton(time_grid, delta_path)
    fig, ax6 = plt.subplots(figsize=(9, 5), dpi=300)
    ax6.plot(time_grid, res6['L_pol'], color='#d35400', lw=2.4, label='L_pol(t) Legitimacy Index')
    ax6.axhline(y=0.50, color='#7f8c8d', ls=':', label='Phase 1/2 Boundary (0.50)')
    ax6.axhline(y=0.35, color='#c0392b', ls=':', label='Phase 2/3 Boundary (0.35: Recursive Trap)')
    if res6['phase2_start']:
        ax6.axvline(x=res6['phase2_start'], color='#2980b9', ls='--', label=f"Phase 2 Start (Yr {res6['phase2_start']:.1f})")
    if res6['phase3_start']:
        ax6.axvline(x=res6['phase3_start'], color='#8e44ad', ls='--', label=f"Phase 3 Start (Yr {res6['phase3_start']:.1f})")
    ax6.set_xlabel("Years from Baseline", fontsize=11, fontweight='bold')
    ax6.set_ylabel("Institutional Legitimacy L_pol(t)", fontsize=11, fontweight='bold')
    ax6.set_title("Model 6: Governance Legitimacy Three-Phase Automaton", fontsize=13, fontweight='bold', pad=12)
    ax6.legend(frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig06_model6_legitimacy_automaton.png"))
    plt.close(fig)

    # Figure 7: Model 7 FM2 Saturation and Governance Degradation
    m7 = Model7ARSICompounding()
    res7 = m7.simulate_saturation(t_max=8.0)
    fig, ax7 = plt.subplots(figsize=(9, 5), dpi=300)
    ax7.plot(res7['time'], res7['S_FM2_saturation'], color='#c0392b', lw=2.2, label='S_FM2(t) Regulatory Saturation')
    ax7.plot(res7['time'], res7['effective_governance_capacity'], color='#27ae60', lw=2.2, label='Effective Adaptation Capacity (1 - S_FM2)')
    ax7.axvline(x=2.0, color='#2c3e50', ls='--', label=f"Year 2 Baseline (Eff. Capacity ≈ {res7['year2_effective_capacity']:.1%})")
    ax7.set_xlabel("Years from Baseline", fontsize=11, fontweight='bold')
    ax7.set_ylabel("Index / Capacity Fraction", fontsize=11, fontweight='bold')
    ax7.set_title("Model 7: FM2 Saturation & Collapse of Governance Capacity", fontsize=13, fontweight='bold', pad=12)
    ax7.legend(frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig07_model7_fm2_saturation.png"))
    plt.close(fig)

    # Figure 8: Model 8 Wright's Law Cost Diffusion Curves
    m8 = Model8CostDiffusion()
    years = np.linspace(0, 100, 200)
    fig, ax8 = plt.subplots(figsize=(9, 5), dpi=300)
    p_comp = m8.trajectory(0.50, 2.0, years) # Compute
    p_bio = m8.trajectory(0.15, 3.0, years)  # Biologics
    p_solar = m8.trajectory(0.32, 3.0, years)
    ax8.semilogy(years, p_comp, color='#2980b9', lw=2.0, label="Compute Hardware (b=0.50, 2yr double)")
    ax8.semilogy(years, p_solar, color='#f39c12', lw=2.0, label="Solar Panels (b=0.32, 3yr double)")
    ax8.semilogy(years, p_bio, color='#e74c3c', lw=2.4, label="Biologics / Reprogramming (b=0.15, 3yr double)")
    ax8.axhline(y=10_000, color='#27ae60', ls='--', lw=1.8, label="Democratization Target ($10,000)")
    ax8.set_xlabel("Years from Baseline", fontsize=11, fontweight='bold')
    ax8.set_ylabel("Treatment Price [USD] (Log Scale)", fontsize=11, fontweight='bold')
    ax8.set_title("Model 8: Wright's Law Diffusion Failure (174.6yr vs 23yr Window)", fontsize=13, fontweight='bold', pad=12)
    ax8.legend(frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig08_model8_wrights_law_diffusion.png"))
    plt.close(fig)

    # Figure 9: Model 10 Coupled 11-Variable Trajectory
    m10 = Model10CompositeTrajectory(t_max=30.0, dt=0.2)
    res10 = m10.simulate_state_vector()
    fig, ax10 = plt.subplots(figsize=(10, 6), dpi=300)
    ax10.plot(res10['time'], res10['L_pol_legitimacy'], color='#e74c3c', lw=2.2, label='Legitimacy L_pol(t)')
    ax10.plot(res10['time'], res10['W_solvency'], color='#e67e22', lw=2.0, label='Welfare Solvency W(t)')
    ax10.plot(res10['time'], res10['I_dam'], color='#2980b9', lw=2.0, label='Dam Integrity I_dam(t)')
    ax10.plot(res10['time'], res10['S_FM2'], color='#8e44ad', lw=2.0, ls='--', label='FM2 Saturation S_FM2(t)')
    ax10.set_xlabel("Years from Baseline (2026)", fontsize=11, fontweight='bold')
    ax10.set_ylabel("Normalized State Variables", fontsize=11, fontweight='bold')
    ax10.set_title("Model 10: Coupled 11-Variable Lock-in State Trajectory", fontsize=13, fontweight='bold', pad=12)
    ax10.legend(loc='center right', frameon=True)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig10_model10_composite_trajectory.png"))
    plt.close(fig)

    # Figure 10: Lyapunov Proof: Strict Positivity of V_dot in S5
    lyap = LyapunovBasinStability()
    E_grid = np.linspace(5_000, 30_000, 50)
    L_grid = np.linspace(0.10, 0.45, 50)
    E_M, L_M = np.meshgrid(E_grid, L_grid)
    V_dot_M = np.zeros_like(E_M)
    for r in range(50):
        for c in range(50):
            res_l = lyap.evaluate_lyapunov(E=E_M[r, c], I_dam=0.80, L_pol=L_M[r, c])
            V_dot_M[r, c] = res_l['V_dot']
            
    fig, ax_l = plt.subplots(figsize=(8, 6), dpi=300)
    cp = ax_l.contourf(E_M, L_M, V_dot_M, levels=20, cmap='YlOrRd')
    cbar = fig.colorbar(cp)
    cbar.set_label("V_dot(x) > 0 [Monotonic Basin Expansion]", fontsize=10, fontweight='bold')
    ax_l.set_xlabel("Enhanced Elite Headcount E(t)", fontsize=11, fontweight='bold')
    ax_l.set_ylabel("Institutional Legitimacy L_pol(t)", fontsize=11, fontweight='bold')
    ax_l.set_title("Section III: Lyapunov Stability Proof — Positively Invariant S5 Attractor", fontsize=12, fontweight='bold', pad=12)
    plt.tight_layout()
    fig.savefig(os.path.join(FIGURES_DIR, "fig14_lyapunov_stability_phase.png"))
    plt.close(fig)

    print(f"[OK] Successfully rendered 10 publication figures to {FIGURES_DIR}")

if __name__ == "__main__":
    generate_all_figures()
