#!/usr/bin/env python

import os
import tracker
import urllib2

class Image:

	def __init__(self, url):
		self.url = url
		self.tags = ""
		self.size = 0
		self.filename = ""


	def get_tags(self):
		query = """
SELECT ?labels
WHERE {

	?f nie:url '%s' .
	?f nao:hasTag ?tags .
	?tags a nao:Tag ; nao:prefLabel ?labels .
}
		""" % self.url

		dbarray = tracker.query(query)
		return [x[0] for x in dbarray]


	def get_date(self):
		query = """
SELECT ?date
WHERE {
	?f nie:url '%s' .
	?f nie:contentCreated ?date .
}
		""" % self.url

		dbarray = tracker.query(query)
		return str(dbarray[0][0])

	def get_filename(self):
		return urllib2.unquote(self.url)[7:]
