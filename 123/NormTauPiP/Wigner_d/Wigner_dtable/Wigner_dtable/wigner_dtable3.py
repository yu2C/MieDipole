from sympy import Integer, symbols, pi, pprint
from sympy.physics.wigner import wigner_d_small
half = 1/Integer(2)
beta = symbols("beta", real=True)
pprint(wigner_d_small(half, beta), use_unicode=True)

pprint(wigner_d_small(half, beta).subs({beta:pi/2}), use_unicode=True)