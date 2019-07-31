# PyTrace

![image2](./references/final_scene.png)

A (nearly) pure Ray Tracing Project for Python

This work is based off the books [Ray Tracing: The Rest of Your Life](https://github.com/RayTracing/raytracingtherestofyourlife) by Peter Shirley but ported to Python. 

#### To run, simply run pypy3 main.py or python main.py

dependencies include: 
1. pypy3 (note all other dependencies must be installed within pypy3)
2. numpy 
3. matplotlib
4. tqdm
5. noise

Technically, you can run w/o pypy3 installed but it is very slow w/o the JIT compilation, as seen below 

## Benchmarks: 
Note: Iterations per second are how many output pixels are processed per second 
 