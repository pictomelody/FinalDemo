import sys

sys.path.append('C:\Python27\Lib\site-packages')

import cv2
from pictoMelodyWebApp import musicAndColor as musc
import pictoMelodyWebApp.Music as muscno
from pictoMelodyWebApp.averageColor import averageColorGrid
from pictoMelodyWebApp.averageColor import ImageDimensions
from pictoMelodyWebApp.histToNote import showMeTheNote
#Global variables
image_filename = "Horizon.png"
avg_image_filename = "Average-Color.png"
avgcolor_img = ""
n = 5

#x_img = cv2.imread(x_image)
print("Average Color Array: ")
print(averageColorGrid(image_filename, n))

img = cv2.imread(image_filename)
img_dim = ImageDimensions(img, n)
img_avg = cv2.imread(avg_image_filename)
most_avg = musc.more_average(img_avg)
octave = musc.pick_octave(img_avg)
key = musc.pick_key(most_avg)

if musc.pick_major(img_avg, n) == "major":
    major = True
else:
    major = False

print("most_avg: ", most_avg)
print("Music Info: ")
print("Octave: ", octave)
print("Major: ", major)
print("Key: ", key)
print("Notes: ")

track = muscno.create_random_track(key, major)

#print(track)

print("Track length: ", len(track))

#b = "cegb"
#bar = Lilypond.from_Bar(b)
#print(bar)
#Lilypond.to_png(bar,"my_first_bar")
#for bar in track:
#    print("Bar: ", bar)

"""
print(track[0][3])
print(track[0][3][2])
print(track[0][3][2][0])
dot = track[0][3][2][0]
print(type(dot))
print(dot.name)
print(type(dot.name))

melodyNote = showMeTheNote(img)

print ('Note: ' + melodyNote[0])
print (melodyNote[0].lower())
"""
lilypitchu = ""
count = 0
filename = "testSheet.ly" #sheet music for bass chords
version = "\\version \"2.16.0\"  % necessary for upgrading to future LilyPond versions." #REQUIRED to run w/ Lilypond
with open(filename,'w') as w:
    """
    version
    {
      <<
        \newStaff
          {
            \clef "treble"
            \time 4/4
          }
      >>
    }
    """
    w.write(version + "\n")
    w.write("{\n") #opening brakets

    w.write("  <<\n    \\new Staff\n      {\n") #staff opening brackets
    w.write("        \\clef \"treble\"\n")
    w.write("        \\time 4/4\n")
    #melody
    for i in xrange(64):
        melody_note = showMeTheNote(img)
        melody_note = melody_note[0]
        w.write(melody_note[:1].lower() + "\' ")
        if i%4 == 0 and i>0:
            w.write("\n" + "          " )


    w.write("    }\n") #staff closing brackets

    w.write("    \\new Staff\n      {\n") #staff opening brackets
    w.write("        \\clef \"bass\"\n")
    w.write("        \\time 4/4\n")
    #bass chords
    for bar in track:
        for chord in bar:
            lilypitchu = "          "
            note1 = (chord[2][0].name).lower()
            note2 = (chord[2][1].name).lower()
            note3 = (chord[2][2].name).lower()
            if chord == None:
                lilypitchu += r4
            else:
                lilypitchu += "<" + note1[:1].lower()
                lilypitchu += " " + note2[:1].lower()
                lilypitchu += " " + note3[:1].lower() + ">"
            w.write(lilypitchu + "\n")

    w.write("    } >>\n") #staff closing brackets
    w.write("}") #closing brackets

print(count)
#convert track to pasrable string
#write file to test.ly here
#open file
# ' = octave up
#, = octave down
#http://lilypond.org/doc/v2.14/Documentation/learning/simple-notation

"""
print("Graphs: ")
#Graphs for each average color box
for i in xrange(n):
    y1 = i*img_dim.height_box #upper limit of box height
    y2 = y1+img_dim.height_box
    for j in xrange(n):
        x1 = j*img_dim.width_box
        x2 = x1+img_dim.width_box
        img_box = img[x1:x2, y1:y2]
        showHistogram(img_box, "BGR")
"""
