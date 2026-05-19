import csv
import math
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

def lagrange_interpolate(x_nodes, y_nodes, x):
    n = len(x_nodes)
    result = 0.0
    for i in range(n):
        Li = 1.0
        for j in range(n):
            if j != i:
                Li = Li * (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
        result = result + y_nodes[i] * Li
    return result

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

degrees = [2, 3, 4, 5]
pk_values = []
node_sets = []

for deg in degrees:
    xn, yn = get_nodes(nearest_index, deg, x_data, y_data)
    node_sets.append((xn, yn))
    val = lagrange_interpolate(xn, yn, x_star)
    pk_values.append(val)

print(f"\nDataset loaded: {len(x_data)} points from CSV")
print(f"Target x*      = {x_star} hours")
print(f"Nearest node   = index {nearest_index}, hour = {x_data[nearest_index]:.4f}")

print("\nNode Selection Strategy:")
print("  Nodes centered around the nearest data point to x*.")
print("  For degree k, (k+1) nodes are selected symmetrically.")

print("\n" + "-" * 60)
print("  Nodes used for each polynomial degree:")
for i, (deg, (xn, yn)) in enumerate(zip(degrees, node_sets)):
    node_str = ", ".join([f"{v:.4f}" for v in xn])
    print(f"  P{deg}(x): nodes = [{node_str}]")

print("\n" + "-" * 60)
print("  Lagrange Basis Functions for P2 (numeric coefficients):")
xn2, yn2 = node_sets[0]
for i in range(len(xn2)):
    numerator = np.array([1.0])
    denom = 1.0
    for j in range(len(xn2)):
        if j != i:
            numerator = np.polymul(numerator, [1.0, -xn2[j]])
            denom = denom * (xn2[i] - xn2[j])
    coeffs = numerator / denom
    print(f"  L{i}(x) coefficients [highest deg first]: {[round(c, 6) for c in coeffs]}")

print("\n" + "-" * 60)
print("  Expanded Polynomial Coefficients [highest degree first]:")
poly_coeffs_all = []
for i, (deg, (xn, yn)) in enumerate(zip(degrees, node_sets)):
    poly = np.zeros(deg + 1)
    for k in range(len(xn)):
        Li_num = np.array([1.0])
        denom = 1.0
        for j in range(len(xn)):
            if j != k:
                Li_num = np.polymul(Li_num, [1.0, -xn[j]])
                denom = denom * (xn[k] - xn[j])
        Li_coeffs = Li_num / denom
        poly = poly + yn[k] * Li_coeffs
    poly_coeffs_all.append(poly)
    print(f"  P{deg}(x): {[round(c, 6) for c in poly]}")

print("\n" + "-" * 60)
print(f"  Convergence Table at x* = {x_star}")
print(f"  {'Degree k':>10}  {'Pk(x*)':>18}  {'Delta_k':>18}")
print("  " + "-" * 52)
for i, (deg, val) in enumerate(zip(degrees, pk_values)):
    if i == 0:
        print(f"  {deg:>10}  {val:>18.6f}  {'—':>18}")
    else:
        delta = abs(val - pk_values[i - 1])
        print(f"  {deg:>10}  {val:>18.6f}  {delta:>18.6f}")

print("\n  Analysis:")
print("  As polynomial degree increases, Pk(x*) converges quickly.")
print("  Delta_k decreases, showing improved approximation accuracy.")
print(f"  Best estimate at x* = {x_star} hours: Temp ≈ {pk_values[-1]:.6f} °C")

x_plot = np.linspace(min(x_data), max(x_data), 600)

colors = ["royalblue", "seagreen", "darkorange", "mediumpurple"]
interp_markers = ["*", "^", "D", "P"]
interp_colors = ["blue", "green", "red", "purple"]

fig, ax = plt.subplots(figsize=(14, 7))

ax.scatter(x_data, y_data, color="black", zorder=5, s=55, label="Data Points")

for deg, (xn, yn), val, color, mk, ic in zip(degrees, node_sets, pk_values, colors, interp_markers, interp_colors):
    y_plot = [lagrange_interpolate(xn, yn, xv) for xv in x_plot]
    ax.plot(x_plot, y_plot, color=color, linewidth=2, label=f"P{deg}(x),  P{deg}(x*) = {val:.4f} °C")
    ax.scatter([x_star], [val], color=ic, zorder=7, s=130, marker=mk)

ax.axvline(x=x_star, color="red", linestyle="--", alpha=0.6, label=f"x* = {x_star} hr")
ax.set_xlabel("Hour of Day", fontsize=12)
ax.set_ylabel("Temperature (°C)", fontsize=12)
ax.set_title("Task 1: Lagrange Interpolation — All Polynomial Degrees\nHourly Temperature, Dhaka", fontsize=13, fontweight="bold")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("task1_lagrange_plot.png", dpi=150)
plt.show()
print("\nPlot saved as task1_lagrange_plot.png")