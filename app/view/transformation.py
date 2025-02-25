import os
from PIL import Image, ImageChops
import numpy as np


path_images_directory = os.path.abspath('images')
path_turn_90 = os.path.abspath('turn_90')
path_turn_270 = os.path.abspath('turn_270')
black_white = os.path.join('black$white')
path_turn_180 = os.path.abspath('turn_180')
files = os.listdir(path_images_directory)


def make_filter():
    for file in files:
        if file.endswith(".png"):
            image = Image.open(os.path.join(path_images_directory, file))
            x, y = image.size
            pixels = image.load()
            for i in range(x):
                for j in range(y):
                    if pixels[i, j] == 0:
                        pixels[i, j] = 1
                    else:
                        pixels[i, j] = 0
            image.save(os.path.join(black_white, file.split('.png')[0] + 'black&white' + '.png'))
            image.transpose(Image.ROTATE_90).save(os.path.join(path_turn_90,
                                                               file.split('.png')[0] + 'turn_90' + '.png'))
            image.transpose(Image.ROTATE_270).save(os.path.join(path_turn_270,
                                                                file.split('.png')[0] + 'turn_270' + '.png'))
            image.transpose(Image.ROTATE_180).save(os.path.join(path_turn_180,
                                                                file.split('.png')[0] + 'turn_180' + '.png'))




