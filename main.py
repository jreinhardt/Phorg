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

class FilterEntry(gtk.Entry):
	"""
	Entry bar for entering filter queries.
	"""

	def __init__(self):
		gtk.Entry.__init__(self)
		# 'activate' is triggered when user presses ENTER
		self.connect("activate", self.on_activate)


	def on_activate(self, widget):
		print "ACTIVATE:", self.get_text()


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
		entry = FilterEntry()
		box.add(entry)

		# Create view
		self.store = gtk.ListStore(str,int,str)
		view = gtk.TreeView(self.store)
		view.set_headers_visible(True)
		renderer = gtk.CellRendererText()
		view.append_column(gtk.TreeViewColumn("Filename",renderer,text=0))
		view.append_column(gtk.TreeViewColumn("Filesize",renderer,text=1))
		view.append_column(gtk.TreeViewColumn("Date",renderer,text=2))
		box.add(view)

		self.add(box)




win = MainWindow()

dircontent = map(lambda x: os.path.join(os.getcwd(),"pics",x),os.listdir("pics"))

for f in dircontent:
	fid = open(f)
	tags = EXIF.process_file(fid)
	win.store.append((os.path.split(f)[1],os.stat(f).st_size,tags["EXIF DateTimeOriginal"]))

win.show_all()

gtk.main()


