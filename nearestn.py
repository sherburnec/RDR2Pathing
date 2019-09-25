"""
1. select a city as current city.
2. find out the shortest edge connecting the current city and an unvisited city.
3. set the new city as current city.
4. mark the previous current city as visited.
5. if all the cities are visited, then terminate.
6. Go to step 2.
"""

import numpy as np
import random
import math
import cv2

path = []
DV = 2
L=4
dist_dict = {}
def ree():
	print("REEEEEEEEEEEEEEEEEEEEEEEEEEE")

def get_contents(file_name):
	"""
	Acquires a list of points from a given text file and returns an array of City objects
	"""
	key = []
	with open(file_name) as f:
		for l in f:
			temp = l.split(':')
			temp[1] = tuple(temp[1].replace(" ", "").split(","))
			temp[2] = int(temp[2])
			if temp[2] <= DV:
				key.append(City(temp[0], temp[1], temp[2]))
	build_dist_dict(key)
	return key

def build_dist_dict(cities):
	for c in cities:
		dist_dict[c.name] = {}

	for c in cities:
		for d in cities:
			dist_dict[c.name][d.name] = c.dist(d)


class City:
	def __init__ (self, name="", coords=(0,0), d=3):
		self.name = name
		self.x = int(coords[0])
		self.y = int(coords[1])
		self.d = d #Shovel Required 1 for digging; 2 for metal detector
		if self.d == 0: #Blue for no shovel
			self.color = (255, 0, 0)
		elif d == 1: #Red for shovel
			self.color = (0, 255, 0)
		elif d == 2: #Green for metal detector
			self.color = (0, 0, 255)
		else: #Something went wrong
			self.color = (255, 255, 255)
	def __str__(self):
		return self.name
	def dist(self, other_city):
		"""
		Gets the distance between self and a given city. Returns float
		"""
		return math.sqrt( (self.x - other_city.x) ** 2 + (self.y - other_city.y) ** 2)

class Path:
	"""
	Path object
		path is a list of City objects
		dist is the total distnace for said path
	"""
	def __init__(self, path, dist):
		self.path = path
		self.dist = dist

def best_route(points):
	"""
	Compare each path's total distance and choose the lowest one
	Returns the Path with the lowest total distance
	"""
	best_dist = None
	for p in points:
		path, total_dist = pathing(p, points)
		current_path = Path(path, total_dist)
		if best_dist is None:
			best_path = current_path
		elif total_dist < best_dist:
			best_path = current_path
	return best_path

def pathing(p1, points): 
	"""
	Build a possible path one city at a time
	"""
	distance = 0 
	current = p1
	points.pop(points.index(p1))
	trek = []
	trek.append(p1)
	count = 0
	while len(points) > 0:
		if(L == 1):
			temp_point, dist = next_city(current, points, L)
		else:
			if len(points) > 1:
				temp_point, dist = next_city(current, points, L)
			else:
				temp_point = points[0]
				dist = current.dist(temp_point)
		trek.append(temp_point)
		distance += dist
		# points.remove(temp_point)
		points.pop(points.index(temp_point))
		current = temp_point
		count += 1
	return trek, distance

def next_city(p1, points, layer, total_dist=0):
	"""
	Determine the next closest city
	hypotenuse of map is 9000 units so 10000 is used as the intitilized distance

	Returns a City and int that is the closest
	"""
	distance = 10000 * layer
	best_combined = 10000 * layer
	front_runner = City()
	if layer == L:
		print(layer)
	for p in points:
		temp = points[:]
		p_dist = dist_dict[p1.name][p.name] + total_dist
		if(layer > 1):
			# temp_points = points
			temp.remove(p)
			boink, combined_dist = next_city(p, temp, layer - 1, p_dist)
			if combined_dist < best_combined:
				best_combined = combined_dist
				distance = p_dist
				front_runner = p
		elif(layer == 1):
			if(p_dist < distance):
				distance = p_dist
				front_runner = p
		else:
			exit(1)
	return front_runner, distance

def draw_circles(img, point):
	"""
	Draws a circle and the x, y from the given City "point"
	Returns an image object from cv2
	"""
	r = 10
	c = (point.x, point.y)
	t = 2
	img = cv2.circle(img, c, r, point.color, t)
	return img

def draw_line(img, point1, point2):
	"""
	Draws a line from City1 (point1) to City2 (point2)
	Returns an image object from cv2
	"""
	p1 = (point1.x, point1.y)
	p2 = (point2.x, point2.y)
	c = (255, 255, 255)
	t = 2
	img = cv2.line(img, p1, p2, c, t )
	return img

points = get_contents('tarot_swords.txt')

path = best_route(points)

print(path.dist)

image = cv2.imread('map.png')
for p in path.path:
	image = draw_circles(image, p)


prev = None
for p in path.path: #
	if prev is None:
		pass
	else:
		image = draw_line(image, prev, p)
	prev = p

cv2.imwrite('map_adjusted' + str(DV) + '.png', image)