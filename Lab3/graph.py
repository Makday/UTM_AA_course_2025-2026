import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Load data ──────────────────────────────────────────────
df = pd.read_csv("outputs/results.csv")

# Convert ns to ms for readability
ns_cols = [
    "dfs_adj_list_ns", "dfs_adj_matrix_ns", "dfs_edge_list_ns",
    "bfs_adj_list_ns", "bfs_adj_matrix_ns", "bfs_edge_list_ns"
]
ms_cols = [c.replace("_ns", "_ms") for c in ns_cols]
for ns, ms in zip(ns_cols, ms_cols):
    df[ms] = df[ns] / 1_000_000

sparse = df[df["density"] == "sparse"].sort_values("vertices")
dense  = df[df["density"] == "dense"].sort_values("vertices")

# ── Color + style scheme ───────────────────────────────────
COLORS = {
    "adj_list":   "#2196F3",   # blue
    "adj_matrix": "#F44336",   # red
    "edge_list":  "#4CAF50",   # green
}
STYLES = {
    "dfs": "-",
    "bfs": "--",
}
MARKERS = {
    "adj_list":   "o",
    "adj_matrix": "s",
    "edge_list":  "^",
}

# ── Helper ─────────────────────────────────────────────────
def plot_group(ax, data, algo, title):
    for rep in ["adj_list", "adj_matrix", "edge_list"]:
        col = f"{algo}_{rep}_ms"
        ax.plot(
            data["vertices"], data[col],
            label=rep.replace("_", " "),
            color=COLORS[rep],
            linestyle=STYLES[algo],
            marker=MARKERS[rep],
            markersize=5,
            linewidth=1.8,
        )
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel("Vertices (V)")
    ax.set_ylabel("Time (ms)")
    ax.legend(fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# ══════════════════════════════════════════════════════════
#  Figure 1 — DFS vs BFS per representation (sparse)
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("DFS vs BFS — Sparse Graphs", fontsize=13, fontweight="bold", y=1.01)

for ax, rep, label in zip(axes,
    ["adj_list", "adj_matrix", "edge_list"],
    ["Adjacency List", "Adjacency Matrix", "Edge List"]):

    for algo, ls in STYLES.items():
        col = f"{algo}_{rep}_ms"
        ax.plot(sparse["vertices"], sparse[col],
                label=algo.upper(),
                linestyle=ls,
                marker="o", markersize=5,
                linewidth=1.8)
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.set_xlabel("Vertices (V)")
    ax.set_ylabel("Time (ms)")
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

plt.tight_layout()
plt.savefig("outputs/fig1_dfs_vs_bfs_sparse.png", dpi=150, bbox_inches="tight")
print("Saved fig1_dfs_vs_bfs_sparse.png")

# ══════════════════════════════════════════════════════════
#  Figure 2 — DFS vs BFS per representation (dense)
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("DFS vs BFS — Dense Graphs", fontsize=13, fontweight="bold", y=1.01)

for ax, rep, label in zip(axes,
    ["adj_list", "adj_matrix", "edge_list"],
    ["Adjacency List", "Adjacency Matrix", "Edge List"]):

    for algo, ls in STYLES.items():
        col = f"{algo}_{rep}_ms"
        ax.plot(dense["vertices"], dense[col],
                label=algo.upper(),
                linestyle=ls,
                marker="o", markersize=5,
                linewidth=1.8)
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.set_xlabel("Vertices (V)")
    ax.set_ylabel("Time (ms)")
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

plt.tight_layout()
plt.savefig("outputs/fig2_dfs_vs_bfs_dense.png", dpi=150, bbox_inches="tight")
print("Saved fig2_dfs_vs_bfs_dense.png")

# ══════════════════════════════════════════════════════════
#  Figure 3 — All representations compared (DFS, sparse vs dense)
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("DFS — Sparse vs Dense: Representation Comparison",
             fontsize=13, fontweight="bold", y=1.01)

plot_group(axes[0], sparse, "dfs", "Sparse")
plot_group(axes[1], dense,  "dfs", "Dense")

plt.tight_layout()
plt.savefig("outputs/fig3_dfs_representations.png", dpi=150, bbox_inches="tight")
print("Saved fig3_dfs_representations.png")

# ══════════════════════════════════════════════════════════
#  Figure 4 — All representations compared (BFS, sparse vs dense)
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("BFS — Sparse vs Dense: Representation Comparison",
             fontsize=13, fontweight="bold", y=1.01)

plot_group(axes[0], sparse, "bfs", "Sparse")
plot_group(axes[1], dense,  "bfs", "Dense")

plt.tight_layout()
plt.savefig("outputs/fig4_bfs_representations.png", dpi=150, bbox_inches="tight")
print("Saved fig4_bfs_representations.png")

# ══════════════════════════════════════════════════════════
#  Figure 5 — Sparse vs Dense head-to-head (adj list only)
# ══════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Sparse vs Dense — Adjacency List",
             fontsize=13, fontweight="bold", y=1.01)

for ax, algo in zip(axes, ["dfs", "bfs"]):
    col = f"{algo}_adj_list_ms"
    ax.plot(sparse["vertices"], sparse[col], label="Sparse", marker="o", linewidth=1.8)
    ax.plot(dense["vertices"],  dense[col],  label="Dense",  marker="s", linewidth=1.8, linestyle="--")
    ax.set_title(algo.upper(), fontsize=11, fontweight="bold")
    ax.set_xlabel("Vertices (V)")
    ax.set_ylabel("Time (ms)")
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

plt.tight_layout()
plt.savefig("outputs/fig5_sparse_vs_dense_adjlist.png", dpi=150, bbox_inches="tight")
print("Saved fig5_sparse_vs_dense_adjlist.png")

print("\nAll figures saved to outputs/")