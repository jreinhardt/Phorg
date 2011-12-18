#!/usr/bin/env python

# Baustellen:
# - Filterzeugs
# - Liste sinnvoll
# - Code-Struktur

import sys
import os
import urllib2

import pygtk
pygtk.require("2.0")
import gtk

from image import Image
import tracker



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
		filterbar = gtk.HBox()
		self.entry = gtk.Entry()
		self.entry.connect("activate", self._entry_activate)
		filterbar.add(self.entry)
		button = gtk.Button(stock=gtk.STOCK_CLEAR)
		button.connect("clicked", self._filter_cleared)
		filterbar.add(button)
		box.pack_start(filterbar, expand=False, fill=False)

		# Create view
		self.store = gtk.ListStore(str, int, str, str)
		view = gtk.TreeView(self.store)
		view.connect("row-activated", self._view_row_activated)
		view.set_headers_visible(True)
		renderer = gtk.CellRendererText()
		column_titles = ["Filename", "Filesize", "Date","Tags"]
		for title,idx in zip(column_titles,range(len(column_titles))):
			col = gtk.TreeViewColumn(title,renderer,text=idx)
			col.set_resizable(True)
			col.set_sort_column_id(idx)
			view.append_column(col)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		scroll.add(view)
		box.pack_start(scroll)

		self.add(box)

	def _entry_activate(self, widget):
		from filter import Query
		query = Query(widget.get_text())
		try:
			result = query.filter(images)
		except ValueError:
			# Invalid query
			return
		self.store.clear()
		self.add_images(result)


	def _view_row_activated(self, view, path, column):
		import subprocess
		iter = self.store.get_iter(path)
		filename = self.store.get_value(iter, 0)
		subprocess.Popen([cmd, filename])


	def add_images(self, lst):
		"""
		Add a list of images to the list store.
		"""
		for img in lst:
			tags = " ".join(img.get_tags())
			date = img.get_date()
			filename = img.get_filename()
			
			self.store.append((filename, 1, date, tags))


	def _filter_cleared(self, button):
		self.entry.set_text("")
		self.store.clear()
		self.add_images(images)


def find_images(path):
	"""
	Recursively find all images in a given directory.

	Returns a list of the filenames of the images.
	"""
	images = []
	for dirpath, dirnames, filenames in os.walk(path):
		for fn in filenames:
			if os.path.splitext(fn)[1].lower() in ['.jpg', '.jpeg', '.png', '.gif']:
				images.append(os.path.join(dirpath, fn))
	return images


def get_images_from_tracker():
	query = """
SELECT ?url WHERE {
	?x a nfo:Image.
	?x nie:url ?url.
}
	"""
	result = tracker.query(query)
	return [str(x[0]) for x in result]


win = MainWindow()

# Load all pictures from the "pics" directory
print "Looking for images..."
#filenames = find_images(os.getcwd())
filenames = get_images_from_tracker()
print "Found %d images." % len(filenames)
images = []
print "Loading image information..."
for fn in filenames:
	images.append(Image(fn))
print "Done loading image information."

win.add_images(images)


win.show_all()

gtk.main()


