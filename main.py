#!/usr/bin/env python3
import argparse
import re
import sys
from tabulate import tabulate

from chord import Chord, NOTES_REGEX

def calculate_roman(progression, tonic=None):
    to_roman = {
        0: 'I',
        1: 'bII',
        2: 'II',
        3: 'bIII',
        4: 'III',
        5: 'IV',
        6: 'bV',
        7: 'V',
        8: 'bVI',
        9: 'VI',
        10: 'bVII',
        11: 'VII',
    }

    chords = {}

    for chord in progression:
        diff = chord - tonic
        num = to_roman[diff]

        if chord.is_minor():
            num = num.lower()

        chords[chord.name] = num

    print(tabulate(chords.items(), tablefmt='plain'))

def valid_note(value):
    if not re.match(NOTES_REGEX, value):
        raise argparse.ArgumentTypeError(f'Invalid note: {value}')
    return value

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    # parser.add_argument('-t', '--tonic', type=valid_note, required=True)
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
    for chord in chords:
        print(f'{chord.name}: {" ".join(chord.notes())}')

    # calculate_roman(chords, Chord(args.tonic))
