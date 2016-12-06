import sys

sys.path.append('C\Annie\Python2.7\Lib\site-packages')
#sys.path.append('D\Annie\Music\SoundFont\ElPiano1.sf2')

import math
import colorsys
import numpy as np
import cv2
import mingus.core.notes as notes #lets me use notes and use basic functions
import mingus.core.scales as scales #diatonic library doesn't exist. it's just scales
from mingus.containers import MidiInstrument, NoteContainer, Note #use to store generated notes
#from mingus.midi import fluidsynth #play notes
import mingus.extra.lilypond as LilyPond

#D\Annie\Code\pictoMelody\musicAndColor\ElPiano1.sf2
#sf2 = 'ElPiano1.sf2'
#fluidsynth.fluid_patchset('D\Annie\Music\SoundFont\ElPiano1.sf2')
#fluidsynth.init('ElPiano1.sf2')
#n = Note("C-5")
#n.channel = 5
#n.velocity = 50
#fluidsynth.play_Note(n)

"""
Each pixel is = [b, g, r] where b, g, and r are (0, 255)
Calculate avg_b, avg_g, and avg_r
MINOR/MAJOR: The lower the avg of (avg_b, avg_g, avg_r), the more minor (darker/sadder). Basically, if low = minor.
-Low = (0, 127)
-High = (128, 255)
-The dark side (< 128, < 128, < 128)
OCTAVE: Scales with color avg and max octave
KEY: Colorwheel key
-http://biteyourownelbow.com/keychar.htm
-keys and color: http://zarathustra574.blogspot.com/2015/01/musical-keys-and-goethes-color-wheel.html
NOTE:

"""

def pick_major(avgcolor_img, n):
    cookie = 0 #If you come to the dark side, you get a cookie
    for block in avgcolor_img:
        for pixel in block:
            if pixel[0] < 128 and pixel[1] < 128 and pixel[2] < 128:
                cookie += 1
            if cookie > (n*n)/2:
                return "minor"
    return "major"

def more_average(avgcolor_img): #returns a list
    avg = [0, 0, 0] #average of average colors

    for block in avgcolor_img:
        for pixel in block:
            avg[0] += pixel[0]
            avg[1] += pixel[1]
            avg[2] += pixel[2]

    for i in xrange(len(avg)):
        avg[i] = avg[i]/25

    return(avg)

#Note: Piano has 8 octaves. let's just go with that (0-8)
def pick_octave(avgcolor_img):
    avg = more_average(avgcolor_img)
    octotal = 8
    factor = octotal/3
    rem = octotal%3
    sum_avg = avg[0] + avg[1] + avg[2]
    #print("factor: " + str(factor))
    #print("rem: " + str(rem))
    if rem == 2:
        if avg[0] < avg[1] and avg[0] < avg[2]: #if blue is lowest
            b_factor = factor
            g_factor = (factor + rem)
            r_factor = (factor + rem)
        if avg[1] < avg[0] and avg[1] < avg[2]: #if green is lowest
            b_factor = (factor + rem)
            g_factor = factor
            r_factor = (factor + rem)
        else:
            b_factor = (factor + rem)
            g_factor = (factor + rem)
            r_factor = factor

    elif rem == 1:
        if avg[0] > avg[1] and avg[0] > avg[2]: #if blue is largest
            b_factor = (factor + rem)
            g_factor = factor
            r_factor = factor
        if avg[1] > avg[0] and avg[1] > avg[2]: #if green is lowest
            b_factor = factor
            g_factor = (factor + rem)
            r_factor = factor
        else:
            b_factor = factor
            g_factor = factor
            r_factor = (factor + rem)

    else:
        b_factor = factor
        g_factor = factor
        r_factor = factor

    b_scale = (float(avg[0])/sum_avg)*b_factor
    g_scale = (float(avg[1]/sum_avg))*g_factor
    r_scale = (float(avg[2])/sum_avg)*r_factor

    octave = b_scale + g_scale + r_scale
    octave = int(math.ceil(octave))
    return octave

def pick_key(avgof_avgcolor_img):
    #http://stackoverflow.com/questions/23472290/why-is-the-conversion-between-rgb-and-hls-color-systems-imprecise
    dict_musickey = {50: 'C', 145: 'G', 0: 'D', 55: 'A', 140: 'E', 20:'B',
                     30: 'F#', 35: 'C#', 40: 'Ab', 240: 'Eb', 180: 'Bb', 60: 'F'}
    avg_r = avgof_avgcolor_img[2]
    avg_g = avgof_avgcolor_img[1]
    avg_b = avgof_avgcolor_img[0]
    #print("RGB: ", avg_r, avg_g, avg_b)
    h, l, s = colorsys.rgb_to_hls(float(avg_r)/255, float(avg_g)/255, float(avg_b)/255)
    #print("HLS: ", h, l, s)
    h = int(round(h * 360))
    l = int(round(l * 100))
    s = int(round(s * 100))
    pixel_hls = [h, l, s]

    h -= h%5

    while h not in dict_musickey:
        h+=5
    key = dict_musickey[h]

    return(key)
#
#
#
#
#
if __name__ == "__main__":
    image = "Average-Color.png"

    avgcolor_img = cv2.imread(image)

    cica = more_average(avgcolor_img)
    print (cica)

    octave = pick_octave(cica)
    print("Octave: " + str(octave))

    major = pick_major(avgcolor_img)
    print("Major/Minor?: " + major)

    #pixel_key = pick_key(avgcolor_img) #Note: Overflow error. do key later

    note_list = []
    note_list.append(notes.augment("C"))
    note_list.append(notes.int_to_note(138%12))
    print(note_list)
