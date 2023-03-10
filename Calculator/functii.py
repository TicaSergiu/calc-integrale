import math
import timeit

from scipy.integrate import quadrature
import sympy as sp
from metode import *

fs = sp.lambdify(sp.Symbol('x'), 'sin(x)')
f = 'sin(x)'

start = timeit.default_timer()
aprox, err = simpson_compozit_err(f, 0, np.pi, 0.00000001)
print(timeit.default_timer() - start)

print("Aprox: " + str(aprox))
print("Err: " + str(err))
print("Exact: " + str(quadrature(fs, 0, np.pi)[0]))
print(int(2.2))
