import math
import matplotlib.pyplot as plt

def f(x):
    return 1.2 - ((x**2) / ((1 - x)**2)) * math.exp(-8.0 * x) + math.log(1 + x)

def secant(x0, x1, tol):
    print("{:<5}{:<15}{:<15}{:<15}{:<20}{:<15}".format("Iter", "x0", "x1", "xr(new)", "f(xr)", "ea (%)"))
    print("-" * 90)

    it = 0
    errors = []

    while True:
        it += 1
        f0, f1 = f(x0), f(x1)

        if f1 - f0 == 0:
            print("Division by zero. Not applicable")
            return None

        step = (f1 * (x1 - x0)) / (f1 - f0)

        alpha = 1.0
        for _ in range(50):
            xr = x1 - alpha * step
            if (1 + xr) > 0 and xr != 1:
                break
            alpha /= 2
        else:
            print("Could not find a valid step within the domain.")
            return None

        ea = abs((xr - x1) / xr) * 100
        errors.append(ea)

        print("{:<5}{:<15.6f}{:<15.6f}{:<15.6f}{:<20.6f}{:.6f}".format(it, x0, x1, xr, f(xr), ea))

        if ea < tol:
            break

        x0 = x1
        x1 = xr

        if it > 1000:
            print("Max iterations reached.")
            break

    plt.figure()
    plt.plot(range(1, len(errors) + 1), errors, marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Approximate Error (%)')
    plt.title('Convergence of Approximate Error - Secant Method')
    plt.yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return xr

def main():
    x0 = 0.3
    x1 = 0.7
    tol = 0.00001

    root = secant(x0, x1, tol)
    if root is not None:
        print("\nApproximate root: {:.6f}\n".format(root))

if __name__ == "__main__":
    main()