import cv2
import numpy as np
import sys
sys.path.append("..")
from myPackage import tools as tl
from os.path import join, altsep, basename
import matplotlib.pyplot as plt

def is_ok_4(point):
    point = np.array(point) // 255
    if point[0][0] + point[0][1] > 1:
        return False
    if point[0][1] + point[0][2] > 1:
        return False
    if point[0][2] + point[1][2] > 1:
        return False
    if point[1][2] + point[2][2] > 1:
        return False
    if point[2][2] + point[2][1] > 1:
        return False
    if point[2][1] + point[2][0] > 1:
        return False
    if point[2][0] + point[1][0] > 1:
        return False
    if point[1][0] + point[0][0] > 1:
        return False
    return True

def is_ok_5(point):
    point = np.array(point) // 255
    
    if (point[0][0] + point[2][2] > 1 and (point[0][1] + point[1][2] > 1 or point[1][0] + point[2][1] > 1)):
        return False
    if (point[2][0] + point[0][2] > 1 and (point[0][1] + point[1][0] > 1 or point[1][2] + point[2][1] > 1)):
        return False
    if (point[0][0] + point[2][2] > 1 and (point[0][1] + point[2][1] > 1 or point[1][0] + point[1][2] > 1)):
        return False
    if (point[2][0] + point[0][2] > 1 and (point[0][1] + point[2][1] > 1 or point[1][2] + point[1][0] > 1)):
        return False
    
    return True

def process(skeleton, name, plot= False, path= None):
    print("Minutiae extraction...")
    img = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)
    (h,w) = skeleton.shape[:2]
    if path is not None:
        filename = name+'.txt'
        full_name = altsep.join((path, filename))
        file = open(full_name, 'w')
        #file.write('# (x, y) position of minutiae and type as class (0: termination, 1: bifurcation)\n')

    for i in range(h):
        for j in range(w):
            if skeleton[i, j] == 255:
                # En caso de valer 255 se analizan sus vecinos,
                # para saber si se trata de una terminación o de una bifurcación
                
                window = skeleton[i - 1:i + 2, j - 1:j + 2]
                neighbours = sum(window.ravel()) // 255
                left = skeleton[i-8:i+9, j-40:j]
                right = skeleton[i-8:i+9, j+1:j+40]
                left_neighbours = sum(left.ravel()) // 255
                right_neighbours = sum(right.ravel()) // 255
                
                if neighbours != 2 and neighbours < 4:
                    continue
                
                isolate = 0
                for k in range(1, 10):
                    x = 0
                    xleft = max({i-k, 0})
                    xright = min({i+k+1, h-1})
                    yleft = max({j-k, 0})
                    yright = min({j+k+1, w-1})
                    x = sum(skeleton[xleft, yleft:yright]) + sum(skeleton[xright, yleft:yright])
                    x += sum(skeleton[xleft:xright, yleft]) + sum(skeleton[xleft:xright, yright])
                    if x == 0:
                        isolate = 1
                        break
                
                if isolate:
                    continue
                    
                if neighbours == 2 and left_neighbours>30 and right_neighbours>30:
                    # En caso de que los vecinos sean igual a 2 (Contando el mismo píxel que se analiza)
                    # se trataría de una terminación y esta se almacenaría en el archivo fichero,
                    # también se dibuja en la imágenes un circulo de color verde.
                    if path is not None:
                        #.write(str(i) + ',' + str(j) + ',0\n')
                        file.write(str(i) + ',' + str(j) + '\n')
                    cv2.circle(img, (j, i), 1, (0, 255, 0), 1)

                if (neighbours == 4 and is_ok_4(window)) or (neighbours > 4 and is_ok_5(window)):
                    # En caso de que los vecinos sean mayores a 3 (Contando el mismo píxel que se analiza)
                    # se trataría de una bifurcación y esta se almacenaría en el archivo fichero,
                    # también se dibuja en la imágenes un circulo de color rojo.
                    if path is not None:
                        #file.write(str(i) + ',' + str(j) + ',1\n')
                        file.write(str(i) + ',' + str(j) + '\n')
                    cv2.circle(img, (j, i), 1, (255, 0, 0), 1)
                
    if plot:
        img2 = cv2.resize(img, (img.shape[1] * 2, img.shape[0] * 2))
        cv2.imshow("Minutiae '{}'".format(name), img2)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    p = [[0, 0, 0],
         [255, 255, 0],
         [0, 255, 0]]
    print(is_ok_5(p))