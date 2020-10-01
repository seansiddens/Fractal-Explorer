import fractals
import seaborn as sns
import numpy as np
from PIL import Image, ImageEnhance
import time
start_time = time.time()

if __name__ == "__main__":
    b = fractals.Buddhabrot(3500, 2000, 1000000)
    b.render_color()
    b.display()
    b.save('images/test-bf1.png')

    #col_map = 'inferno'
    # m = fractals.Mandelbrot(1750, 1000, 1000)
    # m.render(col_map)
    # m.display()
    # m.save('images/' + col_map + '.png')

    # bs = fractals.BurningShip(800, 600, 50)
    # bs.render(col_map)
    # bs.display()
    # bs.save('images/burning_ship_' + col_map + '.png')

    total_time = time.time() - start_time
    print(round(total_time, 2), "s")

