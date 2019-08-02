from geometry import * 
from math import *
from hitable import * 
import random
from abc import ABC,abstractmethod


'''
randomly sample direction through unit disk
'''
def random_in_unit_disk():
	p = vec3(1.0,1.0,1.0)
	while p.dot(p) >= 1.0:
		p = 2.0 * vec3(random.random(),random.random(),0) - vec3(1,1,0)
	return p

'''
randomly sample a direction on the unit sphere
'''
def random_unit_sphere():
    p = vec3(1,1,1)
    while p.squared_length() >= 1.0:
        p = 2.0 * vec3(random.random(),random.random(),random.random()) - vec3(1.0,1.0,1.0)
    return p 

'''
generate random cosine direction on the unit hemisphere
'''
def random_cosine_direction():
	r1 = random.random()
	r2 = random.random()
	z = sqrt(1-r2)
	phi = 2 * pi * r1
	x = cos(phi) * 2 * sqrt(r2)
	y = sin(phi) * 2 * sqrt(r2)
	return vec3(x,y,z)

class pdf(ABC):
	def __init__(self):
		pass
	def value(self,direction: vec3):
		return 0
	def generate(self):
		return 0

class cosine_pdf(pdf):
	def __init__(self,w: vec3):
		self.uvw = onb()
		self.uvw.build_from_w(w)
	def value(self,direction: vec3):
		cosine = unit_vector(direction).dot(self.uvw.axis[2])
		if cosine > 0.0:
			return cosine/pi
		else:
			return 0.0
	def generate(self):
		return self.uvw.local(random_cosine_direction())

class hitable_pdf(pdf):
	def __init__(self,p, origin: vec3):
		self.p = p
		self.o = origin
	def value(self,direction):
		return self.p.pdf_value(self.o,direction)
	def generate(self):
		return self.p.random_gen(self.o)

class mixture_pdf(pdf):
	def __init__(self,p0: pdf,p1: pdf):
		self.p = []
		self.p.append(p0)
		self.p.append(p1)
	def value(self,direction: vec3):
		return 0.5 * self.p[0].value(direction) + 0.5 * self.p[1].value(direction)
	def generate(self):
		if random.random() < 0.5:
			return self.p[0].generate()
		else:
			return self.p[1].generate() 

def random_to_sphere(radius: float, distance_squared: float): 
	# print("radius: {}, distance_squared: {}" .format(radius,distance_squared))
	# print("{}".format((radius ** 2)/distance_squared))
	r1 = random.random()
	r2 = random.random()
	z = 1 + r2 * (sqrt(1 - (radius * radius)/distance_squared) - 1)
	phi = 2 * pi * r1
	x = cos(phi)*sqrt(1 - z * z)
	y = sin(phi) * sqrt(1 - z * z)
	return vec3(x,y,z)






