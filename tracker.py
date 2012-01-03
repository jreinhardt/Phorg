#!/usr/bin/env python

import dbus
from dbus.mainloop.glib import DBusGMainLoop

# Initialize DBUS
DBusGMainLoop(set_as_default=True)
_bus = dbus.SessionBus()
_proxy = _bus.get_object(
	"org.freedesktop.Tracker1",
	"/org/freedesktop/Tracker1/Resources"
)
_interface = dbus.Interface(_proxy, "org.freedesktop.Tracker1.Resources")


def query(string):
	return _interface.SparqlQuery(string)


def register_update_listener(listener):
	# Note: It seems the GraphUpdated signal is only sent by Tracker >= 0.9.x
	_proxy.connect_to_signal('GraphUpdated', listener)


def update(string):
	_interface.SparqlUpdate(string)
