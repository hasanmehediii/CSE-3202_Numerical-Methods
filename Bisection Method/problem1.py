import math
import matplotlib.pyplot as plt

def f(x):
    return 225 + 82*x - 90*x**2 + 44*x**3 - 8*x**4 + 0.7*x**5

def bisection(a, b, tol):
    if f(a) * f(b) >= 0:
        print("Bisection method fails.")
        return 0

    print(f"Initial interval length L0 = {b-a}")
    print(f"{'Iter':<12}{'a':<14}{'b':<12}{'xr=(a+b)/2':<17}{'f(xr)':<20}{'εa (%)':<15}")
    print("-"*100)

    it = 0
    xr_old = a
    errors = []  
    num=0
    while 1:
        it += 1
        xr = (a + b) / 2

        if it == 1:
           continue
        else:
            ea = abs((xr - xr_old) / xr) * 100

        
        errors.append(ea) 
        
        num+=1
        print(f"{num:<5}"
              f"{a:<15.10f}{b:<15.10f}{xr:<15.10f}{f(xr):<20.10f}"
              f"{(f'{ea:.10f}')}"
              )

        if f(xr) == 0 :
            break
        elif f(a) * f(xr) < 0:
            b = xr
        else:
            a = xr

        xr_old = xr
        if ea<tol:
            break
  
    plt.figure()
    plt.plot(range(1, len(errors)+1), errors, marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Absolute Error (%)')
    plt.title('Convergence of Absolute Error in Bisection Method')
    plt.grid(True)
    plt.show()

    return xr

a, b = -1.2, -1.0
tol = 0.05

root = bisection(a, b, tol)
print(f"\nApproximate root: {root:.10f}\n")