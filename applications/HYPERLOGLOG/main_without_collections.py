from pycompss.api.task import task
from pycompss.api.parameter import *
from HyperLogLog import HyperLogLog

def parse_arguments():
	import argparse
	parser = \
		argparse.ArgumentParser(
			description = "Count the number of distinct words of a set of text files"
		)
	parser.add_argument("files", metavar="N", type = str, nargs = "+",
                help="(Absolute or relative) paths to files")
	parser.add_argument("--bits", default = 64, type = int, help = "Bits per hash")
	parser.add_argument("--buckets", default = 11, type = int, help = "Bits for bucket indexing")
	return parser.parse_args()

@task(filename = FILE_IN, returns = 1)
def count_distinct(filename, bits, buckets):
	h = HyperLogLog(b = bits, p = buckets)
	with open(filename, "r") as f:
		for line in f:
			for w in line.strip().split():
				h.add_word(w)
	return h

@task(returns = 1)
def reduce_hloglog(bits, buckets, *args):
	h = HyperLogLog(b = bits, p = buckets)
	for hloglog in args:
		h.add_hyperloglog(hloglog)
	return h.get_estimation()

def main(files, bits, buckets):
	N = len(files)
	hloglogs =\
		list(map(count_distinct, files, [bits] * N, [buckets] * N))
	from pycompss.api.api import compss_wait_on
	print("Estimated cardinality: %d" 
		% compss_wait_on(reduce_hloglog(bits, buckets, *hloglogs)))

if __name__ == '__main__':
	opts = parse_arguments()
	main(**vars(opts))