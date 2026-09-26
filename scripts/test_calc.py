import sys, os
sys.path.insert(0, r'c:\Users\nswcl\.gemini\antigravity-ide\scratch\the-mathematical-basin-13-models')
from models.model01_basin_grievance import Model1BasinGrievance

m1 = Model1BasinGrievance()
res = m1.simulate_trajectory(t_max=35.0, dt=0.1, seed=42)
print("Crossing year:", res["crossing_year"])
for yr in [5, 10, 15, 20, 23, 25]:
    idx = int(yr / 0.1)
    g_exp = res["G_expected"][idx]
    g_sto = res["G_stochastic"][idx]
    p_exp = res["p_expected"][idx]
    print(f"Year {yr}: G_exp = {g_exp:.3e}, G_stoch = {g_sto:.3e}, p_exp = {p_exp:.4f}")
