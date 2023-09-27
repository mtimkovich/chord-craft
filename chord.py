import re

NOTES = {
    'A':  0,
    'A#': 1,
    'Bb': 1,
    'B':  2,
    'C':  3,
    'C#': 4,
    'Db': 4,
    'D':  5,
    'D#': 6,
    'Eb': 6,
    'E':  7,
    'F':  8,
    'F#': 9,
    'Gb': 9,
    'G':  10,
    'G#': 11,
    'Ab': 11,
}

# Octave is 12 semitones.
OCTAVE = 12

class InvalidChordError(Exception):
    pass

class Chord:
    def __init__(self, s):
        self.parse(s)

    def parse(self, s):
        """
        (This is borrowed from ChordPro's documentation.)

        * A root note, e.g. C, F#, or Bb
        * An optional qualifier (qual), e.g. m (minor), aug (augmented)
        * An optional extension (ext), e.g. 7, maj9
        * An optional bass, a slash / followed by another root note

        """
        NOTES = r'[ABCDEFG](b|#)?'
        regex = f'({NOTES})(m(?!aj)|-)?([^/]+)?(/({NOTES}))?'

        m = re.match(regex, s)

        if m is None:
            raise InvalidChordError(f'Could not parse given chord: {s}')

        self.root = m.group(1)
        self.qual = m.group(3)
        self.ext = m.group(4)
        self.bass = m.group(6)

    # TODO: Create a function that enumerates the notes of the chord.

    def __sub__(self, other):
        """Return difference in semitones between the roots of 2 chords."""
        a_tone = NOTES[self.root]
        b_tone = NOTES[other.root]
        if a_tone < b_tone:
            a_tone += OCTAVE
        return a_tone - b_tone

    def __repr__(self):
        keys = ['root', 'qual', 'ext', 'bass']
        d = {}

        for k in keys:
            value = getattr(self, k)

            if value is not None:
                d[k] = value

        return str(d)

if __name__ == '__main__':
    # TODO: Write some tests.
    chord = 'Bbm9/F'
    # chord = 'C'
    # chord = 'B/F'
    # chord = 'Ebmaj7/G'
    chord = 'Em7/G'
    # chord = 'Z7'
    c = Chord(chord)
    print(c)
