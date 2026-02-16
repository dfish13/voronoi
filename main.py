from PIL import Image
import numpy as np
import random
import math


height = 1024
width = 1024
num_cells = 50

def random_color():
	r = random.randint(0, 255)
	g = random.randint(0, 255)
	b = random.randint(0, 255)
	return (r, g, b)

def random_point(h, w):
	x = float(random.randint(0, h))
	y = float(random.randint(0, w))
	return (x, y)

class VoronoiCell():
	def __init__(this, h, w):
		this.color = random_color()
		this.point = random_point(h, w)

class Line():
	def __init__(this, p1, p2):
		x1, y1 = p1
		x2, y2 = p2
		this.a = x1 - x2;
		this.b = y1 - y2;
		this.c = (x2**2 - x1**2 + y2**2 - y1**2) / 2;

	def distance_to_point(this, p):
		x, y = p
		d = math.sqrt(this.a**2 + this.b**2)
		n = this.a * x + this.b * y + this.c
		return n / d

def distance(p1, p2, verbose=False):
	s = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 
	if verbose:
		print(s)
	return s


def closest_point_color(i, j, cells):
	min_k = 0
	min_distance = 100000000
	for k in range(len(cells)):
		d = distance((i, j), cells[k].point)
		if d < min_distance:
			min_k = k
			min_distance = d
	return cells[min_k].color

def mix_cells(cells, i, j):
	border = 1
	l = Line(cells[0].point, cells[1].point)
	d = l.distance_to_point((i, j))
	if d >= border:
		return cells[0].color
	if d <= -border:
		return cells[1].color
	d += border
	d /= (2 * border)
	return mix_color(cells[0].color, cells[1].color, d, 1 - d)

def mix_color(x, y, a, b):
	return tuple(a * x[i] + b * y[i] for i in range(3))


def anti_alias_color(i, j, cells):
	min_k = 0
	min_distance = 100000000
	for k in range(len(cells)):
		d = distance((i, j), cells[k].point)
		if d < min_distance:
			min_k = k
			min_distance = d

	min_k2 = 0
	min_distance = 100000000
	close_cells = [cells[min_k]]
	for k in range(len(cells)):
		if k == min_k:
			continue
		d = distance((i, j), cells[k].point)
		if d < min_distance:
			min_k2 = k
			min_distance = d

	close_cells.append(cells[min_k2])
	return mix_cells(close_cells, i, j)


cells = list(VoronoiCell(height, width) for i in range(num_cells))

pixel_array = np.ones((height,width, 3), dtype=np.uint8)
pixel_array2 = np.ones((height,width, 3), dtype=np.uint8)

for i in range(height):
	for j in range(width):
		pixel_array[i][j] = closest_point_color(i, j, cells)

for i in range(height):
	for j in range(width):
		pixel_array2[i][j] = anti_alias_color(i, j, cells)

image = Image.fromarray(pixel_array)
image.save('normal.png')
image = Image.fromarray(pixel_array2)
image.save('anti_alias.png')
