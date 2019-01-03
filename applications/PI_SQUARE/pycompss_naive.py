from pycompss.api.task import task
from pycompss.api.parameter import *

@task(returns = 1)
def test_random_point():
  import numpy as np
  # p is a 1x2 vector with two numbers in [-1, 1]
  p = 2.0 * np.random.rand(2) - 1.0
  # count this point iff it is within one unit or less
  # within the origin
  if np.linalg.norm(p) <= 1.0:
    return 1.0
  return 0.0

def main():
  import sys
  N = int(sys.argv[1])
  # Note that test_random_point is now a PyCOMPSs task
  # This means that calling this task does not imply immediate results
  # So, a future object will be returned instead
  future_proportions = [test_random_point() for _ in range(N)]
  from pycompss.api.api import compss_barrier, compss_wait_on
  # We will wait for all tasks to end before adding these values to our
  # final accumulator
  compss_barrier()
  proportion = sum([compss_wait_on(x) / float(N) for x in future_proportions])
  # Print our pi approximation with up to 16 decimal places
  print("%.16f" % (4.0 * proportion))

if __name__ == "__main__":
  main()
