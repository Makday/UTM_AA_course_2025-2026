import tkinter as tk
from collections import deque
import networkx as nx
import os

# ========================= CONFIG =========================
DELAY = 800  # milliseconds (default speed)
START_NODE = "0"
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 700
NODE_RADIUS = 25
# =========================================================

def read_adjacency_list(filename="inputs/input.txt"):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found!")
        print("Please create input/input.txt with adjacency list format.")
        exit(1)

    graph = {}
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            nodes = line.split()
            if not nodes:
                continue
            u = nodes[0]
            graph[u] = nodes[1:]
    return graph


class GraphVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-time BFS & DFS Visualization - Tkinter Canvas")

        self.adj_list = read_adjacency_list()
        print("Loaded nodes:", list(self.adj_list.keys()))

        self.G = nx.Graph()
        for u, neighbors in self.adj_list.items():
            self.G.add_node(u)
            for v in neighbors:
                if v not in self.G:
                    self.G.add_node(v)
                self.G.add_edge(u, v)

        self.pos = nx.spring_layout(self.G, seed=42, k=0.6, iterations=50)

        self.create_widgets()
        self.fit_graph_to_canvas()
        self.draw_static_graph()

        self.visited = set()
        self.traversal_order = []
        self.after_id = None
        self.is_running = False

    # ... [create_widgets, fit_graph_to_canvas, canvas_x, canvas_y, draw_static_graph, update_node_color, reset_highlights, reset remain unchanged] ...

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                                bg="#f8f9fa", highlightthickness=0)
        self.canvas.pack(pady=10, padx=10)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=8)

        tk.Button(control_frame, text="Start BFS", command=self.start_bfs, width=14, bg="#4CAF50", fg="white").grid(
            row=0, column=0, padx=6)
        tk.Button(control_frame, text="Start DFS", command=self.start_dfs, width=14, bg="#2196F3", fg="white").grid(
            row=0, column=1, padx=6)
        tk.Button(control_frame, text="Reset", command=self.reset, width=12).grid(row=0, column=2, padx=6)
        tk.Button(control_frame, text="Fit Graph", command=self.fit_graph_to_canvas).grid(row=0, column=3, padx=6)

        tk.Label(control_frame, text="Animation Speed:").grid(row=1, column=0, pady=(10, 0), sticky="w")
        self.speed_slider = tk.Scale(control_frame, from_=100, to=2000, orient=tk.HORIZONTAL,
                                     length=400, resolution=50)
        self.speed_slider.set(DELAY)
        self.speed_slider.grid(row=1, column=1, columnspan=3, pady=(10, 0))

        self.info_label = tk.Label(self.root, text="Ready - Click BFS or DFS to start",
                                   font=("Arial", 12, "bold"), fg="#333")
        self.info_label.pack(pady=5)

        self.order_label = tk.Label(self.root, text="Traversal Order: ",
                                    font=("Consolas", 11), anchor="w", justify="left", wraplength=900)
        self.order_label.pack(fill="x", padx=20, pady=5)

    def fit_graph_to_canvas(self):
        if not self.pos:
            return
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        width = max_x - min_x if max_x > min_x else 1
        height = max_y - min_y if max_y > min_y else 1
        scale_x = (CANVAS_WIDTH - 120) / width
        scale_y = (CANVAS_HEIGHT - 120) / height
        scale = min(scale_x, scale_y) * 0.95
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        self.offset_x = CANVAS_WIDTH / 2 - center_x * scale
        self.offset_y = CANVAS_HEIGHT / 2 - center_y * scale
        self.scale = scale

    def canvas_x(self, x):
        return self.offset_x + x * self.scale

    def canvas_y(self, y):
        return self.offset_y + y * self.scale

    def draw_static_graph(self):
        self.canvas.delete("all")
        for u, v in self.G.edges():
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            self.canvas.create_line(
                self.canvas_x(x1), self.canvas_y(y1),
                self.canvas_x(x2), self.canvas_y(y2),
                fill="#999999", width=2.5, tags="edge"
            )
        for node in self.G.nodes():
            x, y = self.pos[node]
            cx = self.canvas_x(x)
            cy = self.canvas_y(y)
            self.canvas.create_oval(
                cx - NODE_RADIUS, cy - NODE_RADIUS,
                cx + NODE_RADIUS, cy + NODE_RADIUS,
                fill="#a8d0ff", outline="#333", width=3, tags=f"node_{node}"
            )
            self.canvas.create_text(cx, cy, text=str(node),
                                    font=("Arial", 13, "bold"), fill="#000", tags=f"label_{node}")

    def update_node_color(self, node, color):
        items = self.canvas.find_withtag(f"node_{node}")
        if items:
            self.canvas.itemconfig(items[0], fill=color)

    def reset_highlights(self):
        for node in self.G.nodes():
            self.update_node_color(node, "#a8d0ff")

    def reset(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.is_running = False
        self.visited.clear()
        self.traversal_order.clear()
        self.reset_highlights()
        self.info_label.config(text="Reset - Choose BFS or DFS")
        self.order_label.config(text="Traversal Order: ")

    def start_bfs(self):
        self.reset()
        self.is_running = True
        self.info_label.config(text="Running BFS...", fg="#4CAF50")
        queue = deque([START_NODE])
        self.bfs_step(queue)

    def start_dfs(self):
        self.reset()
        self.is_running = True
        self.info_label.config(text="Running DFS...", fg="#2196F3")
        stack = [START_NODE]
        self.dfs_step(stack)

    # ==================== BFS with Orange ====================
    def bfs_step(self, queue):
        if not queue or not self.is_running:
            self.finish("BFS")
            return

        current = queue.popleft()
        if current in self.visited:
            self.root.after(10, lambda: self.bfs_step(queue))
            return

        self.visited.add(current)
        self.traversal_order.append(current)

        self.update_node_color(current, "red")           # Current node

        # Orange only for BFS frontier (Queue)
        for n in list(queue):
            if n not in self.visited:
                self.update_node_color(n, "orange")

        self.update_order_label("BFS")

        for neighbor in self.G.neighbors(current):
            if neighbor not in self.visited and neighbor not in queue:
                queue.append(neighbor)

        delay = self.speed_slider.get()
        self.after_id = self.root.after(delay, lambda: self.bfs_step(queue))

    # ==================== DFS WITHOUT Orange ====================
    def dfs_step(self, stack):
        if not stack or not self.is_running:
            self.finish("DFS")
            return

        current = stack.pop()
        if current in self.visited:
            self.root.after(10, lambda: self.dfs_step(stack))
            return

        self.visited.add(current)
        self.traversal_order.append(current)

        self.update_node_color(current, "red")   # Only red for current

        # NO orange for DFS
        # We only show current (red) and visited (green at the end)

        self.update_order_label("DFS")

        for neighbor in reversed(list(self.G.neighbors(current))):
            if neighbor not in self.visited:
                stack.append(neighbor)

        delay = self.speed_slider.get()
        self.after_id = self.root.after(delay, lambda: self.dfs_step(stack))

    def update_order_label(self, algo):
        order_str = " → ".join(map(str, self.traversal_order))
        self.order_label.config(text=f"{algo} Order: {order_str}")

    def finish(self, algo):
        self.is_running = False
        for node in self.visited:
            self.update_node_color(node, "limegreen")
        self.info_label.config(text=f"✓ {algo} Completed!", fg="#4CAF50")


# ====================== MAIN ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()