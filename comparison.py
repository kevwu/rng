import time

import rng # custom RNG, rng.py
import math
import random # for Python's MT PRNG

import os # for urandom

import matplotlib.pyplot as plt
import numpy as np
import scipy.special

IMG_DIR = 'img/'

def test_rng(name, samples, gen):
	print("Testing: " + name)
	# generate values until we reach the desired number of samples
	values = list()
	while(len(values) < samples):
		values += gen()
		# print(values)
		# print(len(values))

	# truncate at number of samples
	values = values[:samples]

	# frequency plot
	plt.figure()
	plt.title(name)
	plt.hist(values, 256)
	plt.savefig(IMG_DIR + name + '_freq.png', bbox_inches='tight')

	# byte heatmap
	plt.figure()
	plt.title(name)
	heatgrid = np.reshape(values, (100, 100))
	plt.imshow(heatgrid)
	plt.savefig(IMG_DIR + name + '_bytegrid.png', bbox_inches='tight')

	# make equivalent bit array from byte array
	values_bits = list()

	for val in values:
		for bit in '{:08b}'.format(val): # convert byte to bits
			values_bits.append(int(bit))

	# bit heatmap
	plt.figure()
	plt.title(name)
	heatgrid_bits = np.reshape(values_bits, (320,250))
	plt.imshow(heatgrid_bits)
	plt.savefig(IMG_DIR + name + '_bitgrid.png', bbox_inches='tight')

# Linux's /dev/urandom true RNG
test_rng('urandom', 10000, lambda: os.urandom(20))

# python's built-in PRNG
test_rng('python', 10000, lambda: ((random.getrandbits(8)) for _ in range(20)))

# use our custom RNG
test_rng('custom', 10000, lambda: rng.generate())