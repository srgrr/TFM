from HyperLogLog import HyperLogLog

def wc_naive(dataset):
	st = set([])
	with open(dataset, "r") as f:
		for line in f:
			for w in line.strip().split():
				st.add(w)
	return len(st)

def hloglog(dataset):
	hobj = HyperLogLog(b = 64, p = 15, plot = True)
	with open(dataset, "r") as f:
		for line in f:
			for w in line.strip().split():
				hobj.add_word(w)
	print(hobj.buckets)
	hobj.plot_result()
	return hobj.get_estimation()

def main():
	dataset = "shakespeare.txt"
	correct = wc_naive(dataset)
	estimation = hloglog(dataset)
	print("Correct: %d\nEstimated: %d\n" % (correct, estimation))

if __name__ == '__main__':
	main()