#!/usr/bin/env python

# Baustellen:
# - Filterzeugs
# - Liste sinnvoll
# - Code-Struktur

import pygtk
pygtk.require("2.0")
import gtk
import sys
import os
import EXIF
import dbus
from dbus.mainloop.glib import DBusGMainLoop

class Tags:
	def __init__(self):
		DBusGMainLoop(set_as_default=True)
		self.bus = dbus.SessionBus()

		self.res_proxy = self.bus.get_object("org.freedesktop.Tracker1",
			"/org/freedesktop/Tracker1/Resources")
		self.res_interface = dbus.Interface(self.res_proxy,"org.freedesktop.Tracker1.Resources")

	def get_tags(self,path):
		dbarray = self.res_interface.SparqlQuery("""SELECT ?tags ?labels
			WHERE {
				?f nie:isStoredAs ?as ; nao:hasTag ?tags .
				?as nie:url 'file://%s' .
				?tags a nao:Tag ; nao:prefLabel ?labels .
			}""" % path)
		return [x[1] for x in dbarray]


class MainWindow(gtk.Window):
	"""
	Main window of the application.
	"""


	def __init__(self):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
	
		self.store = None
		self._create_gui()


	def _create_gui(self):
		box = gtk.VBox()

		# Create filter text box
		entry = gtk.Entry()
		box.add(entry)

		# Create view
		self.store = gtk.ListStore(str,int,str,str)
		view = gtk.TreeView(self.store)
		view.set_headers_visible(True)
		renderer = gtk.CellRendererText()
		view.append_column(gtk.TreeViewColumn("Filename",renderer,text=0))
		view.append_column(gtk.TreeViewColumn("Filesize",renderer,text=1))
		view.append_column(gtk.TreeViewColumn("Date",renderer,text=2))
		view.append_column(gtk.TreeViewColumn("Tags",renderer,text=3))
		box.add(view)

		self.add(box)



win = MainWindow()

dircontent = map(lambda x: os.path.join(os.getcwd(),"pics",x),os.listdir("pics"))

tags = Tags()

for f in dircontent:
	fid = open(f)
	exif = EXIF.process_file(fid)
	t = ", ".join(tags.get_tags(f))
	win.store.append((os.path.split(f)[1],os.stat(f).st_size,exif["EXIF DateTimeOriginal"],t))

win.show_all()

gtk.main()


