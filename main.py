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
		self.store = gtk.ListStore(str,int)
		view = gtk.TreeView(self.store)
		view.set_headers_visible(True)
		renderer = gtk.CellRendererText()
		col1 = gtk.TreeViewColumn("Palim",renderer,text=0)
		col2 = gtk.TreeViewColumn("Ketchup",renderer,text=1)
		view.append_column(col1)
		view.append_column(col2)
		box.add(view)

		self.add(box)




win = MainWindow()

dircontent = os.listdir(os.getcwd())
for f in dircontent:
	win.store.append((f,os.stat(f).st_size))

win.show_all()

gtk.main()


