import pygtk
pygtk.require("2.0")
import gtk
import sys
import os
import EXIF

win = gtk.Window()

entry = gtk.Entry()

files = gtk.ListStore(str,int,str)

dircontent = map(lambda x: os.path.join(os.getcwd(),"pics",x),os.listdir("pics"))

for f in dircontent:
	fid = open(f)
	tags = EXIF.process_file(fid)
	files.append((os.path.split(f)[1],os.stat(f).st_size,tags["EXIF DateTimeOriginal"]))

renderer = gtk.CellRendererText()

view = gtk.TreeView(files)
view.set_headers_visible(True)
view.append_column(gtk.TreeViewColumn("Filename",renderer,text=0))
view.append_column(gtk.TreeViewColumn("Filesize",renderer,text=1))
view.append_column(gtk.TreeViewColumn("Date",renderer,text=2))

box = gtk.VBox()

box.add(entry)
box.add(view)

win.add(box)

win.show_all()

	

gtk.main()


