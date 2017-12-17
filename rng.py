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
	image_string = pygame.image.tostring(image, 'RGBA', False)
	
	img_bytes = bytearray(np.asarray(Image.frombytes('RGBA', (640,480), image_string)))
	h = hashlib.new('SHA256')
	h.update(img_bytes)

	values = list()
	for val in h.digest():
		values.append(val)

	return values
