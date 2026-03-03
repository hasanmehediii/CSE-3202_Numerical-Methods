import math
import matplotlib.pyplot as plt

def f(x):
    return x**5 - 4*x**3 + 2*x**2 - math.log(x + 2) - 1.5

def bisection(xl, xu, tol):
    if f(xl) * f(xu) >= 0:
        print("Bisection method fails.")
        return 0

    print(f"{'Iter':<8}{'xl':<12}{'xu':<12}{'xr':<12}{'f(xr)':<15}{'ea (%)':<15}")
    print("-" * 75)

    it = 0
    xr_old = xl
    errors = []
    iters = []

    while True:
        it += 1
        xr = (xl + xu) / 2
        
        if it == 1:
            ea_str = "N/A"
            print(f"{it:<8}{xl:<12.6f}{xu:<12.6f}{xr:<12.6f}{f(xr):<15.6f}{ea_str:<15}")
        else:
            ea = abs((xr - xr_old) / xr) * 100
            errors.append(ea)
            iters.append(it)
            print(f"{it:<8}{xl:<12.6f}{xu:<12.6f}{xr:<12.6f}{f(xr):<15.6f}{ea:<15.6f}")

            if f(xr) == 0 or ea < tol:
                break

        if f(xl) * f(xr) < 0:
            xu = xr
        else:
            xl = xr

        xr_old = xr

    plt.figure()
    plt.plot(iters, errors, marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Approximate Relative Error (%)')
    plt.title('Convergence Behavior of Bisection Method')
    plt.grid(True)
    plt.show()

    return xr

xl, xu = 0.5, 2
tol = 0.5 * 10**(2 - 5) 

root = bisection(xl, xu, tol)
print(f"\nApproximate root: {root:.6f}\n")