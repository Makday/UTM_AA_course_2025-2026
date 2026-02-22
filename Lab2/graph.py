import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("outputs/benchmark.txt")

algorithms  = df.algorithm.unique()
input_types = df.input_type.unique()

styles = {
    "random":  {"color": "#4ecdc4", "linestyle": "-",  "marker": "o"},
    "sorted":  {"color": "#ff6b35", "linestyle": "--", "marker": "s"},
    "reverse": {"color": "#a78bfa", "linestyle": ":",  "marker": "^"},
}

for algo in algorithms:
    fig, ax = plt.subplots(figsize=(10, 6))

    for input_type in input_types:
        subset = df[(df["algorithm"] == algo) & (df["input_type"] == input_type)]
        s = styles[input_type]
        ax.plot(
            subset["size"], subset["time_ns"],
            label=input_type,
            color=s["color"],
            linestyle=s["linestyle"],
            marker=s["marker"],
            markersize=4,
            linewidth=2
        )

    ax.set_title(f"{algo} — Time vs Input Size", fontsize=14, fontweight="bold")
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Time (ns)", fontsize=12)
    ax.legend(title="Input Type", fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"outputs/{algo}.png", dpi=150)
    plt.show()