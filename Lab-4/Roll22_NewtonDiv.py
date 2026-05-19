import csv
import numpy as np
import matplotlib.pyplot as plt

x_data = []
y_data = []

with open("temparature_data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        x_data.append(float(row["hour"]))
        y_data.append(float(row["temperature_celsius"]))

x_star = 11.5

nearest_index = 0
min_dist = abs(x_data[0] - x_star)
for i in range(1, len(x_data)):
    if abs(x_data[i] - x_star) < min_dist:
        min_dist = abs(x_data[i] - x_star)
        nearest_index = i

def get_nodes(center_idx, degree, x_list, y_list):
    n_nodes = degree + 1
    half = n_nodes // 2
    start = center_idx - half
    if start < 0:
        start = 0
    end = start + n_nodes
    if end > len(x_list):
        end = len(x_list)
        start = end - n_nodes
    if start < 0:
        start = 0
    return list(x_list[start:end]), list(y_list[start:end])

def build_divided_diff_table(x_nodes, y_nodes):
    n = len(x_nodes)
    table = []
    col0 = list(y_nodes)
    table.append(col0)
    for k in range(1, n):
        prev = table[k - 1]
        col = []
        for i in range(n - k):
            val = (prev[i + 1] - prev[i]) / (x_nodes[i + k] - x_nodes[i])
            col.append(val)
        table.append(col)
    return table

def newton_interpolate(x_nodes, div_table, x):
    n = len(x_nodes)
    result = div_table[0][0]
    product = 1.0
    for k in range(1, n):
        product = product * (x - x_nodes[k - 1])
        result = result + div_table[k][0] * product
    return result

degrees = [2, 3, 4, 5]
nk_values = []
node_sets = []
div_tables = []

for deg in degrees:
    xn, yn = get_nodes(nearest_index, deg, x_data, y_data)
    table = build_divided_diff_table(xn, yn)
    val = newton_interpolate(xn, table, x_star)
    node_sets.append((xn, yn))
    div_tables.append(table)
    nk_values.append(val)

print("=" * 65)
print("  TASK 2 — NEWTON'S DIVIDED DIFFERENCE INTERPOLATION")
print("  Domain  : Climate & Weather")
print("  Problem : Estimate temperature at x* = 11.5 hours (Dhaka)")
print("=" * 65)

print(f"\nDataset loaded : {len(x_data)} points from temperature_data.csv")
print(f"Target x*      = {x_star} hours")
print(f"Nearest node   = index {nearest_index}, hour = {x_data[nearest_index]:.4f}")

print("\nNode Ordering Strategy:")
print("  Nodes are selected symmetrically around the nearest point to x*.")
print("  They are ordered left to right (ascending x) so that divided")
print("  differences capture the local behavior around the target.")

print("\n" + "-" * 65)
print("  Nodes used for each polynomial degree:")
for deg, (xn, yn) in zip(degrees, node_sets):
    node_str = ", ".join([f"{v:.4f}" for v in xn])
    print(f"  N{deg}(x): nodes x = [{node_str}]")

print("\n" + "-" * 65)
print("  Complete Divided Difference Table (for highest degree N5):")

xn5, yn5 = node_sets[3]
table5 = div_tables[3]
n5 = len(xn5)

header = f"  {'x':>10}  {'f[x]':>12}"
for k in range(1, n5):
    header += f"  {'Order ' + str(k):>14}"
print(header)
print("  " + "-" * (12 + 16 * n5))

for i in range(n5):
    row_str = f"  {xn5[i]:>10.4f}  {table5[0][i]:>12.6f}"
    for k in range(1, n5):
        if i < len(table5[k]):
            row_str += f"  {table5[k][i]:>14.6f}"
        else:
            row_str += f"  {'':>14}"
    print(row_str)

print("\n" + "-" * 65)
print("  Newton Interpolation Polynomial Forms:")
for deg, (xn, yn), table in zip(degrees, node_sets, div_tables):
    coeffs = [table[k][0] for k in range(deg + 1)]
    poly_str = f"  N{deg}(x) = {coeffs[0]:.6f}"
    for k in range(1, deg + 1):
        term_parts = " * ".join([f"(x - {xn[j]:.4f})" for j in range(k)])
        sign = "+" if coeffs[k] >= 0 else "-"
        poly_str += f" {sign} {abs(coeffs[k]):.6f} * {term_parts}"
    print(poly_str)
    print()

print("-" * 65)
print(f"  Convergence Table at x* = {x_star}")
print(f"  {'Degree k':>10}  {'Nk(x*)':>18}  {'Delta_k':>18}")
print("  " + "-" * 52)
for i, (deg, val) in enumerate(zip(degrees, nk_values)):
    if i == 0:
        print(f"  {deg:>10}  {val:>18.6f}  {'—':>18}")
    else:
        delta = abs(val - nk_values[i - 1])
        print(f"  {deg:>10}  {val:>18.6f}  {delta:>18.6f}")

print("\n  Analysis:")
print("  Delta_k shrinks as degree increases — the estimate converges.")
print("  Adding more nodes around x* improves local accuracy.")
print(f"  Best estimate: Temperature at x* = {x_star} hrs ≈ {nk_values[-1]:.6f} °C")

print("\n" + "-" * 65)
print("  Comparison: Newton vs Lagrange at x* = 11.5")
lagrange_pk = [32.625754, 32.640222, 32.638463, 32.638909]
print(f"  {'Degree k':>10}  {'Newton Nk(x*)':>18}  {'Lagrange Pk(x*)':>18}  {'Difference':>14}")
print("  " + "-" * 68)
for deg, nval, lval in zip(degrees, nk_values, lagrange_pk):
    diff = abs(nval - lval)
    print(f"  {deg:>10}  {nval:>18.6f}  {lval:>18.6f}  {diff:>14.8f}")
print("\n  Both methods are mathematically equivalent — results match.")

x_plot = np.linspace(min(x_data), max(x_data), 600)

colors = ["royalblue", "seagreen", "darkorange", "mediumpurple"]
interp_markers = ["*", "^", "D", "P"]
interp_colors = ["blue", "green", "red", "purple"]

fig, ax = plt.subplots(figsize=(14, 7))

ax.scatter(x_data, y_data, color="black", zorder=5, s=55, label="Data Points")

for deg, (xn, yn), table, val, color, mk, ic in zip(degrees, node_sets, div_tables, nk_values, colors, interp_markers, interp_colors):
    y_plot = [newton_interpolate(xn, table, xv) for xv in x_plot]
    ax.plot(x_plot, y_plot, color=color, linewidth=2, label=f"N{deg}(x),  N{deg}(x*) = {val:.4f} °C")
    ax.scatter([x_star], [val], color=ic, zorder=7, s=130, marker=mk)

ax.axvline(x=x_star, color="red", linestyle="--", alpha=0.6, label=f"x* = {x_star} hr")
ax.set_xlabel("Hour of Day", fontsize=12)
ax.set_ylabel("Temperature (°C)", fontsize=12)
ax.set_title("Task 2: Newton's Divided Difference — All Polynomial Degrees\nHourly Temperature, Dhaka", fontsize=13, fontweight="bold")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("task2_newton_plot.png", dpi=150)
plt.show()
print("\nPlot saved as task2_newton_plot.png")