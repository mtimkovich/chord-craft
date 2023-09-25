#!/usr/bin/env python3
from chord import Chord

# chords = 'G Em G Em C D C D G Em C D C D G'
chords = 'Dm7 G7 C7'
chords = chords.split()
chords = [Chord(c) for c in chords]

for c in chords:
    print(c)

diff = chords[1] - chords[0]
print(diff)
