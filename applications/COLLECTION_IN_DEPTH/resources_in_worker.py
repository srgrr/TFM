from pycompss.api.task import task
from pycompss.api.parameter import *

# A small, simple program to show the COLLECTION_IN_DEPTH feature
# Its workflow can be summarized as follows:
# 1) A 2x2x2x2 matrix of np.array objects is created, each np.array is the return
#    of a PyCOMPSs task
# 2) We return M[0][1][0][1] with a PyCOMPSs task
# 3) This vector is also manually recreated, and compared against the actual result


# This program should be enough to test that this feature
# works, as the main aspects are tested with it.

@task(returns = 1)
def generate_object(seed):
  """Given an integer, create a random numpy vector of 5 elements
  using this integer as the random seed. 
  """
  import numpy as np
  np.random.seed(seed)
  return np.random.rand(5)

@task(c = {Type: COLLECTION_IN, Depth: 4}, returns = 1)
def select_element(c, i, j, k, l):
  """Given a collection and a set of indices, return the element
  of this collection which corresponds to these indices
  """
  return c[i][j][k][l]

def main():
  from pycompss.api.api import compss_wait_on
  # Generate a 2x2x2x2 random matrix with pre-determined seed
  two_two_two_two_matrix = \
    [
      [
        [
          [                # Note that all blocks will have a unique seed between 0 and 15
            generate_object(8 * i + 4 * j + 2 * k + l) for l in range(2)
          ] for k in range(2)
        ] for j in range(2)
      ] for i in range(2)
    ]
  # Pick the fifth vector from a COLLECTION_IN parameter
  zero_one_zero_one = compss_wait_on(select_element(two_two_two_two_matrix, 0, 1, 0, 1))
  print("My chosen vector is \t %s" % str( zero_one_zero_one ))

  # Recreate this vector locally 
  import numpy as np
  np.random.seed(4 + 1)
  master_vector = np.random.rand(5)

  print("The correct vector is \t %s" % str( master_vector ))

  # Check that they match
  assert np.allclose(zero_one_zero_one, master_vector), "Vectors do not match"
  # They did match, we can now end the program
  print("Congratulations! Both vectors match!")

if __name__ == "__main__":
  main()
