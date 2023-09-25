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
    "Invalid chord"

class Chord:
    def __init__(self, s):
        self.parse(s)

    def match_pop(self, regex, s):
        """Match the beginning of a string and pop off matches."""
        m = re.match(f'^{regex}', s)
        if m is not None:
            match = m.group(1)
            s = s[m.end():]

            if match == '':
                match = None
            return match, s
        return None, s

    def parse(self, s):
        """
        (This is borrowed from ChordPro's documentation.)

        * A root note, e.g. C, F#, or Bb
        * An optional qualifier, e.g. m (minor), aug (augmented)
        * An optional extension, e.g. 7, maj9
        * An optional bass, a slash / followed by another root note

        """
        NOTES = r'[ABCDEFG](b|#)?'

        components = [
            {'name': 'root',      'regex': f'({NOTES})'},
            {'name': 'qualifier', 'regex': r'(m(?!aj)|-)'},
            {'name': 'extension', 'regex': r'([^/]*)'},
            {'name': 'bass',      'regex': f'/({NOTES})'},
        ]

        for c in components:
            value, s = self.match_pop(c['regex'], s)
            setattr(self, c['name'], value)

        if self.root is None:
            raise InvalidChordError()

    def __sub__(self, other):
        a_tone = NOTES[self.root]
        b_tone = NOTES[other.root]
        if a_tone < b_tone:
            a_tone += OCTAVE
        return a_tone - b_tone

    def __repr__(self):
        keys = ['root', 'qualifier', 'extension', 'bass']
        d = {}

        for k in keys:
            value = getattr(self, k)

            if value is not None:
                d[k] = value

        return str(d)

if __name__ == '__main__':
    # TODO: Write some tests.
    chord = 'Bbm9/F'
    chord = 'B/F'
    chord = 'Ebmaj7/G'
    chord = 'Em7/G'
    c = Chord(chord)
    print(c)
