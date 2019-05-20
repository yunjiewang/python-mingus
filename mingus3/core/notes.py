#!/usr/bin/python
# -*- coding: utf-8 -*-

#    mingus - Music theory Python package, notes module.
#    Copyright (C) 2008-2009, Bart Spaans
#    Copyright (C) 2011, Carlo Stemberger
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Basic module for notes.

This module is the foundation of the music theory package.

It handles conversions from integers to notes and vice versa and thus
enables simple calculations.
"""

from .mt_exceptions import NoteFormatError, RangeError, FormatError

_note_dict = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11
}
fifths = ('F', 'C', 'G', 'D', 'A', 'E', 'B')
ns = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')  # sharp
nf = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')  # flat

_keys = (
        ('Cb', 'ab'),  #  7 b
        ('Gb', 'eb'),  #  6 b
        ('Db', 'bb'),  #  5 b
        ('Ab', 'f'),   #  4 b
        ('Eb', 'c'),   #  3 b
        ('Bb', 'g'),   #  2 b
        ('F', 'd'),    #  1 b
        ('C', 'a'),    #  nothing
        ('G', 'e'),    #  1 #
        ('D', 'b'),    #  2 #
        ('A', 'f#'),   #  3 #
        ('E', 'c#'),   #  4 #
        ('B', 'g#'),   #  5 #
        ('F#', 'd#'),  #  6 #
        ('C#', 'a#'),  #  7 #
)
_major_keys, _minor_keys = tuple(zip(*_keys))

def int_to_note(note_int, accidentals='#'):
    """Convert integers in the range of 0-11 to notes in the form of C or C#
    or Db.

    Throw a RangeError exception if the note_int is not in the range 0-11.

    If not specified, sharps will be used.

    Examples:
    >>> int_to_note(0)
    'C'
    >>> int_to_note(3)
    'D#'
    >>> int_to_note(3, 'b')
    'Eb'
    """
    if note_int not in range(12):
        raise RangeError('int out of bounds (0-11): %d' % note_int)
    if accidentals == '#':
        return ns[note_int]
    elif accidentals == 'b':
        return nf[note_int]
    else:
        raise FormatError("'%s' not valid as accidental" % accidentals)


def is_enharmonic(note1, note2):
    """Test whether note1 and note2 are enharmonic, i.e. they sound the same."""
    return note_to_int(note1) == note_to_int(note2)


def is_valid_note(note):
    """Return True if note is in a recognised format. False if not."""
    letter, accidentals = note[0], note[1:]
    if letter not in _note_dict:
        return False
    if any(acc not in "b#" for acc in accidentals):
        return False
    return True


def assert_valid_note(note):
    """Throw a NoteFormatError exception if the note format is not recognised."""
    if not is_valid_note(note):
        raise NoteFormatError("Unknown note format '%s'" % note)


def note_to_int(note):
    """Convert notes in the form of C, C#, Cb, C##, etc. to an integer in the
    range of 0-11.
    """
    # Check if input is valid
    assert_valid_note(note)

    # Check for '#' and 'b' postfixes
    val = _note_dict[note[0]]
    for post in note[1:]:
        if post == 'b':
            val -= 1
        elif post == '#':
            val += 1
    return val % 12


def reduce_accidentals(note):
    """Reduce any extra accidentals to proper notes.

    Example:
    >>> reduce_accidentals('C####')
    'E'
    """
    # Check if input is valid
    assert_valid_note(note)

    # Calculate note integer
    val = note_to_int(note[0])
    for token in note[1:]:
        if token == 'b':
            val -= 1
        elif token == '#':
            val += 1
        else:
            raise NoteFormatError("Unknown note format '%s'" % note)

    # Determine sharp or flat
    if val >= note_to_int(note[0]):
        return int_to_note(val % 12)
    else:
        return int_to_note(val % 12, 'b')


def remove_redundant_accidentals(note):
    """Remove redundant sharps and flats from the given note.

    Examples:
    >>> remove_redundant_accidentals('C##b')
    'C#'
    >>> remove_redundant_accidentals('Eb##b')
    'E'
    """
    # Check if input is valid
    assert_valid_note(note)

    # Calculate net accidentals
    val = 0
    for token in note[1:]:
        if token == 'b':
            val -= 1
        elif token == '#':
            val += 1
    result = note[0]

    # Cancel out redundancy
    while val > 0:
        result = augment(result)
        val -= 1
    while val < 0:
        result = diminish(result)
        val += 1
    return result


def augment(note):
    """Augment a given note.

    Examples:
    >>> augment('C')
    'C#'
    >>> augment('Cb')
    'C'
    """
    assert_valid_note(note)
    if note[-1] != 'b':
        return note + '#'
    else:
        return note[:-1]


def diminish(note):
    """Diminish a given note.

    Examples:
    >>> diminish('C')
    'Cb'
    >>> diminish('C#')
    'C'
    """
    assert_valid_note(note)
    if note[-1] != '#':
        return note + 'b'
    else:
        return note[:-1]


def to_minor(note):
    """Find relative minor key note"""
    assert_valid_note(note)
    return _minor_keys[_major_keys.index(note)]


def to_major(note):
    """Find relative major key note"""
    assert_valid_note(note)
    return _major_keys[_minor_keys.index(note.lower())]
