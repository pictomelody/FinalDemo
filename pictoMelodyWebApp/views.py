from django.shortcuts import render, render_to_response

import sys

sys.path.append('C:\Python27\Lib\site-packages')

import numpy as np
import cv2
import mingus.extra.lilypond as Lilypond
import mingus.core.notes as notes
import musicAndColor as musc
import Music as muscno
from averageColor import averageColorGrid
from averageColor import ImageDimensions
#from cvHistExample import showHistogram
from histToNote import showMeTheNote
import random
import json
import urllib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def detect1(request):
    print request, "hello"
    notes = [["A5"], ["B5"],["C5"], ["D5"], ["E5"], ["F5"], ["G5"],["A#4"], ["B#4"],["C#4"], ["D#4"], ["E#4"], ["F#4"], ["G#4"],
              ["Ab4"], ["Bb4"],["Cb4"], ["Db4"], ["Eb4"], ["Fb4"], ["Gb4"], ["A3"], ["B3"],["C3"], ["D3"], ["E3"], ["F3"], ["G3"],
              ["A4"], ["B4"], ["C4"], ["D4"], ["E4"], ["F4"], ["G4"],["A4"], ["B4"],["C4"], ["D4"], ["E4"], ["F4"], ["G4"],]
    notesheet = [notes[i] for i in sorted(random.sample(xrange(len(notes)), 12))]
    # notesheet = [["F4"],["G4"],["Ab4"],["C4"],["D4"]]
    key = "Eb"
    if request.method == 'POST':

        print request.POST.get('url'), "url"
        array = detect(request)
        if array is not None:
            notesheet = array[0]
            key = array[1]#untab if need to test url function

    return render(request, "Pictomelody.html", {"notesheet": notesheet, "key":key})

def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)

    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()

        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()

        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image

@csrf_exempt
def detect(request):

    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        print request.FILES.get('image')
        print request.FILES
        print request.FILES.get('image', None)

        if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])
            print image

        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            url = request.POST.get('url')

            # if the URL is None, then return an error

            if len(url)==0 or  url is None:
                data["error"] = "No URL provided."
                return None

            # load the image and convert
            image = _grab_image(url=url)

        # Global variables
        image_filename = image
        avg_image_filename = "C:\Users\TJ\picto\music_generator\Average-Color.png"
        avgcolor_img = ""
        n = 5

        #img = cv2.imread(image_filename)
        #img_dim = ImageDimensions(image, n)
        #img_avg = cv2.cv.LoadImage(avg_image_filename,CV_LOAD_IMAGE_COLOR)
        #print img_avg
        most_avg = musc.more_average(image)
        octave = musc.pick_octave(image)
        key = musc.pick_key(most_avg)
        if musc.pick_major(image, n) == "major":
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
        track = clean_up(track)
        print track

        return (track, key)

        #print("Track length: ", len(track))

        #Write to sheet music --no longer needed
        # # lilypitchu = ""
        # count = 0
        # filename = "testSheet.ly"  # sheet music for bass chords
        # version = "\\version \"2.16.0\"  % necessary for upgrading to future LilyPond versions."  # REQUIRED to run w/ Lilypond
        # with open(filename, 'w') as w:
        #     w.write(version + "\n")
        #     w.write("{\n")  # opening brakets
        #
        #     w.write("  <<\n    \\new Staff\n      {\n")  # staff opening brackets
        #     w.write("        \\clef \"treble\"\n")
        #     w.write("        \\time 4/4\n")
        #     # melody
        #     for i in xrange(64):
        #         melody_note = showMeTheNote(image)
        #         melody_note = melody_note[0]
        #         w.write(melody_note[:1].lower() + "\' ")
        #         if i % 4 == 0 and i > 0:
        #             w.write("\n" + "          ")
        #
        #     w.write("    }\n")  # staff closing brackets
        #
        #     w.write("    \\new Staff\n      {\n")  # staff opening brackets
        #     w.write("        \\clef \"bass\"\n")
        #     w.write("        \\time 4/4\n")
        #     # bass chords
        #     for bar in track:
        #         for chord in bar:
        #             lilypitchu = "          "
        #             note1 = (chord[2][0].name).lower()
        #             note2 = (chord[2][1].name).lower()
        #             note3 = (chord[2][2].name).lower()
        #             if chord == None:
			# pass
        #                # lilypitchu += r4
		 #    else:
        #                 lilypitchu += "<" + note1[:1].lower()
        #                 lilypitchu += " " + note2[:1].lower()
        #                 lilypitchu += " " + note3[:1].lower() + ">"
        #             w.write(lilypitchu + "\n")
        #
        #     w.write("    } >>\n")  # staff closing brackets
        #     w.write("}")  # closing brackets
        # data.update({"success": True})
        # return render_to_response('Pictomelody.html')

def clean_up(a):
    a = a[1]
    b = []
    for i in a:
        for j in i[2]:
            b.append([str(j).replace("-","").replace('\'','')])

    return b
