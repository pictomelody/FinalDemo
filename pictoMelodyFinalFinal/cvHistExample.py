import sys

sys.path.append('C:\Python2.7\Lib\site-packages')
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Import image into program.
def showHistogram(img, plot):
    # Display only selected plots.
    #plot_code = [x.upper() for x in list(raw_input('Enter plots to display (CLAHE, GREY, BGR): ').split())]
    plot_code = [plot]
    key_code = []
    # Convert image to gray scale and copy into variable.
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Create histogram of CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # Plot resulting histogram.
    if 'CLAHE' in plot_code:
        CLAHE = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_CLAHE = CLAHE.apply(gray_img)
        hist_CLAHE = cv2.calcHist([img_CLAHE], [0], None, [256], [0, 256])
        print hist_CLAHE
        plt.plot(hist_CLAHE, color='c')
        plt.xlim([0, 256])
        key_code.append('CLAHE')

    # Create histogram for pixel intensity (in grey scaled image).
    # Plot resulting histogram.
    if 'GREY' in plot_code:
        hist_int = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
        plt.plot(hist_int, color='k')
        plt.xlim([0, 256])
        key_code.append('Grey')

    # Create histograms for separate blue, green, and red elements of image separately.
    # Plot all histograms with respective colors.
    if 'BGR' in plot_code:
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist_color = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist_color, color=col)
            plt.xlim([0, 256])
        key_code.append('Blue')
        key_code.append('Green')
        key_code.append('Red')

    print plot_code

    # Display graphs.
    plt.legend(key_code, loc='upper left')
    plt.show()
