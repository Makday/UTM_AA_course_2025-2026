import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data
df = pd.read_csv('outputs/results.csv')

# Separate sparse and dense graphs
sparse_df = df[df['density'] == 'sparse'].copy()
dense_df = df[df['density'] == 'dense'].copy()

# Create figure with subplots
fig = plt.figure(figsize=(16, 10))

# Plot 1: Sparse graphs - Time vs Vertices
ax1 = plt.subplot(2, 3, 1)
ax1.plot(sparse_df['vertices'], sparse_df['prim_ms'], 'o-', label='Prim', linewidth=2, markersize=6)
ax1.plot(sparse_df['vertices'], sparse_df['kruskal_ms'], 's-', label='Kruskal', linewidth=2, markersize=6)
ax1.set_xlabel('Vertices', fontsize=11)
ax1.set_ylabel('Time (ms)', fontsize=11)
ax1.set_title('Sparse Graphs: Time vs Vertices', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot 2: Dense graphs - Time vs Vertices
ax2 = plt.subplot(2, 3, 2)
ax2.plot(dense_df['vertices'], dense_df['prim_ms'], 'o-', label='Prim', linewidth=2, markersize=6)
ax2.plot(dense_df['vertices'], dense_df['kruskal_ms'], 's-', label='Kruskal', linewidth=2, markersize=6)
ax2.set_xlabel('Vertices', fontsize=11)
ax2.set_ylabel('Time (ms)', fontsize=11)
ax2.set_title('Dense Graphs: Time vs Vertices', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Time vs Edges (both densities)
ax3 = plt.subplot(2, 3, 3)
ax3.plot(sparse_df['edges'], sparse_df['prim_ms'], 'o-', label='Prim (Sparse)', linewidth=2, markersize=6)
ax3.plot(sparse_df['edges'], sparse_df['kruskal_ms'], 's-', label='Kruskal (Sparse)', linewidth=2, markersize=6)
ax3.plot(dense_df['edges'], dense_df['prim_ms'], 'o--', label='Prim (Dense)', linewidth=2, markersize=6)
ax3.plot(dense_df['edges'], dense_df['kruskal_ms'], 's--', label='Kruskal (Dense)', linewidth=2, markersize=6)
ax3.set_xlabel('Edges', fontsize=11)
ax3.set_ylabel('Time (ms)', fontsize=11)
ax3.set_title('Time vs Edges (All Graphs)', fontsize=12, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Log scale - Sparse graphs
ax4 = plt.subplot(2, 3, 4)
ax4.loglog(sparse_df['vertices'], sparse_df['prim_ms'], 'o-', label='Prim', linewidth=2, markersize=6)
ax4.loglog(sparse_df['vertices'], sparse_df['kruskal_ms'], 's-', label='Kruskal', linewidth=2, markersize=6)
ax4.set_xlabel('Vertices (log scale)', fontsize=11)
ax4.set_ylabel('Time (ms, log scale)', fontsize=11)
ax4.set_title('Sparse Graphs: Log-Log Scale', fontsize=12, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3, which='both')

# Plot 5: Log scale - Dense graphs
ax5 = plt.subplot(2, 3, 5)
ax5.loglog(dense_df['vertices'], dense_df['prim_ms'], 'o-', label='Prim', linewidth=2, markersize=6)
ax5.loglog(dense_df['vertices'], dense_df['kruskal_ms'], 's-', label='Kruskal', linewidth=2, markersize=6)
ax5.set_xlabel('Vertices (log scale)', fontsize=11)
ax5.set_ylabel('Time (ms, log scale)', fontsize=11)
ax5.set_title('Dense Graphs: Log-Log Scale', fontsize=12, fontweight='bold')
ax5.legend()
ax5.grid(True, alpha=0.3, which='both')

# Plot 6: Performance Ratio (Prim/Kruskal)
ax6 = plt.subplot(2, 3, 6)
# Avoid division by zero
sparse_ratio = sparse_df['prim_ms'] / sparse_df['kruskal_ms'].replace(0, np.nan)
dense_ratio = dense_df['prim_ms'] / dense_df['kruskal_ms'].replace(0, np.nan)

ax6.plot(sparse_df['vertices'], sparse_ratio, 'o-', label='Sparse', linewidth=2, markersize=6)
ax6.plot(dense_df['vertices'], dense_ratio, 's-', label='Dense', linewidth=2, markersize=6)
ax6.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='Equal Performance')
ax6.set_xlabel('Vertices', fontsize=11)
ax6.set_ylabel('Ratio (Prim/Kruskal)', fontsize=11)
ax6.set_title('Performance Ratio: Prim/Kruskal', fontsize=12, fontweight='bold')
ax6.legend()
ax6.grid(True, alpha=0.3)

plt.suptitle('MST Algorithm Performance Comparison: Prim vs Kruskal', 
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'benchmark_results.png'")

# Create additional individual plots for better detail

# Detailed sparse comparison
fig2, ax = plt.subplots(figsize=(10, 6))
ax.plot(sparse_df['vertices'], sparse_df['prim_ms'], 'o-', label='Prim', linewidth=2, markersize=8)
ax.plot(sparse_df['vertices'], sparse_df['kruskal_ms'], 's-', label='Kruskal', linewidth=2, markersize=8)
ax.set_xlabel('Number of Vertices', fontsize=12)
ax.set_ylabel('Execution Time (ms)', fontsize=12)
ax.set_title('Sparse Graphs: Prim vs Kruskal Performance', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('sparse_comparison.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'sparse_comparison.png'")

# Detailed dense comparison
fig3, ax = plt.subplots(figsize=(10, 6))
ax.plot(dense_df['vertices'], dense_df['prim_ms'], 'o-', label='Prim', linewidth=2, markersize=8)
ax.plot(dense_df['vertices'], dense_df['kruskal_ms'], 's-', label='Kruskal', linewidth=2, markersize=8)
ax.set_xlabel('Number of Vertices', fontsize=12)
ax.set_ylabel('Execution Time (ms)', fontsize=12)
ax.set_title('Dense Graphs: Prim vs Kruskal Performance', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dense_comparison.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'dense_comparison.png'")

# Summary statistics
print("\n" + "="*60)
print("PERFORMANCE SUMMARY")
print("="*60)
print("\nSparse Graphs:")
print(f"  Prim   - Mean: {sparse_df['prim_ms'].mean():.2f}ms, Max: {sparse_df['prim_ms'].max():.2f}ms")
print(f"  Kruskal - Mean: {sparse_df['kruskal_ms'].mean():.2f}ms, Max: {sparse_df['kruskal_ms'].max():.2f}ms")

print("\nDense Graphs:")
print(f"  Prim   - Mean: {dense_df['prim_ms'].mean():.2f}ms, Max: {dense_df['prim_ms'].max():.2f}ms")
print(f"  Kruskal - Mean: {dense_df['kruskal_ms'].mean():.2f}ms, Max: {dense_df['kruskal_ms'].max():.2f}ms")

print("\nFastest Algorithm by Graph Type:")
avg_sparse_prim = sparse_df['prim_ms'].mean()
avg_sparse_kruskal = sparse_df['kruskal_ms'].mean()
avg_dense_prim = dense_df['prim_ms'].mean()
avg_dense_kruskal = dense_df['kruskal_ms'].mean()

print(f"  Sparse: {'Kruskal' if avg_sparse_kruskal < avg_sparse_prim else 'Prim'} "
      f"({min(avg_sparse_prim, avg_sparse_kruskal):.2f}ms vs {max(avg_sparse_prim, avg_sparse_kruskal):.2f}ms)")
print(f"  Dense:  {'Kruskal' if avg_dense_kruskal < avg_dense_prim else 'Prim'} "
      f"({min(avg_dense_prim, avg_dense_kruskal):.2f}ms vs {max(avg_dense_prim, avg_dense_kruskal):.2f}ms)")
print("="*60)

plt.show()
