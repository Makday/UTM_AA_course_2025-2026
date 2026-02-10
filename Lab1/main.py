import matplotlib.pyplot as plt
from pathlib import Path
import algorithms.dynamic_programming
import algorithms.recursive
import algorithms.matrix
import algorithms.fast_fourier
import algorithms.binet
import time

def measure(input_list, func, func_name, attempts=3):
    results = {val: [] for val in input_list}
    table_lines = []

    header = f"{'Attempt':<10}"
    for val in input_list:
        header += f"{val:<12}"
    table_lines.append(header)
    table_lines.append("-" * (10 + 18 * len(input_list)))

    for i in range(1, attempts + 1):
        row = f"{i:<10}"
        for val in input_list:
            start = time.time()
            func(val)
            elapsed = time.time() - start
            results[val].append(elapsed)
            row += f"{elapsed:<12.3f}"
        table_lines.append(row)

    table_text = "\n".join(table_lines)
    print(f"\n=== {func_name} ===")
    print(table_text)

    output_folder = Path("old_output")
    table_file = output_folder / f"{func_name}_results.txt"
    with open(table_file, "w") as f:
        f.write(f"Results for {func_name}\n")
        f.write("=" * 50 + "\n\n")
        f.write(table_text)

    means = [sum(times) / len(times) for times in results.values()]
    inputs = list(results.keys())

    plt.figure(figsize=(10, 6))
    plt.plot(inputs, means, marker='o', linewidth=2, markersize=8)
    plt.xlabel('Input Size', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title(f'{func_name} - Performance', fontsize=14)
    plt.grid(True, alpha=0.3)

    graph_file = output_folder / f"{func_name}.png"
    plt.savefig(graph_file, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"  → Table saved to: {table_file}")
    print(f"  → Graph saved to: {graph_file}")

    return results

with open("inputs/large_input.txt", "r") as f:
    data = f.read()
    large_input = [int(x.strip()) for x in data.split(",")]

with open("inputs/small_input.txt", "r") as f:
    data = f.read()
    small_input = [int(x.strip()) for x in data.split(",")]

folder = Path("old_output")
folder.mkdir(exist_ok=True)

algorithm_list = [
    (algorithms.dynamic_programming.fibonacci, "dynamic_programming", large_input),
    (algorithms.matrix.fibonacci, "matrix", large_input),
    (algorithms.fast_fourier.fibonacci, "fast_fourier", large_input),
    (algorithms.binet.fibonacci, "binet", large_input),
    (algorithms.recursive.fibonacci, "recursive", small_input)
]

for func, func_name, input_data in algorithm_list:
    measure(input_data, func, func_name, attempts=3)
    print("Finished measuring: " + func_name)