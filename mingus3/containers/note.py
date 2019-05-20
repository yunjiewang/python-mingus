#!/usr/bin/python
# -*- coding: utf-8 -*-

#    mingus - Music theory Python package, note module.
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

from mingus3.core import notes, intervals
from .mt_exceptions import NoteFormatError
from math import log
import re

class Note(object):

    """A note object.

    In the mingus.core module, notes are generally represented by strings.
    Most of the times, this is not enough. We want to set the octave and
    maybe the amplitude, vibrato or other dynamics. Then we want to store
    the notes in bars, the bars in tracks, the tracks in compositions, etc.

    We could do this with a number of lists, but ultimately it is a lot
    easier to use objects. The Note class provides an easy way to deal with
    notes in an object oriented matter.

    You can use the class NoteContainer to group Notes together in intervals
    and chords.
    """

    name = 'C'
    octave = 4
    dynamics = {}
    channel = 1
    velocity = 64

    def __init__(self, name='C', octave=4, dynamics={}):
        if type(name) is str:
            self.set_note(name, octave, dynamics)
        elif hasattr(name, 'name'):
            # Hardcopy Note object
            self.set_note(name.name, name.octave, name.dynamics)
            if hasattr(name, 'channel'):
                self.channel = name.channel
            if hasattr(name, 'velocity'):
                self.velocity = name.velocity
        elif type(name) is int:
            self.from_int(name)
        else:
            raise NoteFormatError("Don't know what to do with name object: "
                    "'%s'" % name)

    def set_channel(self, channel):
        self.channel = channel
        
    def set_velocity(self, velocity):
        self.velocity = velocity
    
    def set_note(self, name='C', octave=4, dynamics={}):
        """Set the note to name in octave with dynamics.

        Return the objects if it succeeded, raise an NoteFormatError
        otherwise.
        """
        dash_index = name.split('-')
        if len(dash_index) == 1:
            if notes.is_valid_note(name):
                self.name = name
                self.octave = octave
                self.dynamics = dynamics
                return self
            else:
                raise NoteFormatError("The string '%s' is not a valid "
                        "representation of a note in mingus" % name)
        elif len(dash_index) == 2:
            if notes.is_valid_note(dash_index[0]):
                self.name = dash_index[0]
                self.octave = int(dash_index[1])
                self.dynamics = dynamics
                return self
            else:
                raise NoteFormatError("The string '%s' is not a valid "
                        "representation of a note in mingus" % name)
        return False

    def empty(self):
        """Remove the data in the instance."""
        self.name = ''
        octave = 0
        dynamics = {}

    def augment(self):
        """Call notes.augment with this note as argument."""
        self.name = notes.augment(self.name)

    def diminish(self):
        """Call notes.diminish with this note as argument."""
        self.name = notes.diminish(self.name)

    def change_octave(self, diff):
        """Change the octave of the note to the current octave + diff."""
        self.octave += diff
        if self.octave < -1:
            print('[!] Warning: octave less than -1')

    def octave_up(self):
        """Increment the current octave with 1."""
        self.change_octave(1)

    def octave_down(self):
        """Decrement the current octave with 1."""
        self.change_octave(-1)

    def remove_redundant_accidentals(self):
        """Call notes.remove_redundant_accidentals on this note's name."""
        self.name = notes.remove_redundant_accidentals(self.name)

    def transpose(self, interval, up=True):
        """Transpose the note up or down the interval.

        Examples:
        >>> a = Note('A')
        >>> a.transpose('3')
        >>> a
        'C#-5'
        >>> a.transpose('3', False)
        >>> a
        'A-4'
        """
        # Calculate the new self.name and self.octave
        old_name, old_octave = self.name, self.octave
        self.name = intervals.from_shorthand(self.name, interval, up)
        if up:
            if Note(self.name[0]) < Note(old_name[0]):
                self.octave += 1
        else:
            if Note(self.name[0]) > Note(old_name[0]):
                self.octave -= 1

        # Correct for interval larger than one octave
        _acc, _deg, add_octave = intervals.parse_shorthand(interval)
        self.octave += add_octave

    def from_int(self, integer):
        """Set the Note corresponding to the integer.

        0 is a C on octave 0, 12 is a C on octave 1, etc.

        Example:
        >>> Note().from_int(12)
        'C-1'
        """
        self.name = notes.int_to_note(integer % 12)
        self.octave = integer // 12
        return self

    def measure(self, other):
        """Return the number of semitones between this Note and the other.

        Examples:
        >>> Note('C').measure(Note('D'))
        2
        >>> Note('D').measure(Note('C'))
        -2
        """
        return int(other) - int(self)

    def to_hertz(self, standard_pitch=440):
        """Return the Note in Hz.

        The standard_pitch argument can be used to set the pitch of A-4,
        from which the rest is calculated.
        """
        # int(Note("A", 4)) == 57
        diff = self.__int__() - 57
        return 2 ** (diff / 12.0) * standard_pitch

    def from_hertz(self, hertz, standard_pitch=440):
        """Set the Note name and pitch, calculated from the hertz value.

        The standard_pitch argument can be used to set the pitch of A-4,
        from which the rest is calculated.
        """
        log2 = lambda x: log(x, 2)
        value = log2(hertz/standard_pitch) * 12 + 57
        self.name = notes.int_to_note(round(value) % 12)
        self.octave = value // 12
        return self

    def to_shorthand(self):
        """Give the traditional Helmhotz pitch notation.

        Examples:
        >>> Note('C-4').to_shorthand()
        "c'"
        >>> Note('C-3').to_shorthand()
        'c'
        >>> Note('C-2').to_shorthand()
        'C'
        >>> Note('C-1').to_shorthand()
        'C,'
        """
        res = self.name
        if self.octave >= 3:
            res = res.lower()
        o = self.octave - 3
        while o < -1:
            res += ','
            o += 1
        while o > 0:
            res += "'"
            o -= 1
        return res

    def from_shorthand(self, shorthand):
        """Convert from traditional Helmhotz pitch notation.

        Examples:
        >>> Note().from_shorthand("C,,")
        'C-0'
        >>> Note().from_shorthand("C")
        'C-2'
        >>> Note().from_shorthand("c'")
        'C-4'
        """
        name = ''
        octave = 0
        for x in shorthand:
            if x in ['a', 'b', 'c', 'd', 'e', 'f', 'g']:
                name = str.upper(x)
                octave = 3
            elif x in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                name = x
                octave = 2
            elif x in ['#', 'b']:
                name += x
            elif x == ',':
                octave -= 1
            elif x == "'":
                octave += 1
        return self.set_note(name, octave, {})

    def __int__(self):
        """Return the current octave multiplied by twelve and add
        notes.note_to_int to it.
        
        This means a C-0 returns 0, C-1 returns 12, etc. This method allows
        you to use int() on Notes.
        """
        res = self.octave * 12 + notes.note_to_int(self.name[0])
        for n in self.name[1:]:
            if n == '#':
                res += 1
            elif n == 'b':
                res -= 1
        return res

    def __lt__(self, other):
        """Enable the comparing operators on Notes (>, <, \ ==, !=, >= and <=).

        So we can sort() Intervals, etc.

        Examples:
        >>> Note('C', 4) < Note('B', 4)
        True
        >>> Note('C', 4) > Note('B', 4)
        False
        """
        if other is None:
            return False
        return int(self) < int(other)

    def __eq__(self, other):
        """Compare Notes for equality by comparing their note values."""
        if other is None:
            return False
        return int(self) == int(other)

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return not(self < other or self == other)

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return not self < other

    def __repr__(self):
        """Return a helpful representation for printing Note classes."""
        return "'%s-%d'" % (self.name, self.octave)

