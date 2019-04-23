from pycompss.api.task import task
from pycompss.api.api import compss_barrier

NUM_ITERATIONS = 100

@task(returns = 1)
def f(x):
  return x

def main():
  for i in range(NUM_ITERATIONS):
    l = []
    for j in range(NUM_ITERATIONS):
      l.append(f(object()))
    compss_barrier()

if __name__ == "__main__":
  main()
