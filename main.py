#!/usr/bin/env python3
from chord import Chord

# chords = 'G Em G Em C D C D G Em C D C D G'

"""
Major scale
major, major, min, major, major, major, minor

---------------
 C |  0 | I
 D |  2 | II
 E |  4 | III
 F |  5 | IV
 G |  7 | V
 A |  9 | VI
 B | 11 | VII
 C | 12 | VIII
---------------

"""

# diff = chords[1] - chords[0]
# print(diff)

# for n in 'CDEFGAB':
#     diff = Chord(n) - Chord('C')
#     print(diff)

def calculate_roman(progression, tonic=None):
    pass

# ii7 V7 I7
chords = 'Dm7 G7 C7'
chords = chords.split()
chords = [Chord(c) for c in chords]

for c in chords:
    print(c)

calculate_roman(chords, Chord('C'))
