
import matplotlib.image as mpimg
import numpy as np
import pprint as pp

def get_connex (map):
    height , width = map.shape[0], map.shape[1]

    UF = (-1)*np.ones((height,width))

    ite = 0
    U = np.zeros((height*width))
    E = []

    def find_pxl():
        i,j = 0,0
        to_find , current = False, (0,0)
        while i < width and (not(to_find)):
            while j < height and (not(to_find)):
                if U[i,j] == 0 and map[i,j] == 1:
                    to_find , current = True, (i,j)
        return current, to_find

    def in_limits(pos):
        return 0<= pos[0] < height and 0<= pos[1] < width

    def add_neighboors(current):
        i,j = current[0], current[1]
        N = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
        for k in range(4):
            if in_limits(N[k]):
                E.append(N[k])



    current, tofind = find_pxl()
    UF[current[0],current[1]] = ite
    U[current[0],current[1]] = 1

    while(tofind):
        add_neighboors ( current )
        while E != []:
            current = E[0]
            UF[current[0],current[1]] = ite
            add_neighboors ( current )
            U[current[0],current[1]] = 1
        ite += 1
        current, tofind = find_pxl()
    return UF, ite

def get_contour(UF,ite):
    height , width = UF.shape[0], UF.shape[1]

    contour = [[]]*ite
    U = np.zeros((height,width))

    def find_contour(k):
        i,j = 0,0
        to_find , pxl = False, (0,0)

        def non_pxl_neighboors(i,j):
            is_border, pxl = False, []
            N = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
            for x in N:
                if UF[x[0],x[1]]==-1:
                    is_border, pxl = True, x
                    break
            return is_border, pxl

        while i < width and (not(to_find)):
            while j < height and (not(to_find)):
                if UF[i,j] == k:
                    is_border, pxl = non_pxl_neighboor (i,j)
                    to_find , current = True, (i,j)
        return current, to_find

    for k in range(ite):
        current = find_contour(k,UF)

def get_map (filename):
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
