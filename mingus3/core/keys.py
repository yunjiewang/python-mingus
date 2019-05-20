#!/usr/bin/python
# -*- coding: utf-8 -*-

#    mingus - Music theory Python package, keys module.
#    Copyright (C) 2010-2011, Carlo Stemberger
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

"""Module for dealing with keys.

This module provides a simple interface for dealing with keys.
"""

from .mt_exceptions import FormatError, NoteFormatError, RangeError
from . import notes
from itertools import cycle, islice

keys = (
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
major_keys, minor_keys = tuple(zip(*keys))
base_scale = ('C', 'D', 'E', 'F', 'G', 'A', 'B')  # scale consists all natural notes
_key_cache = {}  # cache for get_notes function


def is_valid_key(key):
    """Return True if key is in a recognized format. False if not."""
    result = any(key in keypairs for keypairs in keys)
    return result


def get_key(accidentals=0):
    """Return the key corresponding to accidentals.

    Return the tuple containing the major key corresponding to the
    accidentals put as input, and his relative minor; negative numbers for
    flats, positive numbers for sharps.
    """
    if accidentals not in range(-7, 8):
        raise RangeError('integer not in range (-7)-(+7).')
    return keys[accidentals+7]


def assert_valid_key(key):
    if not is_valid_key(key):
        raise NoteFormatError("unrecognized format for key '%s'" % key)


def get_key_signature(key='C'):  # Todo: rename to get_accidental_numbers
    """Return the key signature.

    0 for C or a, negative numbers for flat key signatures, positive numbers
    for sharp key signatures.
    """
    assert_valid_key(key)
    if key[0].isupper():
        accidentals = major_keys.index(key) - 7
    else:
        accidentals = minor_keys.index(key) - 7
    return accidentals


def get_key_signature_accidentals(key='C'):
    """Return the list of accidentals present into the key signature."""
    accidentals = get_key_signature(key)
    res = []

    if accidentals < 0:
        for i in range(-accidentals):
            res.append('{0}{1}'.format(notes.fifths[-i-1], 'b'))
    elif accidentals > 0:
        for i in range(accidentals):
            res.append('{0}{1}'.format(notes.fifths[i], '#'))
    return res


def get_notes(key='C'):  # Todo: What if harmonic minor/melodic minor???
    """Return an ordered list of the notes in this natural key.

    Examples:
    >>> get_notes('F')
    ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']
    >>> get_notes('c')
    ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb']
    """
    # Check if result already existed in cache
    if key in _key_cache:
        return _key_cache[key]
    assert_valid_key(key)
    result = []

    # Use dict to record altered notes,
    # e.g. altered_notes_dict['C'] = 'C#' for key="E"
    altered_notes_dict = {nt[0]: nt for nt in get_key_signature_accidentals(key)}

    # Get the tonic note index
    tonic_index = base_scale.index(key.upper()[0])

    # Rearrange the base scale to begin with tonic
    base_scale_start_on_tonic = islice(cycle(base_scale), tonic_index, tonic_index+7)

    # Correct the scale for accidentals
    for note in base_scale_start_on_tonic:
        if note in altered_notes_dict:
            result.append(altered_notes_dict[note])
        else:
            result.append(note)

    # Save result to cache
    _key_cache[key] = result
    return result


def relative_major(key):
    """Return the relative major of a minor key.

    Example:
    >>> relative_major('a')
    'C'
    """
    try:
        return major_keys[minor_keys.index(key)]
    except ValueError:
        raise NoteFormatError("'%s' is not a minor key" % key)


def relative_minor(key):
    """Return the relative minor of a major key.

    Example:
    >>> relative_minor('C')
    'a'
    """
    try:
        return minor_keys[major_keys.index(key)]
    except ValueError:
        raise NoteFormatError("'%s' is not a major key" % key)


class Key(object):
    """A key object."""
    def __init__(self, key='C'):
        assert_valid_key(key)

        self.key = key
        self.mode = 'minor' if self.key[0].islower() else 'major'
        self.signature = get_key_signature(self.key)

        symbol = self.key[1:]
        accidental_dict = {'': '', 'b': 'flat', '#': 'sharp'}
        accidental = accidental_dict[symbol]
        self.name = '{0} {1} {2}'.format(self.key[0].upper(), accidental, self.mode)

    def __eq__(self, other):
        if self.key == other.key:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

