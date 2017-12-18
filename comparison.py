import time

import rng # custom RNG, rng.py
import math
import random # for Python's MT PRNG

import os # for urandom

import matplotlib.pyplot as plt
import numpy as np
import scipy.special # for erfc, gammainc

IMG_DIR = 'img/'


# name: name of the RNG being tested (for output and filenames)
# samples: number of random values to draw. Must be a square number
# gen: lambda producing a list of random values.
def test_rng(name, samples, gen):
	print("Testing " + str(samples) + " samples from: " + name)
	# generate values until we reach the desired number of samples
	values = list()

	gen_start_time = time.time() * 1000.0
	while(len(values) < samples):
		values += gen()
		# print(values)
		# print(len(values))

	gen_end_time = time.time() * 1000.0
	print("Generated " + str(samples) + " samples in " + str(gen_end_time - gen_start_time) + "ms.")

	# truncate at number of samples
	values = values[:samples]

	# frequency plot
	plt.figure()
	plt.title(name)
	plt.hist(values, 256)
	plt.savefig(IMG_DIR + name + '_' + str(samples) + '_freq.png', bbox_inches='tight')
	print("Frequency histogram saved.")

	# byte heatmap
	plt.figure()
	plt.title(name)
	heatgrid = np.reshape(values, (int(math.sqrt(samples)), int(math.sqrt(samples))))
	plt.imshow(heatgrid)
	plt.savefig(IMG_DIR + name + '_' + str(samples) + '_bytegrid.png', bbox_inches='tight')
	print("Byte grid saved.")

	# make equivalent bit array from byte array
	values_bits = list()

	for val in values:
		for bit in '{:08b}'.format(val): # convert byte to bits
			values_bits.append(int(bit))

	# bit heatmap
	plt.figure()
	plt.title(name)
	heatgrid_rows = int(len(values_bits) / (4 * int(math.sqrt(samples))))
	headgrid_cols = int(len(values_bits) / heatgrid_rows)
	heatgrid_bits = np.reshape(values_bits, (heatgrid_rows, headgrid_cols))
	plt.imshow(heatgrid_bits)
	plt.savefig(IMG_DIR + name + '_bitgrid.png', bbox_inches='tight')
	print("Bit grid saved.")

	# frequency monobit test

	# Add all 1's, convert 0's into -1's
	num_ones = np.sum(values_bits)
	num_zeros = len(values_bits) - num_ones
	S_n = num_ones - num_zeros
	S_obs = abs(S_n) / math.sqrt(len(values_bits))
	p = scipy.special.erfc(S_obs / math.sqrt(2))

	print("Frequency monobit test: p = " + str(p))

	def frequency_block_test(M):
		# frequency block test
		freq_blocks = list() # freq_blocks will be a list of blocks
		cur_block = list() # each block is a list

		BLOCK_SIZE = M

		for bit in values_bits:
			if(len(cur_block) >= BLOCK_SIZE):
				freq_blocks.append(cur_block)
				cur_block = list()
			cur_block.append(bit)

		# find proportions of ones. The NIST paper calls this pi.
		freq_proportions = list()
		for block in freq_blocks:
			freq_proportions.append(np.sum(block) / len(block))

		chi_sq = 0
		for prop in freq_proportions:
			chi_sq += (prop - (0.5)) ** 2

		chi_sq = chi_sq * 4 * BLOCK_SIZE
		p = scipy.special.gammainc(len(freq_blocks) / 2, chi_sq / 2)
		print("Frequency block test, M=" + str(BLOCK_SIZE) + ", p=" + str(p))

	frequency_block_test(8)
	frequency_block_test(128)

	# runs test
	ones_prop = np.sum(values_bits) / len(values_bits)

	def r(k):
		if(k+1 >= len(values_bits)):
			return 1
		if(values_bits[k] == values_bits[k+1]):
			return 0
		else:
			return 1

	V_n = 0
	for k in range(0, len(values_bits)):
		V_n += r(k)

	V_n += 1

	p = scipy.special.erfc(math.fabs(V_n - ( 2 * len(values_bits) * ones_prop * (1 - ones_prop))) / (2 * math.sqrt(2 * len(values_bits)) * ones_prop * (1 - ones_prop)))
	print("Runs test: p=" + str(p))

# Linux's /dev/urandom true RNG
test_rng('urandom', 10000, lambda: os.urandom(20))
# test_rng('urandom', 1000000, lambda: os.urandom(20))

# # python's built-in PRNG
test_rng('python', 10000, lambda: ((random.getrandbits(8)) for _ in range(20)))
# test_rng('python', 1000000, lambda: ((random.getrandbits(8)) for _ in range(20)))

# use our custom RNG
test_rng('custom', 10000, lambda: rng.generate())
# test_rng('custom', 1000000, lambda: rng.generate())