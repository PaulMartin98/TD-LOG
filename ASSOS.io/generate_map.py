
import matplotlib.image as mpimg
import numpy as np
import pprint as pp

def get_map (filename,c = 1):
    img = mpimg.imread(filename)

    height , width = img.shape[0],img.shape[1]
    # new_img = np.zeros((height,width))
    # for i in range(height):
    #     for j in range(width):
    #         print(img[i][j])
    # new_img = (img[:,:,0]+ img[:,:,1]+ img[:,:,2])/3 > 0.9
    new_img = img[:,:,3]>0.9
    new_tab = [0]*(width*height)
    for i in range(height):
        for j in range(width):
            new_tab[i+height*j] = int(new_img[i,j])
    return new_tab, width, height
