#!/usr/bin/env python3
import argparse
import re
import sys
from tabulate import tabulate

from chord import Chord, NOTES_REGEX

"""
---------------
 C |  0 | I
 D |  2 | II
 E |  4 | III
 F |  5 | IV
 G |  7 | V
 A |  9 | VI
 B | 11 | VII

 C |  0 | I
 C |  1 | bII
 C |  1 | #I
 D |  2 | II
 D |  3 | #II
 D |  3 | bIII
 E |  4 | III
 F |  5 | IV
 F |  6 | bV
 F |  6 | #IV
 G |  7 | V
 G |  8 | #V
 G |  8 | bVI
 A |  9 | VI
 A | 10 | #VI
 A | 10 | bVII
 B | 11 | VII
---------------

"""

def calculate_roman(progression, tonic=None):
    to_roman = {
        0: 'I',
        2: 'II',
        4: 'III',
        5: 'IV',
        7: 'V',
        9: 'VI',
        11: 'VII',
    }

    chords = {}

    for chord in progression:
        diff = chord - tonic
        num = to_roman[diff]

        if chord.is_minor():
            num = num.lower()

        ext = chord.ext if chord.ext is not None else ''
        chords[chord.name] = f'{num}{ext}'

    print(tabulate(chords.items(), tablefmt='plain'))

def valid_note(value):
    if not re.match(NOTES_REGEX, value):
        raise argparse.ArgumentTypeError(f'Invalid note: {value}')
    return value

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('-t', '--tonic', type=valid_note, required=True)
    return parser.parse_args()

def chords_from_input(inp):
    chords = []
    for line in inp:
        line = line.split()
        chords += [Chord(c) for c in line]
    return chords

if __name__ == '__main__':
    args = get_args()
    chords = chords_from_input(args.input)

    calculate_roman(chords, Chord(args.tonic))
