from pycompss.api.task import task
from pycompss.api.parameter import *

@task(returns = 1)
def test_random_points(M):
  import numpy as np
  # p is a Mx2 matrix with two numbers in [-1, 1]
  p = 2.0 * np.random.rand(M, 2) - 1.0
  # count these points iff they are within one unit or less
  # within the origin
  return np.sum(np.linalg.norm(p, axis = 1) <= 1.0) / float(M)

def main():
  import sys
  N = int(sys.argv[1])
  M = int(sys.argv[2])
  # Note that test_random_point is now a PyCOMPSs task
  # This means that calling this task does not imply immediate results
  # So, a future object will be returned instead
  future_proportions = [test_random_points(M) for _ in range(N)]
  from pycompss.api.api import compss_barrier, compss_wait_on
  # We will wait for all tasks to end before adding these values to our
  # final accumulator
  compss_barrier()
  proportion = sum([compss_wait_on(x) / float(N) for x in future_proportions])
  # Print our pi approximation with up to 16 decimal places
  print("%.16f" % (4.0 * proportion))

if __name__ == "__main__":
  main()
