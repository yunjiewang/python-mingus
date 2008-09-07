import sys
sys.path += ["../"]

import mingus.containers.Note as Note
import unittest
from mingus.containers.mt_exceptions import NoteFormatError

class test_Note(unittest.TestCase):
	
	def setUp(self):
		self.c = Note("C", 5)
		self.c1 = Note("C")
		self.c2 = Note("C", 3)

		self.b4 = Note("B", 4)
		self.b5 = Note("B", 5)

	def test_cmp(self):
		self.assert_(self.c1 <= self.b5)

		self.assert_(self.c < self.b5)
		self.assert_(self.c1 < self.b5)
		self.assert_(self.c2 < self.b5)

		self.assert_(self.c > self.b4, "%s %s" % (self.c, self.b4))
		self.assert_(self.c1 < self.b4)
		self.assert_(self.c2 < self.b4)

		self.assert_(self.b4 < self.b5)
		self.assert_(Note("C") > Note("Cb"))

	def test_to_int(self):
		self.assertEqual(48, Note("C", 4))
		self.assertEqual(47, Note("Cb", 4))
		self.assertEqual(36, int(self.c2))
		self.assertEqual(71, int(self.b5))
		self.assertEqual(59, int(self.b4))

	def test_set_note(self):
		n = Note()
		self.assert_(n.set_note("C", 5, {}))
		n.empty()
		self.assert_(n.set_note("C-5"))
		self.assert_(n.set_note("C", 5))
		self.assert_(n.set_note("C#-12", 5))

		self.assertRaises(NoteFormatError, n.set_note,"H")
		self.assertRaises(NoteFormatError, n.set_note,"C 23")
		self.assertRaises(NoteFormatError, n.set_note,"C# 123")

	def test_to_hertz(self):
		self.assertEqual(Note("A", 0).to_hertz(), 27.5)
		self.assertEqual(Note("A", 1).to_hertz(), 55)
		self.assertEqual(Note("A", 2).to_hertz(), 110)
		self.assertEqual(Note("A", 3).to_hertz(), 220)
		self.assertEqual(Note("A", 4).to_hertz(), 440)
		self.assertEqual(Note("A", 5).to_hertz(), 880)
		self.assertEqual(Note("A", 6).to_hertz(), 1760)

	def test_from_hertz(self):
		a = Note()
		a.from_hertz(440)
		self.assertEqual(a, Note("A", 4))
		a.from_hertz(880)
		self.assertEqual(a, Note("A", 5))
		a.from_hertz(1760)
		self.assertEqual(a, Note("A", 6))

	def test_transpose(self):
		a = Note("C")
		a.transpose("3")
		self.assertEqual(Note("E"), a)
		a.transpose("b2")
		self.assertEqual(Note("F"), a)
		a.transpose("5")
		self.assertEqual(Note("C", 5), a)
		a.transpose("5", False)
		self.assertEqual(Note("F"), a)

def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test_Note)
	
