import pylab as plt

def parse_elapsed(outp):
	print(outp)
	return float([x.strip().split("=")[1] for x in outp.split("\n") if "reduce" in x][0])

def main():
	elapsed_normal = []
	elapsed_collections = []
	num_files = list(range(1, 101, 10))
	scattered_normal_x, scattered_normal_y = [], []
	scattered_collections_x, scattered_collections_y = [], []
	for i in num_files:
		normal, collections = [], []
		for j in range(5):
			files = ["a.txt"] * i
			command = ["runcompss", "main.py"] + files
			print("RUNNING %s" % command)
			import subprocess
			outp = subprocess.check_output(command)
			normal.append(parse_elapsed(outp))
			scattered_normal_x.append(i)
			scattered_normal_y.append(normal[-1])
			command.append("--collections")
			print("RUNNING %s" % command)
			outp = subprocess.check_output(command)
			collections.append(parse_elapsed(outp))
			scattered_collections_x.append(i)
			scattered_collections_y.append(collections[-1])
			import os
			os.system("matacompss")
			import time
			time.sleep(1)
		import numpy as np
		elapsed_normal.append(np.mean(normal))
		elapsed_collections.append(np.mean(collections))

	plt.figure()
	plt.xlabel("#Parameters in reduction")
	plt.ylabel("Elapsed time (s)")
	pl1, = plt.plot(num_files, elapsed_normal, color = "blue", label = "*args")
	plt.scatter(num_files, elapsed_normal, color = "blue")
	pl2, = plt.plot(num_files, elapsed_collections, color = "red", label = "COLLECTION_IN")
	plt.scatter(num_files, elapsed_collections, color = "red")
	plt.legend(handles = [pl1, pl2])
	plt.savefig("collection_vs_normal.png")

if __name__ == '__main__':
	main()
