import math
import pandas as pd
import matplotlib.pyplot as plt

def f(x):
    return 225 + 82*x - 90*x**2 + 44*x**3 - 8*x**4 + 0.7*x**5

xl = -1.2
xu = -1.0

es_stop = 0.05

data = []
ea_list = []
iter_list = []

xr_old = None
iteration = 0

true_root = -1.1276204097

while True:
    iteration += 1
    
    xr = (xl + xu) / 2
    fxr = f(xr)
    
    if xr_old is None:
        ea = None
    else:
        ea = abs((xr - xr_old) / xr) * 100
    
    et = abs((true_root - xr) / true_root) * 100
    
    data.append([
        iteration,
        round(xl, 10),
        round(xu, 10),
        round(xr, 10),
        round(fxr, 10),
        None if ea is None else round(ea, 10),
        round(et, 10)
    ])
    
    if ea is not None:
        ea_list.append(ea)
        iter_list.append(iteration)
    
    if ea is not None and ea < es_stop:
        break
    
    if f(xl) * fxr < 0:
        xu = xr
    else:
        xl = xr
    
    xr_old = xr

columns = ["Iter", "xl", "xu", "xr", "f(xr)", "Approx Error (%)", "True Error (%)"]
df = pd.DataFrame(data, columns=columns)

print(df)

plt.figure()
plt.plot(iter_list, ea_list, marker='o')
plt.xlabel("Iteration Number")
plt.ylabel("Absolute Approx Error (%)")
plt.title("Error Convergence in Bisection Method")
plt.grid(True)
plt.show()