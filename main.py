import pygtk
pygtk.require("2.0")
import gtk
import sys
import os

win = gtk.Window()

entry = gtk.Entry()

files = gtk.ListStore(str,int)

dircontent = os.listdir(os.getcwd())

for f in dircontent:
	files.append((f,os.stat(f).st_size))

renderer = gtk.CellRendererText()

view = gtk.TreeView(files)
view.set_headers_visible(True)
col1 = gtk.TreeViewColumn("Eimer",renderer,text=0)
col2 = gtk.TreeViewColumn("Reimer",renderer,text=1)
view.append_column(col1)
view.append_column(col2)

box = gtk.VBox()

box.add(entry)
box.add(view)

win.add(box)

win.show_all()

	

gtk.main()


