import sys
import os
import math
import random
from tqdm import tqdm

from scenes import * 
sys.path.append("./src/core/")
from geometry import * 
from hitable import * 
from shape import * 
from camera import * 
from material import * 
from texture import * 
from sampler import * 
import numpy as np
import matplotlib.pyplot as plt
import cProfile
MAX_FLOAT = sys.float_info.max

def de_nan(c: vec3): 
    if math.isnan(c[0]):
        c[0] = 0
    if math.isnan(c[1]):
        c[1] = 0
    if math.isnan(c[2]):
        c[2] = 0
    return c 
def color(r: ray, world: hitable, light_shape: hitable, depth = 0,max_depth = 4):
    hit_anything,hrec = world.hit(r,0.001,MAX_FLOAT)
    if (hit_anything):
        #scattered = ray(vec3(0,0,0),vec3(0,0,0),0.0)
        # albedo = vec3(0,0,0)
        # pdf_val = 0.0
        # if_scatter,(scattered,albedo,pdf_val) = rec.mat.scatter(r,rec)
        emitted = hrec.mat.emitted(r,hrec,hrec.u,hrec.v,hrec.p)
        if_scatter,srec = hrec.mat.scatter(r,hrec)
        if (depth < max_depth and if_scatter):
            if srec.is_specular:
                return srec.attenuation * color(srec.specular_ray,world,light_shape,depth + 1,max_depth)
            plight = hitable_pdf(light_shape,hrec.p)
            p = mixture_pdf(plight,srec.prob_density)
            scattered = ray(hrec.p,p.generate(),r.time)
            pdf_val = p.value(scattered.direction)
            scattering_pdf = hrec.mat.scattering_pdf(r,hrec,scattered)

            return emitted + srec.attenuation * scattering_pdf * color( scattered,world, light_shape, depth + 1,max_depth) / pdf_val
        else:
            return emitted
    else:
        return vec3(0,0,0)


def main(filename: str = 'output',output_res: tuple = (200,100),num_samples= 100):
    nx = output_res[0];
    ny = output_res[1];
    num_samples = num_samples
    output = np.zeros((nx,ny,3)).tolist()
    hit_object_list = [] 
    R = math.cos(math.pi/4)
    aspect_ratio = float(nx)/float(ny)
    hit_object_list,cam = cornell_box(aspect_ratio)
    light_shape = xz_rect(213,343,227,332,554,0)
    glass_sphere = sphere(vec3(190,90,190),90,0)
    sample_list = hitable_list([light_shape,glass_sphere])
    #hit_object_list,cam = random_scene(aspect_ratio)
    seed = 123
    sampler = uniform_sampler_2D(seed)
    # sampler = stratified_sampler_2D(num_samples,seed)
    with tqdm(total = ny * nx) as pbar:
        for j in range(ny-1 ,-1,-1):
            for i in range(0,nx):
                col = vec3(0,0,0)
                samples = sampler.generate_n_samples_uv(num_samples)
                for s in samples: 
                    u,v = s
                    #print(" i: {} u:{} j: {}, v: {} ".format(i,u,j,v))
                    s = (i + u)/nx
                    t = (j + v)/ny
                    r = cam.get_ray(s,t)
                    col += de_nan(color(r,hitable_list(hit_object_list),sample_list,depth = 0,max_depth = 4))
                col /= float(num_samples)
                #col = vec3(math.sqrt(col[0]),math.sqrt(col[1]),math.sqrt(col[2]))
                ir = 255.99 * math.sqrt(col[0]);
                ig = 255.99 * math.sqrt(col[1]);
                ib = 255.99 * math.sqrt(col[2]);

                ir = (max(0,min(ir,255)))
                ig = (max(0,min(ig,255)))
                ib = (max(0,min(ib,255)))
                output[i][j] = [ir,ig,ib]

                pbar.update(1)
                #f.write(str(ir)  +  " "  +  str(ig) +  " "  + str(ib) + "\n");

    plt.imsave(filename + ".png",np.rot90(np.array(output)).astype(np.uint8))
    #f.close()

if  __name__ == "__main__":
    #main("./test_large_2048",output_res = (800,800),num_samples = 2048)
    #main("./test_medium_1024",output_res = (500,500),num_samples = 1024)
    main("./test_small_1024",output_res = (400,300),num_samples = 1024)
    #main("./test_small_256",output_res = (400,300),num_samples = 256)




