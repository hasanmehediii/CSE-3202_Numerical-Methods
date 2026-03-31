import math
import matplotlib.pyplot as plt

def f(x):
    return 1.2 - ((x**2) / ((1 - x)**2)) * math.exp(-8.0 * x) + math.log(1 + x)

def df(x):
    term1 = (2 * x * (1 - x)**2 + 2 * x**2 * (1 - x)) / ((1 - x)**4)
    term2 = (8 * x**2) / ((1 - x)**2)
    return -(term1 * math.exp(-8.0 * x) - term2 * math.exp(-8.0 * x)) + (1 / (1 + x))

def newton_raphson(x0, tol):
    print("{:<5}{:<15}{:<15}{:<15}{:<15}{:<15}".format("Iter", "xk", "f(xk)", "f'(xk)", "x(new)", "ea (%)"))
    print("-" * 80)
    it = 0
    xr_old = x0
    errors = []

    while True:
        it += 1
        fx = f(xr_old)
        dfx = df(xr_old)

        if dfx == 0:
            print("Derivative is zero. Method fails.")
            return None

        alpha = 1.0
        for _ in range(50):
            xr = xr_old - alpha * fx / dfx
            if (1 + xr) > 0 and xr != 1:
                break
            alpha /= 2
        else:
            print("Could not find a valid step within the domain.")
            return None

        if xr != 0:
            ea = abs((xr - xr_old) / xr) * 100
        else:
            ea = float('inf')

        errors.append(ea)
        print("{:<5}{:<15.6f}{:<15.6f}{:<15.6f}{:<15.6f}{:.6f}".format(it, xr_old, fx, dfx, xr, ea))

        if ea < tol:
            break

        xr_old = xr

        if it > 1000:
            print("Max iterations reached.")
            break

    plt.figure()
    plt.plot(range(1, len(errors) + 1), errors, marker='o', color='r')
    plt.xlabel('Iteration')
    plt.ylabel('Approximate Error εa (%)')
    plt.title('Convergence of Approximate Error - Newton-Raphson Method')
    plt.yscale('log')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return xr

def main():
    tol = 0.00001
    x0 = 0.5
    root = newton_raphson(x0, tol)
    if root is not None:
        print("\nApproximate root: {:.6f}\n".format(root))

if __name__ == "__main__":
    main()