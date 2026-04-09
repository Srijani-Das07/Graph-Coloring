"""
generate_figures.py
Generates all 4 paper figures from results/experiments.csv.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
os.makedirs("figures", exist_ok=True)

df = pd.read_csv("results/experiments.csv")

def valid(data, col):
    """Filter rows where col has a real value (not None or -1)."""
    return data[data[col].notna() & (data[col] != -1)]


# Fig 1: Runtime vs Vertices, p=0.5, all 4 algos, log scale
d = df[df["density"] == 0.5]
plt.figure(figsize=(7, 4))
plt.plot(d["n"], d["wp_time_ms"], marker="o", label="Welsh-Powell")
plt.plot(d["n"], d["ds_time_ms"], marker="s", label="DSATUR")
v = valid(d, "bt_time_ms")
if not v.empty: plt.plot(v["n"], v["bt_time_ms"], marker="^", label="Backtracking")
v = valid(d, "sa_time_ms")
if not v.empty: plt.plot(v["n"], v["sa_time_ms"], marker="D", label="Simulated Annealing")
plt.yscale("log")
plt.xlabel("Number of Vertices")
plt.ylabel("Runtime (ms) — log scale")
plt.title("Runtime vs Graph Size (density = 0.5)")
plt.legend(); plt.tight_layout()
plt.savefig("figures/fig1_runtime_vs_size.png", dpi=300); plt.close()
print("Saved fig1")

# Fig 2: Colors used vs Vertices, p=0.5
d5 = df[df["density"] == 0.5]
plt.figure(figsize=(7, 4))
plt.plot(d5["n"], d5["wp_colors"], marker="o", label="Welsh-Powell", linewidth=3, linestyle="-", color="gold", zorder=1)
plt.plot(d5["n"], d5["ds_colors"], marker="s", label="DSATUR", linewidth=1.5, linestyle="--", zorder=2)
v = valid(d5, "sa_colors")
if not v.empty: plt.plot(v["n"], v["sa_colors"], marker="D", label="Simulated Annealing", linewidth=2, linestyle="-", color="red", zorder=4)
v = valid(d5, "bt_colors")
if not v.empty: plt.plot(v["n"], v["bt_colors"], marker="^", label="Backtracking", linewidth=2, linestyle=":", color="black", zorder=100)
plt.xlabel("Number of Vertices")
plt.ylabel("Colors Used")
plt.title("Solution Quality vs Graph Size (density = 0.5)")
plt.legend(); plt.tight_layout()
plt.savefig("figures/fig2_colors_vs_size.png", dpi=300); plt.close()
print("Saved fig2")

# Fig 3: Colors used vs Density, n=50
n50 = df[df["n"] == 50]
plt.figure(figsize=(7, 4))
plt.plot(n50["density"], n50["wp_colors"], marker="o", label="Welsh-Powell", linewidth=3, linestyle="-", color="gold", zorder=1)
plt.plot(n50["density"], n50["ds_colors"], marker="s", label="DSATUR", linewidth=1.5, linestyle="--", zorder=2)
v = valid(n50, "sa_colors")
if not v.empty: plt.plot(v["density"], v["sa_colors"], marker="D", label="Simulated Annealing", linewidth=1, linestyle="--", color="red", zorder=10)
v = valid(n50, "bt_colors")
if not v.empty: plt.plot(v["density"], v["bt_colors"], marker="^", label="Backtracking", linewidth=3, linestyle=":", color="black", zorder=3)
plt.xlabel("Graph Density")
plt.ylabel("Colors Used")
plt.title("Solution Quality vs Graph Density (n = 50)")
plt.legend(); plt.tight_layout()
plt.savefig("figures/fig3_colors_vs_density.png", dpi=300); plt.close()
print("Saved fig3")

# Fig 4: Runtime vs Density, n=30, log scale
n30 = df[df["n"] == 30]
plt.figure(figsize=(7, 4))
plt.plot(n30["density"], n30["wp_time_ms"], marker="o", label="Welsh-Powell")
plt.plot(n30["density"], n30["ds_time_ms"], marker="s", label="DSATUR")
v = valid(n30, "bt_time_ms")
if not v.empty: plt.plot(v["density"], v["bt_time_ms"], marker="^", label="Backtracking")
v = valid(n30, "sa_time_ms")
if not v.empty: plt.plot(v["density"], v["sa_time_ms"], marker="D", label="Simulated Annealing")
plt.yscale("log")
plt.xlabel("Graph Density")
plt.ylabel("Runtime (ms) — log scale")
plt.title("Runtime vs Graph Density (n = 30)")
plt.legend(); plt.tight_layout()
plt.savefig("figures/fig4_runtime_vs_density.png", dpi=300); plt.close()
print("Saved fig4")

print("\nAll figures saved → figures/")