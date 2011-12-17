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


def query(string):
	return _res_interface.SparqlQuery(string)
