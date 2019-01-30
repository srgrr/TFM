from pycompss.api.task import task
from pycompss.api.parameter import *

# This application was developed with the only purpose of being able
# to reproduce an scenario in which some object is transferred
# from the master to the worker, to see the impact, and temporal files
# that are created due to that in various environments and situations

@task( returns = 1 )
def f(x):
  ''' We should see d1v1, and d2v2 in the worker directory
  (e.g: /tmp/COMPSsWorker/... if running locally)
  '''
  return x

def main():
  import numpy as np
  x = np.random.rand(5)
  from pycompss.api.api import compss_wait_on
  y = compss_wait_on(f(x))

if __name__ == '__main__':
  main()
