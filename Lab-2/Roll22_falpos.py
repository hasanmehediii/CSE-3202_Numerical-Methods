import math
import matplotlib.pyplot as plt

def f(x):
    return 1.2 - ((x**2) / ((1 - x)**2)) * math.exp(-8.0 * x) + math.log(1 + x)

def false_position(xl, xu, tol):
    if f(xl) * f(xu) >= 0:
        print("(xl) and f(xu) have the same sign.")
        return None

    print(f"{'Iter':<5}{'xl':<15}{'xu':<15}{'xr':<15}{'f(xr)':<20}{'ea (%)':<15}")
    print("-" * 85)

    it = 0
    xr_old = xl
    errors = []
    iter_nums = []

    while True:
        it += 1
        
        xr = (xl * f(xu) - xu * f(xl)) / (f(xu) - f(xl))
        fxr = f(xr)

        if it == 1:
            print(f"{it:<5}{xl:<15.10f}{xu:<15.10f}{xr:<15.10f}{fxr:<20.10f}{'':<15}")
        else:
            ea = abs((xr - xr_old) / xr) * 100
            errors.append(ea)
            iter_nums.append(it)
            print(f"{it:<5}{xl:<15.10f}{xu:<15.10f}{xr:<15.10f}{fxr:<20.10f}{ea:.10f}")

        if fxr == 0:
            break

        if f(xl) * fxr < 0:
            xu = xr
        else:
            xl = xr

        xr_old = xr

        if it > 1 and ea < tol:
            break

    plt.figure()
    plt.plot(iter_nums, errors, marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Approximate Error (%)')
    plt.title('Convergence of Approximate Error in False Position Method')
    plt.grid(True)
    plt.show()

    return xr

def main():
    tol = 0.00001
    xl = 0.0
    xu = 0.999
    root = false_position(xl, xu, tol)
    if root is not None:
        print(f"\nApproximate root: {root:.10f}\n")

if __name__ == "__main__":
    main()