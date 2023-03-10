import numpy as np
from numpy.linalg import norm
from sympy import diff, Symbol, lambdify

np.seterr(all='raise')


def dreptunghiuri(f, a, b, n):
    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    aprox = 0
    for i in range(n):
        aprox += f((x[i] + x[i + 1]) / 2)

    return aprox * h


def err_dreptunghi(f, a, b, n):
    f_deriv = diff(f, Symbol('x'))
    f_deriv = lambdify(Symbol('x'), f_deriv)
    f = lambdify(Symbol('x'), f)
    valori = f_deriv(np.arange(a, b))
    maxx = norm(valori, np.inf)
    putere = (b - a) ** 2

    aprox = 0
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    for i in range(n):
        aprox += f((x[i] + x[i + 1]) / 2)

    return aprox * h, (putere / (4 * n ** 2)) * maxx


def trapez_clasic(f, a, b, n):
    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    aprox = 0
    for i in range(n):
        aprox += (f(x[i]) + f(x[i + 1])) / 2
    return aprox * h


def trapez_clasic_err(f, a, b, err):
    n = 1
    f_deriv = diff(f, Symbol('x'), 2)
    f_deriv = lambdify(Symbol('x'), f_deriv)
    f = lambdify(Symbol('x'), f)
    valori = f_deriv(np.arange(a, b))
    maxx = norm(valori, np.inf)
    putere = (b - a) ** 3

    aprox = 0
    h = 0
    i = 0
    while (putere / (12 * n ** 2)) * maxx > err:
        i += 1
        n += 1
        aprox = 0
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        for i in range(n):
            aprox += (f(x[i]) + f(x[i + 1])) / 2

    return aprox * h, i


def trapez_compozit(f, a, b, n):
    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    aprox = (f(a) + f(b)) / 2
    for i in range(1, n):
        aprox += f(x[i])
    return aprox * h


def trapez_compozit_err(f, a, b, err):
    n = 1
    f_deriv = diff(f, Symbol('x'), 2)
    f_deriv = lambdify(Symbol('x'), f_deriv)
    f = lambdify(Symbol('x'), f)
    valori = f_deriv(np.arange(a, b))
    maxx = norm(valori, np.inf)
    putere = (b - a) ** 3

    aprox = 0
    h = 0
    i = 0
    while (putere / (12 * n ** 2)) * maxx > err:
        i += 1
        n += 1
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        aprox = (f(a) + f(b)) / 2
        for i in range(1, n):
            aprox += f(x[i])

    return aprox * h, i


def simpson_clasic(f, a, b, n):
    h = (b - a) / n

    x = np.linspace(a, b, n + 1)

    aprox = 0
    for i in range(n):
        aprox += (f(x[i]) + 4 * f((x[i] + x[i + 1]) / 2) + f(x[i + 1])) / 6
    return aprox * h


def simpson_clasic_err(f, a, b, err):
    n = 1
    f_deriv = diff(f, Symbol('x'), 4)
    f_deriv = lambdify(Symbol('x'), f_deriv)
    f = lambdify(Symbol('x'), f)
    valori = f_deriv(np.arange(a, b))
    maxx = norm(valori, np.inf)
    putere = (b - a) ** 5

    h = (b - a) / n
    i = 0
    x = np.linspace(a, b, n + 1)
    aprox = (f(x[i]) + 4 * f((x[i] + x[i + 1]) / 2) + f(x[i + 1])) / 6
    while (putere / (180 * n ** 4)) * maxx > err:
        i += 1
        n += 1
        aprox = 0
        x = np.linspace(a, b, n + 1)
        for i in range(n):
            aprox += (f(x[i]) + 4 * f((x[i] + x[i + 1]) / 2) + f(x[i + 1])) / 6

    h = (b - a) / n
    print((putere / (180 * n ** 4)) * maxx)
    return aprox * h, i


def simpson_compozit(f, a, b, n):
    h = (b - a) / n

    s = f(a) + f(b)
    s_par = 0
    s_impar = 0
    for i in range(1, n):
        if i % 2 == 0:
            s_par += f(a + i * h)
        else:
            s_impar += f(a + i * h)

    aprox = (s + 2 * s_par + 4 * s_impar) * h / 3
    return aprox


def simpson_compozit_err(f, a, b, err):
    n = 1
    f_deriv = diff(f, Symbol('x'))
    f_deriv = lambdify(Symbol('x'), f_deriv)
    f = lambdify(Symbol('x'), f)
    valori = f_deriv(np.arange(a, b))
    maxx = norm(valori, np.inf)
    putere = (b - a) ** 5

    i = 0
    s = f(a) + f(b)
    h = (b - a) / n
    s_para = 0
    s_impara = 0
    while (putere / (2880 * n ** 4)) * maxx > err:
        n += 1
        i += 1
        s = f(a) + f(b)
        h = (b - a) / n
        s_para = 0
        s_impara = 0
        for i in range(1, n):
            if i % 2 == 0:
                s_para += f(a + i * h)
            else:
                s_impara += f(a + i * h)

    aprox = (s + 2 * s_para + 4 * s_impara) * h / 3
    print((putere / (180 * n ** 4)) * maxx - err)
    return aprox, i
