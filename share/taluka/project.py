#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Taluka IDE
# Copyright (C) 2007 Jan Niklas Hasse <jhasse@gmail.com>
#                    Jannes Meyer <jannes.meyer@gmail.com>
#                    Fabian Franzen <flammenvogel@arcor.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xmlconfig
import os
import gtk
from file import *
from build import *

class Project:
	def __init__(self, main):
		self.main = main
		self.files = []
		self.filename = ""
		self.title = ""
	
	def open(self):
		config = xmlconfig.Configuration(self.filename, self.main)
		
		self.title = config.get_title()
	
		self.main.notebook_files.remove_page(0) # Close "Start here"
		self.main.active_project = self
		self.directory = os.path.dirname(self.filename)
		self.main.manager.update()
		self.build = Build(self.main)
	
	def save(self):
		fout = open(self.filename, 'w')
		
		fout.write("""<?xml version="1.0" encoding="utf-8" ?>
<taluka version="0.1">
	<title>%s</title>""" % self.title)

		store = self.main.manager.model
		column = 0
		i = store.get_iter_first()
		while i != None:
			if store.iter_has_child(i):
				fout.write('\n	<target src="%s">' % store.get_value(i, column))
				child = store.iter_children(i)
				while child != None:
					fout.write('\n		<file src="%s"/>' % store.get_value(child, column))
					child = store.iter_next(child)
				fout.write('\n	</target>')
			else:
				fout.write('\n	<file src="%s"/>' % store.get_value(i, column))
			i = store.iter_next(i)
	
		fout.write("\n</taluka>")
		fout.close()

class Manager:
	def __init__(self, main):
		self.main = main
		
		self.treeview = self.main.glade.get_widget('treeview_manager')
		assert self.treeview != None

		self.model = gtk.TreeStore(str, str)
		self.treeview.set_model(self.model)
		self.tvcolumn = gtk.TreeViewColumn('Pixbuf and Text')
		self.treeview.append_column(self.tvcolumn)
		self.cellpb = gtk.CellRendererPixbuf()
		self.cell = gtk.CellRendererText()
		self.tvcolumn.pack_start(self.cellpb, False)
		self.tvcolumn.pack_start(self.cell, True)
		self.tvcolumn.set_cell_data_func(self.cellpb, self.make_pixbuf)
		self.tvcolumn.set_attributes(self.cell, text=0)
		
		self.treeview.connect("row-activated", self.on_row_activated)
	
	def on_row_activated(self, treeview, path, view_column):
		self.main.open_file(self.model.get_value(self.model.get_iter(path), 0),
		                    self.main.active_project.directory)
	
	def update(self):
		pass
	
	def make_pixbuf(self, column, cell, model, iter):
		icon_theme = gtk.icon_theme_get_default()
		try:
			pixbuf = icon_theme.load_icon(model.get_value(iter, 1), 16, 0)
		except:
			pixbuf = None
		cell.set_property('pixbuf', pixbuf)
