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
	parser.add_argument("--collections", action = "store_true")
	return parser.parse_args()

@task(filename = FILE_IN, returns = 1)
def count_distinct(filename, bits, buckets):
	h = HyperLogLog(b = bits, p = buckets)
	with open(filename, "r") as f:
		for line in f:
			for w in line.strip().split():
				h.add_word(w)
	return h

@task(hloglogs = COLLECTION_IN, returns = 1)
def reduce_hloglog_collections(hloglogs, bits, buckets):
	h = HyperLogLog(b = bits, p = buckets)
	for hloglog in hloglogs:
		h.add_hyperloglog(hloglog)
	return h.get_estimation()

@task(returns = 1)
def reduce_hloglog(bits, buckets, *args):
	h = HyperLogLog(b = bits, p = buckets)
	for hloglog in args:
		h.add_hyperloglog(hloglog)
	return h.get_estimation()

def elapsed_time(name, start, end):
	print("%s=%.08f" % (name, end - start))

def main(files, bits, buckets, collections):
	import time
	N = len(files)
	hloglogs =\
		list(map(count_distinct, files, [bits] * N, [buckets] * N))
	from pycompss.api.api import compss_barrier, compss_wait_on
	# Easier isolation of reduce time
	compss_barrier()
	start_t = time.time()
	if collections:
		estimation = reduce_hloglog_collections(hloglogs, bits, buckets)
	else:
		estimation = reduce_hloglog(bits, buckets, *hloglogs)
	end_t = time.time()

	print("Estimated cardinality: %d" % compss_wait_on(estimation))

	elapsed_time("reduce", start_t, end_t)

if __name__ == '__main__':
	opts = parse_arguments()
	main(**vars(opts))
