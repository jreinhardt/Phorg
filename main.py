import pygtk
pygtk.require("2.0")
import gtk

win = gtk.Window()

entry = gtk.Entry()

view = gtk.TreeView()

box = gtk.VBox()

box.add(entry)
box.add(view)

win.add(box)

win.show_all()
gtk.main()


