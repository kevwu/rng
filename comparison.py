import time

import rng # custom RNG, rng.py
import math
import random # for Python's MT PRNG

import os # for urandom

import matplotlib.pyplot as plt
import numpy as np
import scipy.special # for erfc

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
		print(len(values))

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

	if(p >= 0.01):
		print("The sequence is believed to be random.")
	else:
		print("The sequence is not believed to be random.")

	# frequency block test


# Linux's /dev/urandom true RNG
test_rng('urandom', 10000, lambda: os.urandom(20))
test_rng('urandom', 1000000, lambda: os.urandom(20))

# # python's built-in PRNG
test_rng('python', 10000, lambda: ((random.getrandbits(8)) for _ in range(20)))
test_rng('python', 1000000, lambda: ((random.getrandbits(8)) for _ in range(20)))


# use our custom RNG
test_rng('custom', 10000, lambda: rng.generate())
test_rng('custom', 1000000, lambda: rng.generate())