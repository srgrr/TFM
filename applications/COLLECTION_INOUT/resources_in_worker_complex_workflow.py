from pycompss.api.task import task
from pycompss.api.parameter import *

# A small, simple program to show the COLLECTION_INOUT feature
# Its workflow can be summarized as follows:
# 1) Ten random vectors with 5 elements are created in COMPSs tasks
# 2) A task receives these ten random vectors packed in a COLLECTION_IN
#    parameter
# 3) A task receives the fifht element of this collection as an INOUT and increases all
#    its entries by one
# 4) A task receives this collection as a COLLECTION_INOUT, and increases all entries
#    of all vectors by exactly one
# 5) The fifth of these vectors is chosen
# 6) This same vector is created in the master program, and a check is performed


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

@task(c = COLLECTION_INOUT)
def increase_elements(c):
  for elem in c:
    elem += 1.0

@task(e = INOUT)
def increase_element(e):
  e += 1.0

@task(c = COLLECTION_IN, returns = 1)
def select_element(c, i):
  """Given a collection and an integer "i", return the ith element
  of this collection
  """
  print("Received collection value is %s" % str(c))
  return c[i]

def main():
  from pycompss.api.api import compss_wait_on
  # Generate ten random vectors with pre-determined seed
  ten_random_vectors = [generate_object(i) for i in range(10)]
  increase_elements(ten_random_vectors)
  increase_element(ten_random_vectors[4])
  # Pick the fifth vector from a COLLECTION_IN parameter
  fifth_vector = compss_wait_on(select_element(ten_random_vectors, 4))
  print("My chosen vector is \t %s" % str( fifth_vector ))

  # Recreate this vector locally 
  import numpy as np
  np.random.seed(4)
  master_vector = np.random.rand(5) + 2.0

  print("The correct vector is \t %s" % str( master_vector ))

  # Check that they match
  assert np.allclose(fifth_vector, master_vector), "Vectors do not match"

  # They did match, we can now end the program
  print("Congratulations! Both vectors match!")

if __name__ == "__main__":
  main()
