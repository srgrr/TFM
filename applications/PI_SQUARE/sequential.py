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
  proportion = sum([test_random_point() / float(N) for _ in range(N)])
  # Print our pi approximation with up to 16 decimal places
  print("%.16f" % (4.0 * proportion))

if __name__ == "__main__":
  main()
