#!/usr/bin/env python

# Baustellen:
# - Filterzeugs
# - Liste sinnvoll
# - Code-Struktur

import sys
import os

import pygtk
pygtk.require("2.0")
import gtk

from image import Image



# Command to execute when a file is double-clicked in the list view. The
# filename of the selected image is given as an argument.
cmd = 'eog'


# Original list of all images. We need to store this so that we can select
# a subset of it via the filtering mechanism.
images = []


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
		entry = gtk.Entry()
		entry.connect("activate", self._entry_activate)
		box.add(entry)

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
		box.add(view)

		self.add(box)

	def _entry_activate(self, widget):
		from filter import filter
		query = widget.get_text()
		try:
			result = filter(images, query)
		except ValueError:
			# Invalid query
			return
		self.store.clear()
		self.add_images(result)


	def _view_row_activated(self, view, path, column):
		import subprocess
		iter = self.store.get_iter(path)
		filename = self.store.get_value(iter, 0)
		subprocess.Popen([cmd, os.path.join(os.getcwd(), "pics", filename)])


	def add_images(self, lst):
		"""
		Add a list of images to the list store.
		"""
		for img in lst:
			t = ", ".join(img.tags)
			d = img.exif['EXIF DateTimeOriginal']
			self.store.append((img.filename, img.size, d, t))


win = MainWindow()

# Load all pictures from the "pics" directory
filenames = os.listdir("pics")
images = []
for fn in filenames:
	full = os.path.join(os.getcwd(), "pics", fn)
	images.append(Image(full))
win.add_images(images)

win.show_all()

gtk.main()


