#!/usr/bin/env python3
import argparse
import re
import sys
from tabulate import tabulate

from chord import Chord, NOTES_REGEX

def calculate_roman(args):
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

    progression = chords_from_input(args.input)
    tonic = Chord(args.tonic)

    chords = {}

    for chord in progression:
        diff = chord - tonic
        num = to_roman[diff]

        if chord.is_minor():
            num = num.lower()

        chords[chord.name] = num

    print(tabulate(chords.items(), tablefmt='plain'))

def print_notes(args):
    chords = chords_from_input(args.input)
    s = set()
    output = []
    for chord in chords:
        if chord.name in s:
            continue
        output.append([chord.name] + chord.notes())
        s.add(chord.name)

    print(tabulate(output, tablefmt='plain'))

def valid_note(value):
    if not re.match(NOTES_REGEX, value):
        raise argparse.ArgumentTypeError(f'Invalid note: {value}')
    return value

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help='chord input')
    subparsers = parser.add_subparsers()

    prog = subparsers.add_parser('progression', aliases=['prog', 'p'],
                                 help='Output chord progression')
    prog.add_argument('-t', '--tonic', type=valid_note, default='C')
    prog.set_defaults(func=calculate_roman)

    chords = subparsers.add_parser('chords', aliases=['c'], help='Print notes of chords')
    chords.set_defaults(func=print_notes)

    return parser.parse_args()

def chords_from_input(inp):
    chords = []
    for line in inp:
        line = line.split()
        chords += [Chord(c) for c in line]
    return chords

if __name__ == '__main__':
    args = get_args()
    args.func(args)
