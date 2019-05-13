import numpy as np


class HyperLogLog(object):
	"""An implementation of an HyperLogLog memory object, part of the
	wordcount-collections example source code
	"""
	def __init__(self, b, p, plot = False):
		"""Constructor method.
		Parameters:
		b, integer: total number of bits (b - p bits per bucket)
		p, integer: exponent of the number of buckets (2^p)
		"""
		self.b = b
		self.p = p
		self.buckets = np.zeros(2 ** p, dtype = np.uint8)
		self.plot = plot

		if self.plot:
			self.histogram = []

	def hash(self, w):
		"""Get the hash of a token.
		Maybe sha256 is an overkill for this situation, but we prefer to err
		in the cautious side
		"""
		import hashlib
		return int(hashlib.sha256(w.encode("utf-8")).hexdigest(), 16)

	def leading_zeroes(self, n, num_bits):
		"""Get the number of leading zeroes in binary representation
		"""
		for i in range(num_bits - 1, -1, -1):
			if n & (1 << i):
				return num_bits - i - 1
		return num_bits

	def add_word(self, w):
		"""Process a token, update the corresponding register (if necessary)
		"""
		bpp = self.b - self.p
		w_hash = self.hash(w) & ((1 << self.b) - 1)
		bucket_index = w_hash >> bpp
		hash_value = w_hash & ((1 << bpp) - 1)
		self.buckets[bucket_index] = \
			max(self.buckets[bucket_index], self.leading_zeroes(hash_value, bpp))
		if self.plot:
			self.histogram.append(bucket_index)

	def add_hyperloglog(self, h):
		assert self.b == h.b, "Cannot merge HLogLogs with different number of bits"
		assert self.p == h.p, "Cannot merge HLogLogs with different number of buckets"
		# The maximum can be expressed as the componentwise 
		self.buckets = np.maximum(self.buckets, h.buckets)

	def get_estimation(self):
		"""Return the estimation of the cardinality as the harmonic mean
		of the registries
		"""
		return float(self.buckets.shape[0]) / np.mean(1.0 / (2.0 ** self.buckets))

	def plot_result(self):
		if self.plot:
			import pylab as plt
			plt.figure()
			plt.plot(self.histogram)
			plt.savefig("hloglog.png")