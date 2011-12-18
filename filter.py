#!/usr/bin/env python

"""
Module for filtering lists of images.
"""

class Term:
	"""
	A single term of a query.
	"""


	def __init__(self, getter, operator, value):
		"""
		getter: Function which maps an image to the value which is to be compared.
		operator: Operator of the term.
		value: Value which is to be compared with the image's value.
		"""
		self.getter = getter
		self.operator = operator
		self.value = value

	def matches(self, img):
		"""
		Check if an image matches this term.
		"""
		return False


class NumericalTerm(Term):
	"""
	A term which compares numerical values.
	"""

	def __init__(self, getter, operator, value):
		Term.__init__(self, getter, operator, value)
		self.value = float(value)
		if not operator in ['<', '<=', '>', '>=', '=', '==', '!=']:
			raise ValueError("Unknown operator '%s'." % operator)

	def matches(self, img):
		op = self.operator
		v1 = self.getter(img)
		v2 = self.value
		if op == '<':
			return v1 < v2
		elif op == '<=':
			return v1 <= v2
		elif op == '>':
			return v1 > v2
		elif op == '>=':
			return v1 >= v2
		elif op == '=' or op =='==':
			return v1 == v2
		elif op == '!=':
			return v1 != v2


class StringTerm(Term):
	"""
	A term which compares two strings.
	"""

	def __init__(self, getter, operator, value):
		Term.__init__(self, getter, operator, value)
		if not operator in ['==', '=', '#', '!=', '!#']:
			raise ValueError("Unknown operator '%s'." % operator)

	def matches(self, img):
		op = self.operator
		v1 = self.value
		v2 = self.getter(img)
		if op == '==' or op == '=':
			return v1 == v2
		elif op == '#':
			return v1 in v2
		elif op == '!=':
			return v1 != v2
		elif op == '!#':
			return v1 not in v2


class Query:
	"""
	A query.

	Queries are basically sets of terms. An image matches a query if it matches
	all the terms in the query.
	"""

	def __init__(self, string):
		"""
		string: Query string.
		"""
		self.string = string
		self.terms = []
		self._parse()


	def filter(self, imgs):
		"""
		Filter a list of images and return those which match the query.
		"""
		return [img for img in imgs if self.matches(img)]

	def _parse(self):
		"""
		Parse string query into internal abstract representation.
		"""
		tokens = self.string.split()
		tokens = [t.strip() for t in tokens if len(t.strip()) > 0]
		tokens.reverse()

		while len(tokens) > 0:
			var = tokens.pop().lower()
			if len(tokens) < 2:
				raise ValueError("Incomplete query: Expected two more tokens after '%s'." % var)
			if var == 'size':
				self.terms.append(NumericalTerm(lambda img: img.size, tokens.pop(), tokens.pop()))
			elif var == 'filename':
				self.terms.append(StringTerm(lambda img: img.get_filename(), tokens.pop(), tokens.pop()))
			elif var == 'tags':
				self.terms.append(StringTerm(lambda img: ' '.join(img.tags), tokens.pop(), tokens.pop()))
			else:
				raise ValueError("Unknown variable name '%s'." % var)


	def matches(self, img):
		"""
		Check if an image matches this query.
		"""
		for t in self.terms:
			if not t.matches(img):
				return False
		return True
