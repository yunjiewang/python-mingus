#!/usr/bin/python
# -*- coding: utf-8 -*-

#    Music theory Python package, intervals module.
#    Copyright (C) 2008-2009, Bart Spaans
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

"""Module to create intervals from notes.

When you are working in a key (for instance 'F'), you can use the functions
second ('G'), third ('A'), fourth ('Bb'), fifth ('C'), sixth ('D') and
seventh ('E') to get to the respective natural intervals of that note.

When you want to get the absolute intervals you can use the minor and major
functions. For example: minor_third('F') returns 'Ab' while major_third('F')
returns 'A'.

This modules also contains other useful helper functions like measure,
determine, invert, is_consonant and is_dissonant.
"""

import re

from . import keys
from . import notes


def assert_valid_start_note(key, note):
    notes.assert_valid_note(note)
    if note not in keys.get_notes(key):
        raise KeyError(f"The start note '{note}' is not in the key {key}")


def interval(key, start_note, scale_degree_interval):
    """Return the note found at the interval starting from start_note in the
    given key.

    Raise a KeyError exception if start_note is not a valid note.

    Example:
    >>> interval('C', 'D', 1)
    'E'
    """
    assert_valid_start_note(key, start_note)
    notes_in_key = keys.get_notes(key)
    for n in notes_in_key:
        if n[0] == start_note[0]:  # Todo: use direct match instead of 1st letter
            index = notes_in_key.index(n)
    return notes_in_key[(index + scale_degree_interval) % 7]


def unison(note, key=None):
    """Return the unison of note.

    Raise a KeyError exception if the note is not found in the given key.

    The key is not at all important, but is here for consistency reasons
    only.

    Example:
    >>> unison('C')
    'C'
    """
    if key is None:
        key = note
    return interval(key, note, 0)


def second(note, key):
    """Take the diatonic second of note in key.

    Raise a KeyError exception if the note is not found in the given key.

    Examples:
    >>> second('E', 'C')
    'F'
    >>> second('E', 'D')
    'F#'
    """
    return interval(key, note, 1)


def third(note, key):
    """Take the diatonic third of note in key.

    Raise a KeyError exception if the note is not found in the given key.

    Examples:
    >>> third('E', 'C')
    'G'
    >>> third('E', 'E')
    'G#'
    """
    return interval(key, note, 2)


def fourth(note, key):
    """Take the diatonic fourth of note in key.

    Raise a KeyError exception if the note is not found in the given key.

    Examples:
    >>> fourth('E', 'C')
    'A'
    >>> fourth('E', 'B')
    'A#'
    """
    return interval(key, note, 3)


def fifth(note, key):
    """Take the diatonic fifth of note in key.

    Raise a KeyError exception if the note is not found in the given key.

    Examples:
    >>> fifth('E', 'C')
    'B'
    >>> fifth('E', 'F')
    'Bb'
    """
    return interval(key, note, 4)


def sixth(note, key):
    """Take the diatonic sixth of note in key.

    Raise a KeyError exception if the note is not found in the given key.

    Examples:
    >>> sixth('E', 'C')
    'C'
    >>> sixth('E', 'B')
    'C#'
    """
    return interval(key, note, 5)


def seventh(note, key):
    """Take the diatonic seventh of note in key.

    Raise a KeyError exception if the note is not found in the given key.

    Examples:
    >>> seventh('E', 'C')
    'D'
    >>> seventh('E', 'B')
    'D#'
    """
    return interval(key, note, 6)


def minor_unison(note):
    return diminished_unison(note)


def major_unison(note):
    return perfect_unison(note)


def diminished_unison(note):
    return notes.diminish(note)


def perfect_unison(note):
    return note


def augmented_unison(note):
    return notes.augment(note)


def minor_second(note):
    return notes.diminish(major_second(note))


def major_second(note):
    sec = second(note[0], 'C')
    return augment_or_diminish_until_the_interval_is_right(note, sec, 2)


def minor_third(note):
    return notes.diminish(major_third(note))


def major_third(note):
    trd = third(note[0], 'C')
    return augment_or_diminish_until_the_interval_is_right(note, trd, 4)


def minor_fourth(note):
    return diminished_fourth(note)


def major_fourth(note):
    return perfect_fourth(note)


def perfect_fourth(note):
    frt = fourth(note[0], 'C')
    return augment_or_diminish_until_the_interval_is_right(note, frt, 5)


def diminished_fourth(note):
    return notes.diminish(perfect_fourth(note))


def augmented_fourth(note):
    return notes.augment(perfect_fourth(note))


def minor_fifth(note):
    return diminished_fifth(note)


def major_fifth(note):
    return perfect_fifth(note)


def perfect_fifth(note):
    fif = fifth(note[0], 'C')
    return augment_or_diminish_until_the_interval_is_right(note, fif, 7)


def diminished_fifth(note):
    return notes.diminish(perfect_fifth(note))


def minor_sixth(note):
    return notes.diminish(major_sixth(note))


def major_sixth(note):
    sth = sixth(note[0], 'C')
    return augment_or_diminish_until_the_interval_is_right(note, sth, 9)


def minor_seventh(note):
    return notes.diminish(major_seventh(note))


def major_seventh(note):
    sth = seventh(note[0], 'C')
    return augment_or_diminish_until_the_interval_is_right(note, sth, 11)


def diminished_seventh(note):
    return notes.diminish(minor_seventh(note))


def get_interval(note, half_steps, key='C', up=True):  # Todo, up/down toggle?
    """Return the note an interval (in half notes) away from the given note.
    Positive half_steps means looking up, negative means down. The returned
    note either is a diatonic note, or is flattened from a diatonic note.

    This will produce mostly theoretical sound results, but you should use
    the minor and major functions to work around the corner cases.
    """
    notes.assert_valid_note(note)
    if not up:
        half_steps *= -1

    # Set up a diatonic note lookup table that map note_int to note name
    diatonic_notes = keys.get_notes(key)
    diatonic_note_lookup = {notes.note_to_int(dn): dn for dn in diatonic_notes}

    # Calculate note_ints
    starting_note_int = notes.note_to_int(note)
    target_note_int = (starting_note_int + half_steps) % 12

    # Lookup the target note
    try:
        res = diatonic_note_lookup[target_note_int]
    except KeyError:
        # If target note is chromatic, raise it a half step first.
        # Then find match. Finally, apply notes.diminished()
        res = notes.diminish(diatonic_note_lookup[(target_note_int + 1) % 12])
    return res


def measure(note1, note2):
    """Return an integer in the range of 0-11, determining the half note steps
    between note1 and note2.

    Examples:
    >>> measure('C', 'D')
    2
    >>> measure('D', 'C')
    10
    """
    res = (notes.note_to_int(note2) - notes.note_to_int(note1)) % 12
    return res


def augment_or_diminish_until_the_interval_is_right(note1, note2, half_step_interval):
    """A helper function for the minor and major functions.

    You should probably not use this directly.
    """
    cur = measure(note1, note2)
    while cur != half_step_interval:
        if cur > half_step_interval:
            note2 = notes.diminish(note2)
        elif cur < half_step_interval:
            note2 = notes.augment(note2)
        cur = measure(note1, note2)

    # We are practically done right now, but we need to be able to create the
    # minor seventh of Cb and get Bbb instead of B######### as the result
    accidentals = note2[1:]
    sharp_count = accidentals.count('#')
    flat_count = accidentals.count('b')
    if sharp_count > 6:
        flipped_symbol = (12 - sharp_count) * 'b'
        note2 = "".join([note2[0], flipped_symbol])
    elif flat_count > 6:
        flipped_symbol = (12 - flat_count) * '#'
        note2 = "".join([note2[0], flipped_symbol])
    return note2


def invert(note_seq):
    """Invert an interval.

    Example:
    >>> invert(['C', 'E'])
    ['E', 'C']
    """
    return note_seq[::-1]


def determine(note1, note2, shorthand=False, up=True):
    """Name the interval between note1 and note2.

    Examples:
    >>> determine('C', 'E')
    'major third'
    >>> determine('C', 'Eb')
    'minor third'
    >>> determine('C', 'E#')
    'augmented third'
    >>> determine('C', 'Ebb')
    'diminished third'

    This works for all intervals. Note that there are corner cases for major
    fifths and fourths:
    >>> determine('C', 'G')
    'perfect fifth'
    >>> determine('C', 'F')
    'perfect fourth'
    """
    # Check notes are valid
    notes.assert_valid_note(note1)
    notes.assert_valid_note(note2)

    # Store the properties of unaltered major scale intervals
    pre_alt_int_lookup = {
        1: ['unison', 'perfect', 0],  # [interval_type, harmony_quality, half_steps]
        2: ['second', 'imperfect', 2],
        3: ['third', 'imperfect', 4],
        4: ['fourth', 'perfect', 5],
        5: ['fifth', 'imperfect', 7],
        6: ['sixth', 'imperfect', 9],
        7: ['seventh', 'imperfect', 11],
    }

    # Store the interval quality modifier
    perfect_int_modifier = {-2: ['doubly diminished', 'bb'],
                            -1: ['diminished', 'b'],
                            0: ['perfect', ''],
                            1: ['augmented', '#'],
                            2: ['doubly augmented', '##'],
                            }

    imperfect_int_modifier = {-2: ['diminished', 'bb'],
                              -1: ['minor', 'b'],
                              0: ['major', ''],
                              1: ['augmented', '#'],
                              }

    # Calculate interval type and get its unaltered properties
    n1_int_pre_alt = keys.base_scale.index(note1[0])
    n2_int_pre_alt = keys.base_scale.index(note2[0])
    if up:
        distance_pre_alt = (n2_int_pre_alt - n1_int_pre_alt) % 7 + 1
    else:
        distance_pre_alt = (n1_int_pre_alt - n2_int_pre_alt) % 7 + 1
    int_type_name, hmy_qual, half_steps_pre_alt = pre_alt_int_lookup[distance_pre_alt]

    # Calculate half steps between two notes
    n1_int = notes.note_to_int(note1)
    n2_int = notes.note_to_int(note2)
    if up:
        half_steps = (n2_int - n1_int) % 12
    else:
        half_steps = (n1_int - n2_int) % 12

    # Determine interval quality modifier
    half_step_diff = (half_steps - half_steps_pre_alt)
    if half_step_diff < -6:  # minimize trailing accidentals
        half_step_diff += 12
    elif half_step_diff > 6:
        half_step_diff -= 12

    try:
        if hmy_qual == 'perfect':
            mod = perfect_int_modifier[half_step_diff]
        else:
            mod = imperfect_int_modifier[half_step_diff]
    except KeyError:
        raise KeyError('Remove impractical number of sharps and flats in the notes')

    if shorthand:
        res = "".join([mod[1], str(distance_pre_alt)])
    else:
        res = " ".join([mod[0], int_type_name])
    return res


def parse_shorthand(shorthand):
    r = re.compile('^([b#]*)([1-9]|1[0-5])$')
    try:
        accidentals, _degree = r.findall(shorthand)[0]
    except IndexError:
        raise ValueError('interval shorthand is not valid')
    degree = (int(_degree) - 1) % 7 + 1
    octave = (int(_degree) - 1) // 7
    return accidentals, degree, octave


def from_shorthand(note, interval, up=True):
    """Return the note on interval up or down.

    Examples:
    >>> from_shorthand('A', 'b3')
    'C'
    >>> from_shorthand('D', '2')
    'E'
    >>> from_shorthand('E', '2', False)
    'D'
    """
    # warning should be a valid note
    if not notes.is_valid_note(note):
        return False

    # Process the interval input
    accidentals, degree, _ = parse_shorthand(interval)

    # Shorthand lookup dict (1: up=True, 0: up=False)
    shorthand_lookup = {
        1: {1: major_unison, 0: major_unison},
        2: {1: major_second, 0: minor_seventh},
        3: {1: major_third, 0: minor_sixth},
        4: {1: major_fourth, 0: major_fifth},
        5: {1: major_fifth, 0: major_fourth},
        6: {1: major_sixth, 0: minor_third},
        7: {1: major_seventh, 0: minor_second},
    }

    # Look up last character in interval in shorthand_lookup and call that function
    try:
        interval_func = shorthand_lookup[degree][up]
    except KeyError:
        # warning Last character in interval should be 1-7
        return False
    res = interval_func(note)

    # Adjust for accidentals
    for x in accidentals:
        if (x == '#' and up) or (x == 'b' and not up):
            res = notes.augment(res)
        elif (x == 'b' and up) or (x == '#' and not up):
            res = notes.diminish(res)

    return res


def is_consonant(note1, note2, include_fourths=True):
    """Return True if the interval is consonant.

    A consonance is a harmony, chord, or interval considered stable, as
    opposed to a dissonance.

    This function tests whether the given interval is consonant. This
    basically means that it checks whether the interval is (or sounds like)
    a unison, third, sixth, perfect fourth or perfect fifth.

    In classical music the fourth is considered dissonant when used
    contrapuntal, which is why you can choose to exclude it.
    """
    return (is_perfect_consonant(note1, note2, include_fourths) or
            is_imperfect_consonant(note1, note2))


def is_perfect_consonant(note1, note2, include_fourths=True):
    """Return True if the interval is a perfect consonant one.

    Perfect consonances are either unisons, perfect fourths or fifths, or
    octaves (which is the same as a unison in this model).

    Perfect fourths are usually included as well, but are considered
    dissonant when used contrapuntal, which is why you can exclude them.
    """
    dhalf = measure(note1, note2)
    return dhalf in [0, 7] or (include_fourths and dhalf == 5)


def is_imperfect_consonant(note1, note2):
    """Return True id the interval is an imperfect consonant one.

    Imperfect consonances are either minor or major thirds or minor or major
    sixths.
    """
    return measure(note1, note2) in [3, 4, 8, 9]


def is_dissonant(note1, note2, include_fourths=False):
    """Return True if the insterval is dissonant.

    This function tests whether an interval is considered unstable,
    dissonant.

    In the default case perfect fourths are considered consonant, but this
    can be changed by setting exclude_fourths to True.
    """
    return not is_consonant(note1, note2, not include_fourths)
