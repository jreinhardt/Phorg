#!/usr/bin/env python

import os
import tracker
import urllib2


def _escape(str):
	return str.replace('"', '\\"').replace("'", "\\'")

class Image:

	def __init__(self, url):
		self.url = url
		self.tags = ""
		self.size = 0
		self.filename = ""


	def get_tags(self):
		query = """
SELECT ?labels WHERE {
	?f nie:url '%s'.
	?f nao:hasTag ?tags.
	?tags a nao:Tag;
		nao:prefLabel ?labels.
}
		""" % _escape(self.url)
		dbarray = tracker.query(query)
		return [x[0] for x in dbarray]


	def get_date(self):
		query = """
SELECT ?date
WHERE {
	?f nie:url '%s' .
	?f nie:contentCreated ?date .
}
		""" % _escape(self.url)

		dbarray = tracker.query(query)
		return str(dbarray[0][0])

	def get_filename(self):
		return urllib2.unquote(self.url)[7:]

	def get_size(self):
		query = """
SELECT ?size WHERE {
	?x nie:url '%s';
		nfo:fileSize ?size.
}
		""" % _escape(self.url)
		dbarray = tracker.query(query)
		return int(dbarray[0][0])
