import os

from PIL import Image

path = './pic/pic ('
for num in range(1, 1003):
    im = Image.open(path + str(num) + ').jpg')
    im.resize((256, 256)).save(path + str(num) + ').jpg')
