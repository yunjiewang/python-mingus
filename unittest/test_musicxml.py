import sys
sys.path += ["../"]

import mingus3.extra.musicxml as mxl
import unittest

class test_MusicXML(unittest.TestCase):
	
	def setUp(self):
		pass



def suite():
	return unittest.TestLoader().loadTestsFromTestCase(test_MusicXML)

