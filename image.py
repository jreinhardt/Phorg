#!/usr/bin/env python

import os

import EXIF
from tags import get_tags

class Image:

	def __init__(self, filename):
		self.filename = filename
		self.tags = get_tags(filename)
		with open(filename) as fid:
			self.exif = EXIF.process_file(fid)
		self.size = os.stat(filename).st_size
