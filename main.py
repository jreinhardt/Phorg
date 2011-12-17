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


# Command to execute when a file is double-clicked in the list view. The
# filename of the selected image is given as an argument.
cmd = 'eog'


# Original list of all files. We need to store this so that we can select
# a subset of it via the filtering mechanism.
files = []


class MainWindow(gtk.Window):
	"""
	Main window of the application.
	"""

	def __init__(self):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
	
		self.store = None
		self._create_gui()


	def _create_gui(self):
		self.connect("destroy", lambda w: gtk.main_quit())

		box = gtk.VBox()

		# Create filter text box
		filterbar = gtk.HBox()
		entry = gtk.Entry()
		entry.connect("activate", self._entry_activate)
		filterbar.add(entry)
		button = gtk.Button(stock=gtk.STOCK_CLEAR)
		button.connect("clicked", self._filter_cleared)
		filterbar.add(button)
		box.pack_start(filterbar,expand=False,fill=False)

		# Create view
		self.store = gtk.ListStore(str,int,str,str)
		view = gtk.TreeView(self.store)
		view.connect("row-activated", self._view_row_activated)
		view.set_headers_visible(True)
		renderer = gtk.CellRendererText()
		view.append_column(gtk.TreeViewColumn("Filename",renderer,text=0))
		view.append_column(gtk.TreeViewColumn("Filesize",renderer,text=1))
		view.append_column(gtk.TreeViewColumn("Date",renderer,text=2))
		view.append_column(gtk.TreeViewColumn("Tags",renderer,text=3))
		box.pack_start(view)

		self.add(box)

	def _entry_activate(self, widget):
		from filter import filter
		query = widget.get_text()
		try:
			result = filter(files, query)
		except ValueError:
			# Invalid query
			return
		self.store.clear()
		for x in result:
			self.store.append(x)


	def _view_row_activated(self, view, path, column):
		import subprocess
		iter = self.store.get_iter(path)
		filename = self.store.get_value(iter, 0)
		subprocess.Popen([cmd, os.path.join(os.getcwd(), "pics", filename)])


	def _filter_cleared(self,button):
		for x in files:
			self.store.append(x)
		



win = MainWindow()

tags = Tags()
# Load all pictures from the "pics" directory
filenames = os.listdir("pics")
files = []
for fn in filenames:
	full = os.path.join(os.getcwd(), "pics", fn)
	t = ", ".join(tags.get_tags(full))
	with open(full) as fid:
		exif = EXIF.process_file(fid)
	files.append((fn, os.stat(full).st_size, exif["EXIF DateTimeOriginal"],t))

# Fill list store
for f in files:
	win.store.append(f)

win.show_all()

gtk.main()


