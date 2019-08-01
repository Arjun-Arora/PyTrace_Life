from geometry import * 
from math import *
import random

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