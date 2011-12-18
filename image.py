#!/usr/bin/env python

import os
import urllib2

import gobject

import tracker


def _escape(str):
	return str.replace('"', '\\"').replace("'", "\\'")

class Image:

	def __init__(self, url, tags=None, date=None, size=None):
		self.url = url
		self.size = size
		self.date = date

		if tags is not None:
			self.tags = tags
		else:
			self.tags = []


	def get_filename(self):
		return urllib2.unquote(self.url)[7:]



# The 'Images' class should ideally behave like a list, but we also need to
# subclass GObject because we want to use custom signals. However, multiple
# inheritance in that case is not possible ("multiple bases have instance
# lay-out conflict"). Hence we implement the necessary portions of the list
# interface manually.

class Images(gobject.GObject):

	def __init__(self):
		gobject.GObject.__init__(self)

		self._images = []
		query = """
SELECT
	?url
	tracker:coalesce(?date1, ?date2, ?date3, '')
	?size
	(
		SELECT GROUP_CONCAT(nao:prefLabel(?tag), ' ')
		WHERE {
			?img nao:hasTag ?tag.
		}
	)
WHERE {
	?img a nfo:Image;
		nie:url ?url;
		nfo:fileSize ?size.

	OPTIONAL { ?img nie:contentCreated ?date1 }
	OPTIONAL { ?img nie:created ?date2 }
	OPTIONAL { ?img nfo:fileLastModified ?date3 }
}
		"""
		for r in tracker.query(query):
			url = str(r[0])
			date = str(r[1])
			size = int(r[2])
			tags = str(r[3]).split(' ')
			self._images.append(Image(url, tags=tags, date=date, size=size))


	def __getitem__(self, index):
		return self._images[index]


	def __len__(self):
		return len(self._images)


	def __iter__(self):
		return iter(self._images)
