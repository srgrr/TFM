import subprocess
import pylab as plt
import numpy as np
import time

def main():
  sizes = list(range(0, 1000001, 10000))
  values, times = [], []

  for size in sizes:
    start_time = time.time()
    outp = subprocess.check_output(['python', 'sequential.py', str(size)])
    print(outp)
    values.append(float(outp))
    end_time = time.time() - start_time
    times.append(end_time)

  plt.figure('Experiments vs Value')
  plt.xlabel('#Experiments')
  plt.ylabel('Value')
  plt.ylim([np.pi - 0.05, np.pi + 0.05])
  # Draw the correct value of pi as a reference
  pi_plot, = plt.plot([sizes[0], sizes[-1]], [np.pi, np.pi], color = 'yellow', label = '$\pi$')
  approx_plot, = plt.plot(sizes, values, color = 'blue', label = 'approximation')
  plt.legend(handles = [pi_plot, approx_plot], loc = 'upper right')
  plt.savefig('pi_size_vs_value.png')

  plt.figure('Experiments vs Time')
  plt.xlabel('#Experiments')
  plt.ylabel('Elapsed Time (s)')
  plt.plot(sizes, times)
  plt.savefig('pi_size_vs_time.png')

if __name__ == '__main__':
  main()
