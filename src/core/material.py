import sys
from math import * 
from hitable import * 
from geometry import *
from texture import * 
from random_functions import * 
from abc import ABC,abstractmethod
import random


class scatter_rec(ABC):
	def __init__(self,specular: ray = ray(vec3(0.0,0.0,0.0),vec3(0.0,0.0,0.0)),
					  is_specular: bool = False,attenuation: vec3 = vec3(0,0,0),
					 prob_density: pdf = None): 
		self.specular = specular
		self.is_specular = is_specular
		self.attenuation = attenuation
		self.prob_density = pdf 


'''
reflectivity polynomial appoximation
by Christophe Schlick
'''

def schlick(cosine: float, ref_idx: float):
	r0 = (1 - ref_idx) / (1 + ref_idx)
	r0 = r0 * r0
	return r0 + (1-r0) * pow((1-cosine),5)

'''
reflection about normal
'''
def reflect(incoming_vector: vec3, normal: vec3):
	outgoing_vector = incoming_vector - 2 * incoming_vector.dot(normal) * normal;
	return outgoing_vector


'''
refract and return refracted vector
'''
def refract(incoming_vector: vec3, normal: vec3, ni_over_nt: float):
	uv = unit_vector(incoming_vector)
	dt = uv.dot(normal)
	refracted = vec3(0,0,0)
	discriminant = 1.0 - ni_over_nt * ni_over_nt * (1-dt*dt)
	if(discriminant > 0):
		refracted = ni_over_nt * (uv - normal * dt) - normal * sqrt(discriminant)
		return True,refracted
	else:
		return False, refracted


'''
abstract material
'''
class material(ABC):
	def __init__(self):
		pass
	'''
	returns whether we scatter, along with scattered spectra and attentuated spectra
	'''
	def scatter(r_in: ray, hrec):
		return False,(0,0,0)
	'''
	base function so non-emissive materials don't emit anything
	'''
	def emitted(self, r_in: ray, rec,u: float, v: float, p: vec3):
		return vec3(0,0,0)

	def scattering_pdf(self,r_in: ray,rec, scattered: ray):
		return 0.0

class lambertian(material):
	def __init__(self,albedo: texture):
		self.albedo = albedo
		self.uvw = onb()
	def scattering_pdf(self,r_in: ray,rec, scattered: ray):
		cosine = rec.normal.dot(unit_vector(scattered.direction))
		if cosine < 0:
			cosine = 0.0
		return cosine/math.pi
	# now returns True, (scattered,albedo and pdf)
	def scatter(self,r_in: ray, hrec):
		# self.uvw.build_from_w(rec.normal)
		# direction = self.uvw.local(random_cosine_direction())
		# scattered = ray(rec.p,unit_vector(direction),r_in.time)
		# alb = self.albedo.value(rec.u,rec.v,rec.p)
		# pdf = (self.uvw.axis[2].dot(scattered.direction)) / math.pi
		srec = scatter_rec()
		srec.is_specular = False
		srec.attenuation = self.albedo.value(hrec.u,hrec.v,hrec.p)
		srec.prob_density = cosine_pdf(hrec.normal)	

		return True,srec

class metal(material):
	def __init__(self,albedo: vec3,f: float = 0.0):
		if f < 1.0:
			self.fuzz = f
		else:
			self.fuzz = 1.0
		self.albedo = albedo
	def scatter(self,r_in: ray, hrec):
		srec = scatter_rec()
		reflected = reflect(unit_vector(r_in.direction),hrec.normal)
		srec.specular_ray = ray(hrec.p,reflected + self.fuzz * random_unit_sphere())
		srec.attenuation = self.albedo
		srec.is_specular = True
		srec.prob_density = None
		return True,srec

class dielectric(material):
	def __init__(self,ri: float):
		self.ref_idx = ri
	def scatter(self,r_in: ray, hrec):
		srec = scatter_rec()
		srec.is_specular = True
		srec.prob_density = None
		srec.attenuation = vec3(1.0,1.0,1.0)

		outward_normal = None
		ni_over_nt = None
		refracted = None;
		scattered = None;
		reflected = reflect(r_in.direction,hrec.normal)
		attenuation = vec3(1.0,1.0,1.0)
		reflect_prob = None
		cosine = None

		if(r_in.direction.dot(hrec.normal) > 0):
			outward_normal = -hrec.normal
			ni_over_nt = self.ref_idx
			cosine = self.ref_idx * r_in.direction.dot(hrec.normal) / r_in.direction.length()
		else:
			outward_normal = hrec.normal
			ni_over_nt = 1.0/self.ref_idx
			cosine = -r_in.direction.dot(hrec.normal) / r_in.direction.length()

		if_refract,refracted = refract(r_in.direction,outward_normal,ni_over_nt)
		if if_refract:
			reflect_prob = schlick(cosine,self.ref_idx)
			#scattered = ray(rec.p,refracted)
		else:
			#scattered = ray(hrec.p,reflected,r_in.time)
			reflect_prob = 1.0
			#return False, (scattered,attenuation)
		if random.random() < reflect_prob:
			srec.specular_ray = ray(hrec.p,reflected,r_in.time)
		else: 
			srec.specular_ray = ray(hrec.p,refracted,r_in.time)

		return True,srec

'''

light material 

'''
class diffuse_light(material): 
	def __init__(self,tex: texture):
		self.emit = tex

	def scatter(self,r_in: ray, rec):
		'''
		diffuse light do not reflect, simply emit
		'''
		return False,(0,0,0)
	def emitted(self, r_in: ray, rec,u: float, v: float, p: vec3 ):
		'''
		return color associated w/ texture

		'''
		if rec.normal.dot(r_in.direction) < 0.0:
			return self.emit.value(u,v,p)
		else:
			return vec3(0,0,0)


'''

isotropic function

'''

class isotropic(material):
	def __init__(self,a: texture):
		self.albedo = a 
	def scatter(self,r_in: ray, rec):
		scattered = ray(rec.p,random_unit_sphere(),r_in.time)
		attenuation = self.albedo.value(rec.u,rec.v,rec.p)
		return True,(scattered,attenuation)








