import sys

sys.path.append('C\Annie\Python2.7\Lib\site-packages')

import numpy as np
import cv2

#problem: can't run code from Atom, works fine from terminal

def matrix_transpose(matrix):
    """
    returns the matrix transpose
    """
    row_num = len(matrix)
    column_num = len(matrix[0])

    matrix_t = [[] for i in xrange(column_num)] #Create an empty row in matrix_t for each column in matrix to transpose.

    for i in xrange(row_num): #row
        for j in xrange(column_num): #column
            matrix_t[j].append(matrix[i][j])    #As matrix parses through rows, matrix_t parses through columns.

    return matrix_t

def averageColorBox(pixelbox):
    """
    Finds the average bgr color of a box of pixels
    """
    blue_sum = 0
    green_sum = 0
    red_sum = 0
    x = len(pixelbox)
    y = len(pixelbox[0])

    for i in xrange(x):
        for j in xrange(y):
            blue_sum += pixelbox[i][j][0]
            green_sum += pixelbox[i][j][1]
            red_sum += pixelbox[i][j][2]

    #average of: blue, green, red for the pixelbox
    average_colors = [blue_sum/(x*y), green_sum/(x*y), red_sum/(x*y)]

    return (average_colors)

#writing class for image dimensions
class ImageDimensions:
    #Image dimension variables
    #dimensions = ['n', 'width', 'height', 'width_box', 'height_box', 'xrem', 'yrem']
    #n = number of boxes in one dimension (so total number of boxes = 5x5)
    def __init__(self, img, n):
        img_size = img.shape
        self.width = img_size[0] #xsize
        self.height = img_size[1] #ysize
        self.width_box = self.width/n #width of each box
        self.height_box = self.height/n #height of each box
        self.xrem = self.width%n #when image can't be evenly split into 5x5
        self.yrem = self.height%n #there will be a x and y remainder

def averageColorGrid(image_filename, n):
    img = cv2.imread(image_filename)
    img_dim = ImageDimensions(img, n)

    avgcolor = [] #avgcolor is a 25-element list of the average colors of the image
    box_matrix = [] #each element of box_matrix is a box of pixels

    #turns image into grid. there should be 25 2-D boxes
    for i in xrange(n):

        y1 = i*img_dim.height_box #upper limit of box height
        y2 = y1+img_dim.height_box #lower limit of box height
        #is it on the bottom of the grid? if so, then add the y padding
        if i+1 == n:
            y2 += img_dim.yrem

        for j in xrange(n):
            x1 = j*img_dim.width_box
            x2 = x1+img_dim.width_box
            #is it on the right of the grid? if so, then add the x padding
            if j+1 == n:
                x2 += img_dim.xrem
            box_matrix.append(img[x1:x2, y1:y2]) #each element of box_matrix is a 2D box

    box_matrix = np.array(box_matrix)

    for i in xrange(len(box_matrix)):
        avgcolor.append(averageColorBox(box_matrix[i]))

    temp_avg = [[] for i in xrange(n)]

    #turning temp_avg into a 5x5 matrix for better viewing
    for i in xrange(n):
        for j in xrange(n):
            temp_avg[i].append(avgcolor[i*n+j])

    temp_avg = matrix_transpose(temp_avg)

    cv2.imwrite("Average-Color.png", np.array(temp_avg))
    return avgcolor

if __name__ == "__main__":
    print(averageColorGrid("Cat-With-Glasses1.jpg", 5))
