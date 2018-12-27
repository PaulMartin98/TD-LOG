import matplotlib.image as mpimg
import numpy as np
import pprint as pp
img = mpimg.imread("test_img.png")

height , width = img.shape[0],img.shape[1]
new_img = np.zeros((height,width))
print(img)
# for i in range(height):
#     for j in range(width):
#         print(img[i][j])
# new_img = (img[:,:,0]+ img[:,:,1]+ img[:,:,2])/3 > 0.9
new_img = img[:,:,3]>0.9
pp.pprint (new_img)
