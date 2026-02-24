import matplotlib
matplotlib.use("TkAgg")  # use "Qt5Agg" if you have PyQt5 instead
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import matplotlib.collections as mc
import numpy as np
import sys

# ── CONFIG ───────────────────────────────────────────────────────────────────
FILE        = "outputs/animations.txt"
INTERVAL_MS = 1
FRAME_SKIP  = 1        # increase to 2/3/5 for very large arrays
ALGO_ORDER  = ["QUICKSORT", "MERGESORT", "HEAPSORT", "RADIXSORT"]

COLOR_DEFAULT = np.array([0.878, 0.878, 0.878, 1.0])  # white-ish
COLOR_CHANGED = np.array([0.906, 0.298, 0.235, 1.0])  # red
COLOR_DONE    = np.array([0.180, 0.800, 0.443, 1.0])  # green

# ── PARSE FILE ────────────────────────────────────────────────────────────────
def parse_file(path):
    sections = {}
    current  = None
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if parts[0] in ALGO_ORDER:
                current = parts[0]
                sections[current] = []
            elif current:
                sections[current].append(np.array(list(map(int, parts)), dtype=np.int32))
    return sections

# ── MAKE SEGMENTS — defined outside loop, no closure issues ──────────────────
def make_segments(heights):
    n = len(heights)
    # each bar = vertical line from (x, 0) to (x, h)
    segs = np.zeros((n, 2, 2), dtype=np.float64)
    segs[:, 0, 0] = np.arange(n)   # x start
    segs[:, 0, 1] = 0.0            # y start
    segs[:, 1, 0] = np.arange(n)   # x end
    segs[:, 1, 1] = heights         # y end  ← the height
    return segs

# ── MAIN ──────────────────────────────────────────────────────────────────────
try:
    sections = parse_file(FILE)
except FileNotFoundError:
    print(f"Error: '{FILE}' not found.")
    sys.exit(1)

present = [a for a in ALGO_ORDER if a in sections]
n_algos = len(present)

if n_algos == 0:
    print("No algorithm data found.")
    sys.exit(1)

# ── FIGURE SETUP ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(5 * n_algos, 5), facecolor="#0d0d0d")
fig.suptitle(
    "Sorting Algorithm Visualizer   |   R = restart",
    fontsize=13, fontweight="bold", color="white", y=0.98
)

gs   = gridspec.GridSpec(1, n_algos, figure=fig)
axes = [fig.add_subplot(gs[0, i]) for i in range(n_algos)]

for ax in axes:
    ax.set_facecolor("#111111")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")

# ── FULLSCREEN ────────────────────────────────────────────────────────────────
manager = plt.get_current_fig_manager()
try:
    manager.full_screen_toggle()
except Exception:
    try:
        manager.window.showMaximized()
    except Exception:
        pass

# ── PRECOMPUTE frames ─────────────────────────────────────────────────────────
max_frames = max(len(sections[a]) for a in present)
frame_indices = list(range(0, max_frames, FRAME_SKIP))
if frame_indices[-1] != max_frames - 1:
    frame_indices.append(max_frames - 1)

# ── BUILD LineCollections ─────────────────────────────────────────────────────
algo_data   = []
collections = []
step_texts  = []

for i, algo in enumerate(present):
    ax     = axes[i]
    frames = sections[algo]
    n      = len(frames[0])

    # normalize all frames to [0, 1]
    all_vals   = np.concatenate(frames)
    vmin, vmax = float(all_vals.min()), float(all_vals.max())
    span       = max(vmax - vmin, 1.0)

    normed = [((f.astype(np.float64) - vmin) / span) for f in frames]

    # initial segments and colors
    init_segs   = make_segments(normed[0])
    init_colors = np.tile(COLOR_DEFAULT, (n, 1))

    lc = mc.LineCollection(
        init_segs,
        colors=init_colors,
        linewidths=2.0     # fixed width — safe before render
    )
    ax.add_collection(lc)

    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, 1.05)
    ax.set_title(algo, color="white", fontsize=11, fontweight="bold", pad=8)
    ax.set_xticks([])
    ax.set_yticks([])

    step_text = ax.text(
        0.98, 0.02, "step 0",
        transform=ax.transAxes,
        color="#555555", fontsize=8,
        ha="right", va="bottom",
        fontfamily="monospace"
    )

    algo_data.append({
        "frames": frames,
        "normed": normed,
        "n":      n,
        "total":  len(frames),
    })
    collections.append(lc)
    step_texts.append(step_text)

# ── INIT ──────────────────────────────────────────────────────────────────────
def init():
    for lc, txt, d in zip(collections, step_texts, algo_data):
        lc.set_segments(make_segments(d["normed"][0]))
        lc.set_colors(np.tile(COLOR_DEFAULT, (d["n"], 1)))
        txt.set_text("step 0")
        txt.set_color("#555555")
    return collections + step_texts

# ── UPDATE ────────────────────────────────────────────────────────────────────
def update(fi):
    for lc, txt, d in zip(collections, step_texts, algo_data):
        total = d["total"]
        idx   = min(fi, total - 1)
        done  = (idx == total - 1)

        curr_norm = d["normed"][idx]
        curr_raw  = d["frames"][idx]
        prev_raw  = d["frames"][idx - 1] if idx > 0 else curr_raw

        changed_mask = (curr_raw != prev_raw)

        colors = np.tile(COLOR_DEFAULT, (d["n"], 1))
        if done:
            colors[:] = COLOR_DONE
        else:
            colors[changed_mask] = COLOR_CHANGED

        lc.set_segments(make_segments(curr_norm))
        lc.set_colors(colors)

        txt.set_text(f"step {idx}/{total - 1}")
        txt.set_color("#2ecc71" if done else "#555555")

    return collections + step_texts

# ── ANIMATION ─────────────────────────────────────────────────────────────────
ani = animation.FuncAnimation(
    fig,
    update,
    init_func=init,
    frames=frame_indices,
    interval=INTERVAL_MS,
    blit=True,
    repeat=False
)

# ── KEY HANDLER — R to restart ────────────────────────────────────────────────
def on_key(event):
    if event.key == "r":
        ani.frame_seq = iter(frame_indices)
        ani.event_source.stop()
        init()
        fig.canvas.draw()
        ani.event_source.start()

fig.canvas.mpl_connect("key_press_event", on_key)

plt.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.03, wspace=0.2)
plt.show()