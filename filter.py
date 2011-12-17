#!/usr/bin/env python

"""
Module for filtering lists.
"""


def filter(lst, string):
	"""
	Filter a list of files using a filter string.

	Returns the filtered list.
	"""

	max_size = int(string)

	# We now simply assume that each list item is a tuple and that its size
	# is given in its second field.
	return [x for x in lst if x.size <= max_size]

