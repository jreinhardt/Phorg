#!/usr/bin/env python

import os

class Image:

	def __init__(self, filename):
		self.filename = filename
		self.size = 0
		self.tags = []
		self.exif = {}
