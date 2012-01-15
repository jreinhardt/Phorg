import gtk
import tracker

queries = {}

queries["all tags and counts"] = """SELECT ?tag ?label COUNT(?im) WHERE {
	?im a nfo:Image;
		nao:hasTag ?tag;
		nie:isStoredAs ?file .
	?tag a nao:Tag;
		nao:prefLabel ?label .
} GROUP BY ?label"""

queries["tags for file"] = """SELECT ?label WHERE {
	?im a nfo:Image;
		nao:hasTag ?tag;
		nie:isStoredAs ?file .
	?tag a nao:Tag;
		nao:prefLabel ?label .
	?file nie:url 'file://%s' .
}"""

queries["add existing tag"] = """INSERT {
	?im nao:hasTag ?tag
} WHERE {
	?im a nfo:Image;
		nie:isStoredAs ?file .
	?tag a nao:Tag;
		nao:prefLabel '%s' .
	?file nie:url 'file://%s' .
}"""

queries["add nonexisting tag"] = """INSERT {
	_:tag a nao:Tag ;
		nao:prefLabel '%s' .
	?im nao:hasTag _:tag
} WHERE {
	?im a nfo:Image;
		nie:isStoredAs ?file .
	?file nie:url 'file://%s' .
}"""

queries["remove tag from file"] = """DELETE {
	?im nao:hasTag ?tag
} WHERE {
	?tag a nao:Tag ;
		nao:prefLabel '%s' .
	?im a nfo:Image;
		nao:hasTag ?tag;
		nie:isStoredAs ?file .
	?file nie:url 'file://%s' .
}"""

class ImageTagDialog(gtk.Dialog):
	"""
	Dialog for adding and removing tags to and from a single photo
	"""

	def __init__(self,paths,store):
		gtk.Dialog.__init__(self, "Tags",
			None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

		self.store = store

		self.removing = []

		result = tracker.query(queries["all tags and counts"])
		all_tags = [(str(x[1]), int(x[2])) for x in result]
		all_tags = sorted(all_tags,cmp=lambda x,y: cmp(x[1],y[1]))

		entry = gtk.Entry()
		completion = gtk.EntryCompletion()
		entry.set_completion(completion)
		comp_store = gtk.ListStore(str)
		completion.set_model(comp_store)
		completion.set_text_column(0)
		completion.set_inline_selection(True)
		for tag,freq in all_tags:
			comp_store.append([tag])
		self.vbox.pack_start(entry)
		entry.show()

		if(len(paths) == 1):
			iter =  self.store.get_iter(paths[0])
			filename = self.store.get_value(iter,0)
			result = tracker.query(queries["tags for file"] % filename)
			file_tags = [str(x[0]) for x in result]

			for tag in file_tags:
				button = gtk.Button(label="Remove tag %s" % tag)
				button.connect("clicked",lambda b, t=tag: self._remove_tag(b,t))
				self.vbox.pack_start(button)
				button.show()

		response = self.run()

		if response == gtk.RESPONSE_ACCEPT:
			if len(paths) > 1:
				assert(not bool(self.removing))
			for tag in self.removing:
				tracker.update(queries["remove tag from file"] % (tag, filename))

			new_tags = [x.strip() for x in entry.get_text().split(",")]
			for path in paths:
				iter =  self.store.get_iter(path)
				filename = self.store.get_value(iter,0)
				result = tracker.query(queries["tags for file"] % filename)
				file_tags = [str(x[0]) for x in result]

				for tag in new_tags:
					if tag in file_tags:
						continue
					if tag in all_tags:
						tracker.update(queries["add existing tag"] % (filename,tag))
					else:
						tracker.update(queries["add nonexisting tag"] % (tag, filename))

				result = tracker.query(queries["tags for file"] % filename)
				file_tags = [str(x[0]) for x in result]
				self.store.set(iter, 3, ", ".join(file_tags))
		self.destroy()

	def _remove_tag(self,button,label):
		self.removing.append(label)
		button.hide()

class TagsDialog(gtk.Dialog):
	"""
	Dialog for managing all existing tags
	"""

	def __init__(self):
		gtk.Dialog.__init__(self, "Tags",
			None,
			gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
			(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

		self.removing = []

		result = tracker.query(queries["all tags and counts"])
		all_tags = [(str(x[1]), int(x[2])) for x in result]
		all_tags = sorted(all_tags,cmp=lambda x,y: cmp(x[1],y[1]))

		self.store = gtk.ListStore(str,int)
		view = gtk.TreeView(self.store)
		view.set_headers_visible(True)
		renderer = gtk.CellRendererText()
		column_titles = ["Tag", "Nr. of Files"]
		for title,idx in zip(column_titles,range(len(column_titles))):
			col = gtk.TreeViewColumn(title,renderer,text=idx)
			col.set_resizable(True)
			col.set_sort_column_id(idx)
			view.append_column(col)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		scroll.add(view)
		self.vbox.pack_start(scroll)

		for tag, freq in all_tags:
			self.store.append((tag, freq))

		self.show_all()

		response = self.run()

		self.destroy()
