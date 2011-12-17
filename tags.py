#!/usr/bin/env python

import dbus
from dbus.mainloop.glib import DBusGMainLoop

# Initialize DBUS
DBusGMainLoop(set_as_default=True)
_bus = dbus.SessionBus()
_res_proxy = _bus.get_object(
	"org.freedesktop.Tracker1",
	"/org/freedesktop/Tracker1/Resources"
)
_res_interface = dbus.Interface(_res_proxy,"org.freedesktop.Tracker1.Resources")


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

	dbarray = _res_interface.SparqlQuery(query)
	return [x[1] for x in dbarray]
