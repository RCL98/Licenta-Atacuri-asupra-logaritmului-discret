from aritmetica_modulara import sqrt
from sympy.ntheory import factorint
from math import ceil
from functools import reduce
import operator
import generate_primes as gnp
import time
from random import randint, seed

def shanks_ordin_necunoscut(g, h, p):
  rad_p = ceil(sqrt(p - 1))
  n = 100
  lista_n = []
  while n < rad_p:
    lista_n.append(n)
    n *= 10
  lista_n.append(rad_p)
  last_n = 1
  e = 1
  lista = {e: 0}
  for n in lista_n:
    for j in range(last_n, n + 1):
      e = (e * g) % p
      if e == h:
        return j
      lista[e] = j

    u = pow(g, p - n - 1, p)
    l = h
    for i in range(0, n + 1):
      try:
        j = lista[l]
        return i * n + j
      except KeyError:
        l = (l * u) % p
    last_n = n + 1
  return None

def shanks_classic(g, h, p, ordin):
  n = ceil(sqrt(ordin))
  small_steps, giant_steps = 1, 0
  e = 1
  lista = {e: 0}
  for j in range(1, n):
    e = (e * g) % p
    if e == h:
      return j, small_steps, giant_steps
    else:
      lista[e] = j
      small_steps += 1
  u = pow(g, p - n - 1, p)
  s = pow(g, n, p)
  ep = em = h
  u = pow(g, p - n - 1, p)
  e = h
  giant_steps = 1
  for i in range(0, n):
    try:
      j = lista[e]
      return i * n  + j, small_steps, giant_steps
    except KeyError:
      e = (e * u) % p
      giant_steps += 1
  return None

def shanks_ordin_cunoscut_with_memory(g, h_values, p, ordin):
  n = ceil(sqrt(ordin))
  small_steps = 1
  e = 1
  lista = {e: 0}
  for j in range(1, n):
    e = (e * g) % p
    lista[e] = j
    small_steps += 1

  u = pow(g, p - n - 1, p)
  exponents, giant_steps_list = [], []
  for h in h_values:
    e = h
    giant_steps = 1
    for i in range(0, n):
      try:
        j = lista[e]
        exponents.append(i * n + j)
        giant_steps_list.append(giant_steps)
        break
      except KeyError:
        e = (e * u) % p
        giant_steps += 1
  return exponents, small_steps, giant_steps_list

def shanks_general(g, h, p, ordin, r):
  n = ceil(ordin ** (1/r))
  m = ceil(ordin/n)
  small_steps, giant_steps = 1, 0
  e = 1
  lista = {e: 0}
  for j in range(1, m):
    e = (e * g) % p
    if e == h:
      return j, small_steps, giant_steps
    else:
      lista[e] = j
      small_steps += 1

  u = pow(g, p - m - 1, p)
  e = h
  giant_steps = 1
  for i in range(0, n):
    try:
      j = lista[e]
      return i * m + j, small_steps, giant_steps
    except KeyError:
      e = (e * u) % p
      giant_steps += 1
  return None

def shanks_general_with_memory(g, h_values, p, ordin, r):
  n = ceil(ordin ** (1/r))
  m = ceil(ordin/n)
  small_steps = 1
  e = 1
  lista = {e: 0}
  for j in range(1, m):
    e = (e * g) % p
    lista[e] = j
    small_steps += 1
  u = pow(g, p - m - 1, p)
  exponents, giant_steps_list = [], []
  for h in h_values:
    e = h
    giant_steps = 1
    for i in range(0, n):
      try:
        j = lista[e]
        exponents.append(i * m + j)
        giant_steps_list.append(giant_steps)
        break
      except KeyError:
        e = (e * u) % p
        giant_steps += 1
  return exponents, small_steps, giant_steps_list

def optim_factors(ordin):
  factori = [pow(x, e) for x, e in factorint(ordin).items()]
  factori.sort()
  if len(factori) == 1:
    return Shanks_ordin_cunoscut(g, h, p, ordin)
  if len(factori) == 2:
    l = ceil(sqrt(factori[1]))
    m = ceil(sqrt(factori[0]))
  else:
    fact_1 = reduce(operator.mul, factori[:-1])
    if fact_1 > factori[-1]:
      l = ceil(sqrt(fact_1))
      m = ceil(sqrt(factori[-1]))
    else:
      l = ceil(sqrt(factori[-1]))
      m = ceil(sqrt(fact_1))
  return l, m

def shanks_factor(g, h, p, l, m):
  small_steps, giant_steps = 1, 0
  e = 1
  lista = {e: 0}
  for j in range(1, l ** 2):
    e = (e * g) % p
    if e == h:
      return j, small_steps, giant_steps
    else:
      lista[e] = j
      small_steps += 1

  u = pow(g, p - l ** 2 - 1, p)
  e = h
  giant_steps = 1
  for i in range(0, m ** 2):
    try:
      j = lista[e]
      return i * (l ** 2) + j, small_steps, giant_steps
    except KeyError:
      e = (e * u) % p
      giant_steps += 1
  return None

def shanks_factor_with_memory(g, h_values, p, l, m):
  small_steps = 1
  e = 1
  lista = {e: 0}
  for j in range(1, l ** 2):
    e = (e * g) % p
    lista[e] = j
    small_steps += 1
  u = pow(g, p - l ** 2 - 1, p)
  exponents, giant_steps_list = [], []
  for h in h_values:
    e = h
    giant_steps = 1
    for i in range(0, m ** 2):
      try:
        j = lista[e]
        exponents.append(i * (l ** 2) + j)
        giant_steps_list.append(giant_steps)
        break
      except KeyError:
        e = (e * u) % p
        giant_steps += 1
  return exponents, small_steps, giant_steps_list

def shanks_middle_to_edges(g, h, p, ordin):
  n = ceil(sqrt(ordin))
  K = ordin // 2
  small_steps, giant_steps = 1, 0
  e = pow(g, K, p)
  lista = {e: 0}
  for j in range(1, n):
    e = (e * g) % p
    if e == h:
      return j, small_steps, giant_steps
    else:
      lista[e] = j
      small_steps += 1
  u = pow(g, p - n - 1, p)
  s = pow(g, n, p)
  ep = em = h
  giant_steps = 2
  for i in range(0, n):
    try:
      j = lista[em]
      return j + K - i * n, small_steps, giant_steps
    except KeyError:
      try:
        j = lista[ep]
        return K + j + i * n, small_steps, giant_steps
      except KeyError:
        ep = (ep * u) % p
        em = (em * s) % p
        giant_steps += 2
  return None

def Shanks(g, h, p, ordin = None):
  if ordin:
    return Shanks_classic(g, h, p, ordin)
  return Shanks_ordin_necunoscut(g, h, p)

# def test_shanks(numOfTests: int, numOfBits: int):
#   primes, generators, exponents, h_values = gnp.logarithm_test_numbers(numOfTests, numOfBits)
#   for (p, g, e, h) in zip(primes, generators, exponents, h_values):
#     x = Shanks_general(g, h, p, p - 1, e)
#     if e != x:
#       print(f"e:{e}  x:{x}")
#     else:
#       print("Test passed!")

def avg(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)

def test_shanks(numOfTests: int, numOfBits: int, type: str, r = 2):
  times = []
  for _ in range(numOfTests):
    p, g, e, h = gnp.logarithm_test_numbers(1, numOfBits)
    if type == 'c':
      t_start = time.time()
      x, small_steps, giant_steps = Shanks_ordin_cunoscut(g[0], h[0], p[0], p[0] - 1)
    elif type == 'g':
      t_start = time.time()
      x, small_steps, giant_steps = Shanks_general(g[0], h[0], p[0], p[0] - 1, r)
    else:
      l, m = optim_factors(p[0] - 1)
      t_start = time.time()
      x, small_steps, giant_steps = Shanks_factor(g[0], h[0], p[0], l, m)
    t_stop = time.time()
    if e[0] != x:
      print(f"e:{e[0]}  x:{x}")
    else:
      t = (t_stop - t_start)/1000
      times.append(t)
      print(f"Test passed! p:{p[0]}, time:{t:.7f} ms, small_steps:{small_steps} giant_steps:{giant_steps}")
  print(f"Avg time:{avg(times)}")

def test_shanks_same_p(numOfTests: int, numOfBits: int, r = 2):
  times = []
  p, g, exponents, h_values = gnp.logarithm_test_numbers(1, numOfBits)
  l, m = optim_factors(p[0] - 1)
  for _ in range(numOfTests):
    exponents.append(randint(2, p[0] - 1))
    h_values.append(pow(p[0], g[0], exponents[-1]))

  t_start_c = time.time()
  x_c, small_steps_c, giant_steps_c = Shanks_ordin_cunoscut_with_memory(g[0], h_values, p[0], p[0] - 1)
  t_stop_c = time.time()
  for (e, x) in zip(exponents, x_c):
    if e!= x:
      print(f"e:{e}  x_c:{x}")

  t_start_g = time.time()
  x_g, small_steps_g, giant_steps_g = Shanks_general_with_memory(g[0], h_values, p[0], p[0] - 1, r)
  t_stop_g = time.time()
  for (e, x) in zip(exponents, x_g):
    if e != x:
      print(f"e:{e}  x_g:{x}")

  t_start_f = time.time()
  x_f, small_steps_f, giant_steps_f = Shanks_factor_with_memory(g[0], h_values, p[0], l, m)
  t_stop_f = time.time()
  for (e, x) in zip(exponents, x_f):
    if e != x:
      print(f"e:{e}  x_f:{x}")

    print(f"t_c: {(t_stop_c - t_start_c)/1000:.7f}, t_g: {(t_stop_g - t_start_g)/1000}:.7f, t_f:{(t_stop - t_start)/1000:.7f}")
    print(f"sm_c: {small_steps_c}, sm_g: {small_steps_g}, sm_f:{small_steps_f}")
    for (e, g_c, g_g, g_f) in zip(exponents, giant_steps_c, giant_steps_g, giant_steps_f):
      print(f"e:{e}, tgiant_steps_c:{g_c}, giant_steps_g:{g_g} giant_steps_f:{g_f}")

def test_shanks_middle(numOfTests: int, numOfBits: int, randSeed):
  seed(randSeed)
  giant_steps_c_list, small_steps_c_list = [], []
  giant_steps_m_list, small_steps_m_list = [], []
  for iter in range(numOfTests):
    p, g, exp, h = gnp.logarithm_test_numbers(numOfBits, True)
    print("iter:", iter)
    x_c, small_steps_c, giant_steps_c = shanks_classic(g, h, p, p - 1)
    if x_c != exp:
      print(f"Classic x:{x_c}, exp:{exp}")
    else:
      giant_steps_c_list.append(giant_steps_c)
      small_steps_c_list.append(small_steps_c)
      print(f"C_passed x:{x_c}, exp:{exp}, sm:{small_steps_c}, gs:{giant_steps_c}")
    x_m, small_steps_m, giant_steps_m = shanks_middle_to_edges(g, h, p, p - 1)
    if x_m != exp:
      print(f"Middle x:{x_m}, exp:{exp}\n")
    else:
      giant_steps_m_list.append(giant_steps_m)
      small_steps_m_list.append(small_steps_m)
      print(f"M_passed x:{x_c}, exp:{exp}, sm:{small_steps_m}, gs:{giant_steps_m}\n")
  print(f"Classic: smavg:{avg(small_steps_c_list)}, gsavg:{avg(giant_steps_c_list)}")
  print(f"Middle: smavg:{avg(small_steps_m_list)}, gsavg:{avg(giant_steps_m_list)}")
