import random
import sys
import os
import numpy
from mingus.containers import *
import mingus.core.keys
#import mingus.midi.fluidsynth
import mingus.core.progressions as progressions

from mingus.core import notes

def make_progression(base_chord, major):
    temp = notes.note_to_int(base_chord)
    base_chord = notes.int_to_note(temp, 'b')
    if (major):
        return progressions.to_chords(['I', 'V', 'VIm', 'IV'], base_chord)
    else:
        return progressions.to_chords(['Im', 'Vm', 'VI', 'IVm'], base_chord)
#function returns a (basic) chord progression for a given base chord
def alternative_progression(key,major):
    if major: #major
        first = notes.int_to_note((notes.note_to_int(key) + 9)%12)
        second = notes.int_to_note((notes.note_to_int(key) + 7)%12)
        third = notes.int_to_note((notes.note_to_int(key) + 5)%12)
        return [[key,True],[first, False], [second, True], [third, True]]
    else: #minor
        first = notes.int_to_note((notes.note_to_int(key) + 3)%12)
        second = notes.int_to_note((notes.note_to_int(key) + 7)%12)
        third = notes.int_to_note((notes.note_to_int(key) + 5)%12)
        return [[key,False],[first, True], [second, False], [third, False]]
#returns a list of alternate base chords in that key that go well with main progression

#happy = major
def create_random_track(key, happy):
    newTrack= Track()
    progressionChoice = alternative_progression(key, happy)
    for i in range (0,4):
        curBar = Bar(key, (4, 4))
        useProgression = progressionChoice[random.choice(range(0, len(progressionChoice)))]
        progressionChoice.remove(useProgression)
        Progression = make_progression(useProgression[0], useProgression[1])
        for j in range(0,4):
            prevChord=False
            while curBar.current_beat<1:
                if (prevChord):
                    chordIndex= prevInd+ random.choice([1,-1])
                    #the current chord is nect to the previous one in the progression
                    if chordIndex==-1:
                        chordIndex=3
                    elif chordIndex==4:
                        chordIndex=0
                else:
                    chordIndex=random.choice(range(0,4))
                prevChord=True
                curBar.place_notes(Progression[chordIndex], 4)
                prevInd=chordIndex
            newTrack+curBar
    return newTrack

if __name__ == "__main__":
    print create_random_track('C',True)
    mingus.midi.fluidsynth.play_Track(create_random_track('C',True),1,120) #example track, plays on channel 1 at 120 bpm
