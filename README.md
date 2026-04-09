# Graph Coloring - Exam Scheduling Application

Comparative study of four graph coloring algorithms applied to university exam scheduling.
Vertices represent courses, edges represent student conflicts, and colors represent time slots.

---

## Algorithms

### Welsh-Powell
Greedy algorithm that sorts vertices by degree (descending) and assigns the lowest valid color to each.

**Time Complexity:** O(V log V + E) — O(V log V) for sorting vertices by degree, O(E) for the greedy coloring pass. Simplifies to O(V²) for dense graphs.

**Advantages**
- Fastest runtime of all four algorithms
- Simple to implement
- Scales to large graphs (tested up to n=150)

**Disadvantages / Limitations**
- Produces the most colors (worst solution quality)
- Static ordering — no adaptation during coloring
- No guarantee of optimality

---

### DSATUR
Greedy algorithm that dynamically selects the next vertex based on saturation degree (number of distinct colors in its neighborhood).

**Time Complexity:** O(V² + E) for the naive implementation — O(V) per step to select the highest-saturation vertex, plus O(E) total for saturation updates. A heap-based implementation reduces this to O((V + E) log V).

**Advantages**
- Best solution quality among all four algorithms
- Same asymptotic complexity as Welsh-Powell: O(V² + E)
- More effective at higher graph densities

**Disadvantages / Limitations**
- Slower than Welsh-Powell due to priority-based selection overhead
- Still not guaranteed to find the chromatic number
- Performance gap over Welsh-Powell narrows on sparse graphs

---

### Backtracking with Forward Checking
Exact search algorithm that tries color assignments recursively, pruning branches where any uncolored neighbor has no valid colors remaining. Vertices ordered by descending degree.

**Time Complexity:** O(V · k^V) in the worst case, where k is the greedy color upper bound. Forward checking reduces the effective branching factor in practice but cannot eliminate the exponential worst case.

**Advantages**
- Provides a certified feasible coloring
- Forward checking significantly reduces search space
- Correctness guarantee — never returns an invalid coloring

**Disadvantages / Limitations**
- Exponential worst-case complexity: O(k^V)
- Only feasible up to n ≈ 50
- In practice matched greedy color counts — does not improve solution quality without an optimization loop

---

### Simulated Annealing
Metaheuristic that starts from a random coloring and iteratively perturbs it, accepting worse solutions probabilistically based on a cooling temperature schedule.

**Time Complexity:** O(I · Δ_G), where I is the fixed iteration count (10,000) and Δ_G is the maximum degree. Simplifies to O(I · V) for dense graphs. The large constant I dominates in practice, making SA the slowest algorithm despite its relatively mild asymptotic growth.

**Advantages**
- Can theoretically escape local optima
- Tunable runtime via iteration count and cooling schedule
- Applicable to large graphs in principle

**Disadvantages / Limitations**
- Highest runtime of all four algorithms (315ms at n=50, p=0.5)
- Highly sensitive to hyperparameter configuration
- Did not improve over greedy baseline under tested settings (max_iter=10000, T₀=2.0, α=0.999)

---

## Experiments

All experiments run on Erdős–Rényi random graphs, averaged over 10 independent runs.

| Parameter | Values |
|---|---|
| Graph sizes (n) | 10, 20, 30, 50, 75, 100, 150 |
| Densities (p) | 0.2 (sparse), 0.5 (medium), 0.8 (dense) |
| BT / SA max size | n ≤ 50 |
| Runs per config | 10 |

### Comparisons carried out
- **Runtime vs graph size** at p=0.5, all 4 algorithms, log scale (Fig. 1)
- **Solution quality vs graph size** at p=0.5, all 4 algorithms (Fig. 2)
- **Solution quality vs graph density** at n=50, all 4 algorithms (Fig. 3)
- **Runtime vs graph density** at n=30, all 4 algorithms, log scale (Fig. 4)

---

## Results

- **DSATUR** achieves the best solution quality — consistently 10–15% fewer colors than Welsh-Powell across all sizes and densities.
- **Welsh-Powell** is the fastest algorithm by a large margin — up to 28× faster than DSATUR at n=150.
- **Backtracking** confirmed the greedy upper bound in all cases. Its exponential complexity limits it to n ≤ 50.
- **Simulated Annealing** had the highest runtime without improving solution quality under the tested configuration, highlighting its sensitivity to hyperparameter tuning.
- DSATUR's advantage over Welsh-Powell grows with graph density, suggesting saturation-based ordering is most effective in constrained, high-density graphs.

---

## How to Run

### Setup
```bash
pip install -r requirements.txt
```

### Step 1 — Run experiments
```bash
python run_experiments.py
```
Saves results to `results/experiments.csv`. Takes a few minutes due to BT/SA runs.

### Step 2 — Generate figures
```bash
python generate_figures.py
```
Saves all figures to `figures/`.

### Output files
| File | Description |
|---|---|
| `results/experiments.csv` | Raw metrics — colors used, runtime, success rate |
| `figures/fig1_runtime_vs_size.png` | Runtime vs vertices (p=0.5, log scale) |
| `figures/fig2_colors_vs_size.png` | Solution quality vs vertices (p=0.5) |
| `figures/fig3_colors_vs_density.png` | Solution quality vs density (n=50) |
| `figures/fig4_runtime_vs_density.png` | Runtime vs density (n=30, log scale) |

### Project structure
```
Graph-Coloring/
├── algorithms/
│   ├── welsh_powell.py
│   ├── dsatur.py
│   ├── backtracking.py
│   └── simulated_annealing.py
├── data/
│   └── graph_generator.py
├── results/
├── figures/
├── run_experiments.py
├── generate_figures.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Authors

- [Srijani Das](https://github.com/Srijani-Das07)
- [Hana Maria Philip](https://github.com/hana-20092006)
