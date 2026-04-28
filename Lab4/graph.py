import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data
df = pd.read_csv('outputs/results.csv')

# Separate sparse and dense
sparse = df[df['density'] == 'sparse'].copy()
dense = df[df['density'] == 'dense'].copy()

# Set up the plotting style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'dijkstra_array': '#e74c3c',
    'dijkstra_heap': '#3498db',
    'floyd_warshall': '#2ecc71'
}

# ============================================================================
# Plot 1: Sparse Graphs - Time vs Vertices
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(sparse['vertices'], sparse['dijkstra_array_ms'],
        marker='o', linewidth=2, markersize=8,
        color=colors['dijkstra_array'], label='Dijkstra Array O(V³)')

ax.plot(sparse['vertices'], sparse['dijkstra_heap_ms'],
        marker='s', linewidth=2, markersize=8,
        color=colors['dijkstra_heap'], label='Dijkstra Heap O(V²log V)')

ax.plot(sparse['vertices'], sparse['floyd_warshall_ms'],
        marker='^', linewidth=2, markersize=8,
        color=colors['floyd_warshall'], label='Floyd-Warshall O(V³)')

ax.set_xlabel('Number of Vertices (V)', fontsize=12, fontweight='bold')
ax.set_ylabel('Time (milliseconds)', fontsize=12, fontweight='bold')
ax.set_title('Algorithm Performance on Sparse Graphs (avg degree ≈ 8)',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/sparse_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Created: outputs/sparse_comparison.png")

# ============================================================================
# Plot 2: Dense Graphs - Time vs Vertices
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(dense['vertices'], dense['dijkstra_array_ms'],
        marker='o', linewidth=2, markersize=8,
        color=colors['dijkstra_array'], label='Dijkstra Array O(V³)')

ax.plot(dense['vertices'], dense['dijkstra_heap_ms'],
        marker='s', linewidth=2, markersize=8,
        color=colors['dijkstra_heap'], label='Dijkstra Heap O(V³log V)')

ax.plot(dense['vertices'], dense['floyd_warshall_ms'],
        marker='^', linewidth=2, markersize=8,
        color=colors['floyd_warshall'], label='Floyd-Warshall O(V³)')

ax.set_xlabel('Number of Vertices (V)', fontsize=12, fontweight='bold')
ax.set_ylabel('Time (milliseconds)', fontsize=12, fontweight='bold')
ax.set_title('Algorithm Performance on Dense Graphs (25% edge density)',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/dense_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Created: outputs/dense_comparison.png")

# ============================================================================
# Plot 3: Log-Log Scale - Shows algorithmic complexity trends
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Sparse - Log scale
ax1.loglog(sparse['vertices'], sparse['dijkstra_array_ms'],
           marker='o', linewidth=2, markersize=8,
           color=colors['dijkstra_array'], label='Dijkstra Array')

ax1.loglog(sparse['vertices'], sparse['dijkstra_heap_ms'],
           marker='s', linewidth=2, markersize=8,
           color=colors['dijkstra_heap'], label='Dijkstra Heap')

ax1.loglog(sparse['vertices'], sparse['floyd_warshall_ms'],
           marker='^', linewidth=2, markersize=8,
           color=colors['floyd_warshall'], label='Floyd-Warshall')

ax1.set_xlabel('Number of Vertices (V) [log scale]', fontsize=12, fontweight='bold')
ax1.set_ylabel('Time (ms) [log scale]', fontsize=12, fontweight='bold')
ax1.set_title('Sparse Graphs - Log-Log Scale', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, which='both')

# Dense - Log scale
ax2.loglog(dense['vertices'], dense['dijkstra_array_ms'],
           marker='o', linewidth=2, markersize=8,
           color=colors['dijkstra_array'], label='Dijkstra Array')

ax2.loglog(dense['vertices'], dense['dijkstra_heap_ms'],
           marker='s', linewidth=2, markersize=8,
           color=colors['dijkstra_heap'], label='Dijkstra Heap')

ax2.loglog(dense['vertices'], dense['floyd_warshall_ms'],
           marker='^', linewidth=2, markersize=8,
           color=colors['floyd_warshall'], label='Floyd-Warshall')

ax2.set_xlabel('Number of Vertices (V) [log scale]', fontsize=12, fontweight='bold')
ax2.set_ylabel('Time (ms) [log scale]', fontsize=12, fontweight='bold')
ax2.set_title('Dense Graphs - Log-Log Scale', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('outputs/loglog_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Created: outputs/loglog_comparison.png")

# ============================================================================
# Plot 4: Speedup Analysis - Heap vs Array
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Calculate speedups
sparse['heap_speedup'] = sparse['dijkstra_array_ms'] / sparse['dijkstra_heap_ms']
dense['heap_speedup'] = dense['dijkstra_array_ms'] / dense['dijkstra_heap_ms']

# Sparse speedup
ax1.plot(sparse['vertices'], sparse['heap_speedup'],
         marker='o', linewidth=2.5, markersize=10,
         color='#9b59b6', label='Heap vs Array Speedup')
ax1.axhline(y=1, color='red', linestyle='--', linewidth=2, alpha=0.7, label='No speedup (1x)')
ax1.fill_between(sparse['vertices'], 1, sparse['heap_speedup'],
                  alpha=0.2, color='#9b59b6')

ax1.set_xlabel('Number of Vertices (V)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Speedup Factor (x)', fontsize=12, fontweight='bold')
ax1.set_title('Sparse Graphs: Dijkstra Heap Speedup over Array',
              fontsize=13, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Dense speedup
ax2.plot(dense['vertices'], dense['heap_speedup'],
         marker='s', linewidth=2.5, markersize=10,
         color='#e67e22', label='Heap vs Array Speedup')
ax2.axhline(y=1, color='red', linestyle='--', linewidth=2, alpha=0.7, label='No speedup (1x)')
ax2.fill_between(dense['vertices'], dense['heap_speedup'], 1,
                  alpha=0.2, color='#e67e22')

ax2.set_xlabel('Number of Vertices (V)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Speedup Factor (x)', fontsize=12, fontweight='bold')
ax2.set_title('Dense Graphs: Dijkstra Heap Speedup over Array',
              fontsize=13, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/speedup_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Created: outputs/speedup_analysis.png")

# ============================================================================
# Plot 5: Combined Overview - All algorithms, both densities
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

# Sparse graphs (solid lines)
ax.plot(sparse['vertices'], sparse['dijkstra_array_ms'],
        marker='o', linewidth=2, markersize=7, linestyle='-',
        color=colors['dijkstra_array'], label='Sparse: Dijkstra Array')

ax.plot(sparse['vertices'], sparse['dijkstra_heap_ms'],
        marker='s', linewidth=2, markersize=7, linestyle='-',
        color=colors['dijkstra_heap'], label='Sparse: Dijkstra Heap')

ax.plot(sparse['vertices'], sparse['floyd_warshall_ms'],
        marker='^', linewidth=2, markersize=7, linestyle='-',
        color=colors['floyd_warshall'], label='Sparse: Floyd-Warshall')

# Dense graphs (dashed lines)
ax.plot(dense['vertices'], dense['dijkstra_array_ms'],
        marker='o', linewidth=2, markersize=7, linestyle='--',
        color=colors['dijkstra_array'], label='Dense: Dijkstra Array')

ax.plot(dense['vertices'], dense['dijkstra_heap_ms'],
        marker='s', linewidth=2, markersize=7, linestyle='--',
        color=colors['dijkstra_heap'], label='Dense: Dijkstra Heap')

ax.plot(dense['vertices'], dense['floyd_warshall_ms'],
        marker='^', linewidth=2, markersize=7, linestyle='--',
        color=colors['floyd_warshall'], label='Dense: Floyd-Warshall')

ax.set_xlabel('Number of Vertices (V)', fontsize=12, fontweight='bold')
ax.set_ylabel('Time (milliseconds)', fontsize=12, fontweight='bold')
ax.set_title('All-Pairs Shortest Path: Algorithm Performance Comparison',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='upper left', ncol=2)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/combined_overview.png', dpi=300, bbox_inches='tight')
print("✓ Created: outputs/combined_overview.png")

# ============================================================================
# Generate summary statistics
# ============================================================================
print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)

print("\nSparse Graphs - Final Graph (V=1680):")
print(f"  Dijkstra Array:    {sparse['dijkstra_array_ms'].iloc[-1]:>10.1f} ms")
print(f"  Dijkstra Heap:     {sparse['dijkstra_heap_ms'].iloc[-1]:>10.1f} ms  (↓ {sparse['heap_speedup'].iloc[-1]:.1f}x faster)")
print(f"  Floyd-Warshall:    {sparse['floyd_warshall_ms'].iloc[-1]:>10.1f} ms")

print("\nDense Graphs - Final Graph (V=1680):")
print(f"  Dijkstra Array:    {dense['dijkstra_array_ms'].iloc[-1]:>10.1f} ms")
print(f"  Dijkstra Heap:     {dense['dijkstra_heap_ms'].iloc[-1]:>10.1f} ms  (↓ {dense['heap_speedup'].iloc[-1]:.1f}x faster)")
print(f"  Floyd-Warshall:    {dense['floyd_warshall_ms'].iloc[-1]:>10.1f} ms")

print("\nKey Insights:")
print(f"  • Sparse graphs: Heap is {sparse['heap_speedup'].mean():.1f}x faster on average")
print(f"  • Dense graphs: Heap is {dense['heap_speedup'].mean():.1f}x faster on average")
print(f"  • Best for sparse: Dijkstra Heap ({sparse['dijkstra_heap_ms'].iloc[-1]:.0f} ms)")
print(f"  • Best for dense: Floyd-Warshall ({dense['floyd_warshall_ms'].iloc[-1]:.0f} ms)")

print("\n" + "="*70)
print("All plots saved to outputs/ directory")
print("="*70)