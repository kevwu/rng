import pygame
import pygame.camera
from pygame.locals import *

import time

import hashlib

from PIL import Image

import numpy as np

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0", (640, 480))
cam.start()

IMG_DIR = 'img/'

def generate():
	image = cam.get_image()
	pygame.image.save(image, IMG_DIR + 'test.jpg')
	
	img_bytes = bytearray(np.asarray(Image.open(IMG_DIR + 'test.jpg')))
	h = hashlib.new('SHA1')
	h.update(img_bytes)

	values = list()
	for val in h.digest():
		values.append(val)

	print(len(values))

	return values
