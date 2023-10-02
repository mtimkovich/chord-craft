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

    # TODO: Convert b to # when appropriate.
    0:  'A',
    1:  'Bb',
    2:  'B',
    3:  'C',
    4:  'Db',
    5:  'D',
    6:  'Eb',
    7:  'E',
    8:  'F',
    9:  'Gb',
    10: 'G',
    11: 'Ab',
}

NOTES_REGEX = r'[ABCDEFG](b|#)?'

# Octave is 12 semitones.
OCTAVE = 12

def semitone_plus(start: str, n: int):
    """Add semitones to a note and return the resulting note."""
    tone = NOTES[start] + n
    return NOTES[tone % OCTAVE]

class InvalidChordError(Exception):
    pass

class Chord:
    def __init__(self, name):
        self.name = name
        self.parse(name)

    def parse(self, name):
        """
        (This is borrowed from ChordPro's documentation.)

        * A root note, e.g. C, F#, or Bb
        * An optional qualifier (qual), e.g. m (minor), aug (augmented)
        * An optional extension (ext), e.g. 7, maj9
        * An optional bass, a slash / followed by another root note

        """
        regex = f'({NOTES_REGEX})(m(?!aj)|-)?([^/]+)?(/({NOTES_REGEX}))?'

        m = re.match(regex, name)

        if m is None:
            raise InvalidChordError(f'Could not parse given chord: {s}')

        self.root = m.group(1)
        self.qual = m.group(3)
        self.ext = m.group(4)
        self.bass = m.group(6)

    def notes(self):
        the_notes = [self.root]
        if self.is_minor():
            the_notes.append(semitone_plus(self.root, 3))
        else:
            the_notes.append(semitone_plus(self.root, 4))
        the_notes.append(semitone_plus(self.root, 7))

        # TODO: Make this less hacky.
        if self.ext == '7':
            the_notes.append(semitone_plus(self.root, 10))
        elif self.ext == 'maj7':
            the_notes.append(semitone_plus(self.root, 11))

        return the_notes

    def is_minor(self):
        return self.qual in {'m', '-'}

    def is_major(self):
        return not self.is_minor()

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
    # chord = 'Bbm9/F'
    # chord = 'C'
    # chord = 'B/F'
    # chord = 'Ebmaj7/G'
    # chord = 'Em7/G'
    # chord = 'Z7'
    chord = 'Ebmaj7'
    c = Chord(chord)
    print(c.notes())
