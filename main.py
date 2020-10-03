import numpy as np
import cv2
import matplotlib.pyplot as plt

from diffusion_manager import DiffusionManager, ParticleDrawer

if __name__=="__main__":
    

    bottom_x = 50
    top_x = 500
    bottom_y = 50
    top_y = 500

    diffusion_manager = DiffusionManager(bottom_x, top_x, bottom_y, top_y)
    drawer = ParticleDrawer(bottom_x, top_x, bottom_y, top_y, diffusion_manager.border)

    n_left = 900
    n_right = 100
    diffusion_manager.init_particles(n_left, n_right)

    left_concentration, right_concentration = diffusion_manager.calc_concentration()
    drawer.draw(diffusion_manager.particles, left_concentration, right_concentration, n_left)


    counter = 0
    time_limit = 1000

    record_left = []
    record_right = []
    while(counter < time_limit):
        counter += 1
        cv2.waitKey(0)
        
        diffusion_manager.move_particles(20)
        left_concentration, right_concentration = diffusion_manager.calc_concentration()
        record_left.append(left_concentration)
        record_right.append(right_concentration)
        drawer.draw(diffusion_manager.particles, left_concentration, right_concentration, n_left)

    fig = plt.figure()
    plt.title('Concentration over Time')
    plt.plot(record_left, color='red', label='left concentration')
    plt.plot(record_right, color='blue', label='right concentration')
    plt.xlabel('Time')
    plt.ylabel('Concentration')
    fig.legend(loc="upper right")

    plt.show()