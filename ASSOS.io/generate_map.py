
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
    new_tab = np.zeros((height,width))
    for i in range(height):
        for j in range(width):
            new_tab[i,j] = int(new_img[i,j])

    height_c, width_c = int(height/c), int(width/c)
    new_tab_c =  [0]*(height_c*width_c)

    for i in range(height_c):
        for j in range(width_c):
            i1,i2 = i*c, min((i+1)*c, height)
            j1, j2 = j*c, min((j+1)*c, width)

            new_tab_c[i+height*j] = int(new_tab[i1:i2,j1:j2].sum()/(i2-i1)/(j2-j1) > 0.5)

    return (new_tab_c,width_c,height_c)
