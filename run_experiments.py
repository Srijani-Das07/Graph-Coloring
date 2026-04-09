"""
run_experiments.py
Runs all 4 algorithms. WP/DSATUR run on n=10–150. BT/SA capped at n=50.
Averages over 10 runs. Saves to results/experiments.csv.
"""
import sys
import os
sys.path.append(".")

import pandas as pd
from data.graph_generator import generate_random_graph
from algorithms.welsh_powell import run as wp_run
from algorithms.dsatur import run as dsatur_run
from algorithms.backtracking import run as bt_run
from algorithms.simulated_annealing import run as sa_run

WP_DS_SIZES = [10, 20, 30, 50, 75, 100, 150]
BT_SA_SIZES = [10, 20, 30, 50]
DENSITIES   = [0.2, 0.5, 0.8]
RUNS        = 10

results = []

for p in DENSITIES:
    for n in sorted(set(WP_DS_SIZES + BT_SA_SIZES)):
        do_bt_sa = n in BT_SA_SIZES
        wp_c, wp_t = [], []
        ds_c, ds_t = [], []
        bt_c, bt_t, bt_s = [], [], []
        sa_c, sa_t = [], []

        for seed in range(RUNS):
            G = generate_random_graph(n, p, seed=seed)

            _, wc, wt = wp_run(G);   wp_c.append(wc); wp_t.append(wt)
            _, dc, dt = dsatur_run(G); ds_c.append(dc); ds_t.append(dt)

            if do_bt_sa:
                _, bc, bt = bt_run(G)
                bt_c.append(bc if bc is not None else -1)
                bt_t.append(bt)
                bt_s.append(1 if bc is not None else 0)

                _, sc, st = sa_run(G, max_iter=3000)
                sa_c.append(sc); sa_t.append(st)

        avg = lambda l: sum(l) / len(l)

        row = {
            "n":          n,
            "density":    p,
            "wp_colors":  avg(wp_c),
            "wp_time_ms": avg(wp_t),
            "ds_colors":  avg(ds_c),
            "ds_time_ms": avg(ds_t),
            "bt_colors":  avg(bt_c)  if do_bt_sa else None,
            "bt_time_ms": avg(bt_t)  if do_bt_sa else None,
            "bt_success": avg(bt_s)  if do_bt_sa else None,
            "sa_colors":  avg(sa_c)  if do_bt_sa else None,
            "sa_time_ms": avg(sa_t)  if do_bt_sa else None,
        }
        results.append(row)

        line = (f"n={n:3d} p={p} | WP:{row['wp_colors']:.1f}c {row['wp_time_ms']:.2f}ms"
                f" | DS:{row['ds_colors']:.1f}c {row['ds_time_ms']:.2f}ms")
        if do_bt_sa:
            line += (f" | BT:{'OK' if row['bt_success'] > 0.5 else 'FAIL'} {row['bt_time_ms']:.2f}ms"
                     f" | SA:{row['sa_colors']:.1f}c {row['sa_time_ms']:.2f}ms")
        print(line)

os.makedirs("results", exist_ok=True)
pd.DataFrame(results).to_csv("results/experiments.csv", index=False)
print("\nSaved → results/experiments.csv")