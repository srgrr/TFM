@task(returns = 1)
def f(x):
  return x

def master_routine(n):
  import numpy as np
  x = np.random.rand(n)
  y = f(x)
  from pycompss.api.api import compss_wait_on
  return compss_wait_on(y)

def main():
  y1 = master_routine(n)
  y2 = master_routine(n)
