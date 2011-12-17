#!/usr/bin/env python

import tracker

def get_tags(filename):
	"""
	Get a list of all tags of a file.
	"""

	query = """
SELECT ?tags ?labels
WHERE {
	?f nie:isStoredAs ?as ; nao:hasTag ?tags .
	?as nie:url 'file://%s' .
	?tags a nao:Tag ; nao:prefLabel ?labels .
}
	""" % filename

	dbarray = tracker.query(query)
	return [x[1] for x in dbarray]
