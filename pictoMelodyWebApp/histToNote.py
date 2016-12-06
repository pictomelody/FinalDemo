import cv2
import numpy as np
from scipy.signal import argrelextrema
import random


# Final list consisting of all note information.
# Format - 2D array with indices as follows:
# [0] = note name
# [1] = octave
# [2] = frequency
# [3] = wavelength
NOTES_LIST = np.array([['C', 0, 16.351, 20.812],
                       ['C#', 0, 17.324, 19.643],
                       ['D', 0, 18.354, 18.54],
                       ['D#', 0, 19.445, 17.5],
                       ['E', 0, 20.601, 16.518],
                       ['F', 0, 21.827, 15.59],
                       ['F#', 0, 23.124, 14.716],
                       ['G', 0, 24.499, 13.89],
                       ['G#', 0, 25.956, 13.11],
                       ['A', 0, 27.5, 12.374],
                       ['A#', 0, 29.135, 11.68],
                       ['B', 0, 30.868, 11.024],
                       ['C', 1, 32.703, 10.405],
                       ['C#', 1, 34.648, 9.821],
                       ['D', 1, 36.708, 9.27],
                       ['D#', 1, 38.891, 8.75],
                       ['E', 1, 41.203, 8.259],
                       ['F', 1, 43.654, 7.795],
                       ['F#', 1, 46.249, 7.358],
                       ['G', 1, 48.999, 6.945],
                       ['G#', 1, 51.913, 6.555],
                       ['A', 1, 55, 6.187],
                       ['A#', 1, 58.27, 5.84],
                       ['B', 1, 61.735, 5.512],
                       ['C', 2, 65.406, 5.203],
                       ['C#', 2, 69.296, 4.911],
                       ['D', 2, 73.416, 4.635],
                       ['D#', 2, 77.782, 4.375],
                       ['E', 2, 82.407, 4.129],
                       ['F', 2, 87.307, 3.898],
                       ['F#', 2, 92.499, 3.679],
                       ['G', 2, 97.999, 3.472],
                       ['G#', 2, 103.826, 3.278],
                       ['A', 2, 110, 3.094],
                       ['A#', 2, 116.541, 2.92],
                       ['B', 2, 123.471, 2.756],
                       ['C', 3, 130.813, 2.601],
                       ['C#', 3, 138.591, 2.455],
                       ['D', 3, 146.832, 2.318],
                       ['D#', 3, 155.563, 2.187],
                       ['E', 3, 164.814, 2.065],
                       ['F', 3, 174.614, 1.949],
                       ['F#', 3, 184.997, 1.839],
                       ['G', 3, 195.998, 1.736],
                       ['G#', 3, 207.652, 1.639],
                       ['A', 3, 220, 1.547],
                       ['A#', 3, 233.082, 1.46],
                       ['B', 3, 246.942, 1.378],
                       ['C', 4, 261.626, 1.301],
                       ['C#', 4, 277.183, 1.228],
                       ['D', 4, 293.665, 1.159],
                       ['D#', 4, 311.127, 1.094],
                       ['E', 4, 329.628, 1.032],
                       ['F', 4, 349.228, 0.974],
                       ['F#', 4, 369.994, 0.92],
                       ['G', 4, 391.995, 0.868],
                       ['G#', 4, 415.305, 0.819],
                       ['A', 4, 440, 0.773],
                       ['A#', 4, 466.164, 0.73],
                       ['B', 4, 493.883, 0.689],
                       ['C', 5, 523.251, 0.65],
                       ['C#', 5, 554.365, 0.614],
                       ['D', 5, 587.33, 0.579],
                       ['D#', 5, 622.254, 0.547],
                       ['E', 5, 659.255, 0.516],
                       ['F', 5, 698.456, 0.487],
                       ['F#', 5, 739.989, 0.46],
                       ['G', 5, 783.991, 0.434],
                       ['G#', 5, 830.609, 0.41],
                       ['A', 5, 880, 0.387],
                       ['A#', 5, 932.328, 0.365],
                       ['B', 5, 987.767, 0.345],
                       ['C', 6, 1046.502, 0.325],
                       ['C#', 6, 1108.731, 0.307],
                       ['D', 6, 1174.659, 0.29],
                       ['D#', 6, 1244.508, 0.273],
                       ['E', 6, 1318.51, 0.258],
                       ['F', 6, 1396.913, 0.244],
                       ['F#', 6, 1479.978, 0.23],
                       ['G', 6, 1567.982, 0.217],
                       ['G#', 6, 1661.219, 0.205],
                       ['A', 6, 1760, 0.193],
                       ['A#', 6, 1864.655, 0.182],
                       ['B', 6, 1975.533, 0.172],
                       ['C', 7, 2093.005, 0.163],
                       ['C#', 7, 2217.461, 0.153],
                       ['D', 7, 2349.318, 0.145],
                       ['D#', 7, 2489.016, 0.137],
                       ['E', 7, 2637.021, 0.129],
                       ['F', 7, 2793.826, 0.122],
                       ['F#', 7, 2959.955, 0.115],
                       ['G', 7, 3135.964, 0.109],
                       ['G#', 7, 3322.438, 0.102],
                       ['A', 7, 3520, 0.097],
                       ['A#', 7, 3729.31, 0.091],
                       ['B', 7, 3951.066, 0.086],
                       ['C', 8, 4186.009, 0.081],
                       ['C#', 8, 4434.922, 0.077],
                       ['D', 8, 4698.636, 0.072],
                       ['D#', 8, 4978.032, 0.068],
                       ['E', 8, 5274.042, 0.065],
                       ['F', 8, 5587.652, 0.061],
                       ['F#', 8, 5919.91, 0.057],
                       ['G', 8, 6271.928, 0.054],
                       ['G#', 8, 6644.876, 0.051],
                       ['A', 8, 7040, 0.048],
                       ['A#', 8, 7458.62, 0.046],
                       ['B', 8, 7902.132, 0.043],
                       ['C', 9, 8372.018, 0.041],
                       ['C#', 9, 8869.844, 0.038],
                       ['D', 9, 9397.272, 0.036],
                       ['D#', 9, 9956.064, 0.034],
                       ['E', 9, 10548.084, 0.032],
                       ['F', 9, 11175.304, 0.03],
                       ['F#', 9, 11839.82, 0.029],
                       ['G', 9, 12543.856, 0.027],
                       ['G#', 9, 13289.752, 0.026],
                       ['A', 9, 14080, 0.024],
                       ['A#', 9, 14917.24, 0.023],
                       ['B', 9, 15804.264, 0.022]])


# Image to Intensity
# Given an image, returns a numpy type array containing
# number of pixels at intensities 0 - 255.
def img_to_intensity(input_img):
    """
    :param input_img: Image to be processed.
    :return: numpy type array of pixel intensities.
    """
    # Convert image to gray scale and copy into variable.
    gray_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    # Calculate intensity histogram.
    hist_int = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
    # Convert histogram to numpy array.
    return np.array(hist_int)


# Global and Local Extrema
# Given a numpy type array, return the indices of all minimum
# and maximum that occur (within a threshold order).
def global_local_extrema(arr):
    """
    :param arr: nupy type array.
    :return: numpy type array of indices of local and
    global extrema of arr.
    """
    # Calculate global min and max of arr.
    max_global = np.argmax(arr)
    min_global = np.argmin(arr)
    # Calculate local min and max of arr.
    max_local = argrelextrema(arr, np.greater, order=1)
    min_local = argrelextrema(arr, np.less, order=1)
    # Return two separate arrays.
    return np.append(max_local[0], max_global), \
        np.append(min_local[0], min_global)


# Map to Wavelength
# Given two points on the range 0-255, map the distance
# between the points and match to the closest wavelength
# in the NOTES_LIST array declared previously.
def map_to_wavelength(pt_small, pt_large):
    """
    :param pt_small: Small point value.
    :param pt_large: Large point value.
    :return: Index of closest wavelength mapped to distance.
    """
    # Calculate distance between points on 0-255 range.
    dist = pt_large - pt_small
    # Map to range 0.022-20.812 (the full range of
    # wavelengths from notes B9 to C0)
    mapped_dist = dist * .081529 + .022

    # Access only wavelengths of NOTES_LIST.
    wavelengths = NOTES_LIST[:, 3].astype('float')
    # Calculate closest wavelength and return.
    return (np.abs(wavelengths - mapped_dist)).argmin()

def showMeTheNote(img):
    img_arr = img_to_intensity(img)
    max_arr, min_arr = global_local_extrema(img_arr)
    note_index = map_to_wavelength(max_arr[int(len(max_arr)*random.random())],
                                   max_arr[int(len(max_arr)*random.random())])
    return NOTES_LIST[note_index]

if __name__ == "__main__":
    # Import image into program.
    img = cv2.imread('Horizon.png')

    # Create numpy array of image intensities and stores
    # max and min values accordingly.
    img_arr = img_to_intensity(img)
    max_arr, min_arr = global_local_extrema(img_arr)

    note_index = map_to_wavelength(0, 255)
    print 'Note: ' + NOTES_LIST[note_index][0] + '\n' \
          'Octave: ' + NOTES_LIST[note_index][1] + '\n' \
          'Frequency: ' + NOTES_LIST[note_index][2] + '\n' \
          'Wavelength: ' + NOTES_LIST[note_index][3] + '\n'
