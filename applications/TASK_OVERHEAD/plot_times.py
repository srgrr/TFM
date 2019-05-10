import pylab as plt
nums = [float(x.strip()) for x in open("times2.txt").readlines()]

plt.figure()

plt.xlabel("Call ID")
plt.ylabel("Exec. time (s)")

plt.scatter(range(len(nums)), nums, s = 1)

plt.savefig("../../tex/figures/task_overhead_exec_times_fix.png")
