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

from image import Image, Images
from tag import SingleImageTagDialog
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
		self.set_default_size(400, 400)
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
		view.connect("key-press-event", self._key_pressed)
		view.set_headers_visible(True)
		view.set_enable_search(False)
		#The tag dialog is not ready for this:
		#view.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
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

	def _key_pressed(self,widget, event):
		selection = widget.get_selection()
		model, paths = selection.get_selected_rows()
		#t like tags
		if event.keyval == 116:
			if len(paths) == 1:
				SingleImageTagDialog(paths,self.store)

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
			tags = ", ".join(img.tags)
			filename = img.get_filename()
			self.store.append((filename, img.size, img.date, tags))


	def _filter_cleared(self, button):
		self.entry.set_text("")
		self.store.clear()
		self.add_images(images)


win = MainWindow()
images = Images()
win.add_images(images)
win.show_all()

gtk.main()


