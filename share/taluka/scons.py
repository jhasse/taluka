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

import gtk
import re
import subprocess
from subprocess import *
import gobject

class Scons:
	def __init__(self, main):
		self._main = main
		self._window = main # FIXME
		
		self._bottom_panel = self._main.get_bottom_panel()

		image = gtk.Image()
		image.set_from_stock(gtk.STOCK_EXECUTE, gtk.ICON_SIZE_MENU)

		self._panel = BuildResultsPanel(self._window)
		self._bottom_panel.add_item(self._panel, 'Build Results', image)
		
		
		self._directory = self._main.active_project.directory
		
		self.prog = re.compile("(.*):(.*): error: (.*)")

	def create(self):
		fout = open('%s/SConstruct'%self._directory, 'w')
		fout.write('env = Environment()\n')
		
		store = self._main.manager.model
		column = 0
		i = store.get_iter_first()
		while i != None:
			if store.iter_has_child(i):
				fout.write('env.Program(target="%s", source=Split("' % store.get_value(i, column))
				child = store.iter_children(i)
				while child != None:
					fout.write('%s ' % store.get_value(child, column))
					child = store.iter_next(child)
				fout.write('"))\n')
			i = store.iter_next(i)

	def build(self):
		self.create() # change me
		
		self._bottom_panel.activate_item(self._panel)
		
#		docs = self._window.get_unsaved_documents()
#		for doc in docs:
#			if doc.get_uri() != None:
#				doc.save(0)

		self._panel.clear()

		cmdline = "scons -Q debug=1"
		self.pipe = subprocess.Popen(cmdline.split(" "), stdout=PIPE, stderr=PIPE, cwd=self._directory)
		
		gobject.io_add_watch(self.pipe.stdout,
		                     gobject.IO_IN | gobject.IO_HUP,
		                     self.on_output)
		gobject.io_add_watch(self.pipe.stderr,
		                     gobject.IO_IN | gobject.IO_HUP,
		                     self.on_output)

		self._firstError = True
		# Wait for the process to complete
		gobject.child_watch_add(self.pipe.pid, self.on_child_end)

	def on_output(self, source, condition):
		line = source.readline()

		if len(line) > 0:
			treeIter = self._panel.append(line[:-1])
			result = self.prog.match(line)
			if result is not None and self._firstError:
				self._firstError = False
				self._panel.activate(treeIter)
			return True

		return False
		
	def on_child_end(self, pid, error_code):
		self._panel.append("Done!")
		
	def clean(self):
		return True

class BuildResultsPanel(gtk.ScrolledWindow):

	def __init__(self, window):
		super(BuildResultsPanel, self).__init__ ()
		
		self._window = window
		self.model = gtk.ListStore(str)
		self._view = gtk.TreeView()
		self.renderer = gtk.CellRendererText()
		self._view.append_column(gtk.TreeViewColumn("Message", self.renderer, text=0))
		self._view.set_model(self.model)
		self._view.set_headers_visible(False)
		self._view.connect("row-activated", self.on_row_activated)
		self._view.show()
		self.add(self._view)
		self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
# 		self._window = window
# 		
# 		self._view = gtk.TreeView()
# 		self._renderer = gtk.CellRendererText()
# 		self._view.append_column(gtk.TreeViewColumn("Message", self._renderer, text=0))
# 		self._model = gtk.ListStore(str)
# 		self._view.set_model(self._model)

# 		self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
# 		self.add(self._view)
# 		self._view.connect("row-activated", self.on_row_activated)
# 		self._view.show()

	def on_row_activated(self, view, row, column):
		model = view.get_model()
		iter = model.get_iter(row)
		
		str = model.get_value(iter, 0)
		result = re.match("(.*?):(.*?):.*", str)
		line = result.group(2)
		file_name = result.group(1)
		
		doc = self._window.get_active_document()
		
		line = int(line) - 1
		doc.goto_line(line)

		view = self._window.get_active_view()

		text_iter = doc.get_iter_at_line(line)
		view.scroll_to_iter(text_iter, 0.25)

	def append(self, message):
		return self._view.get_model().append([message])
	
	def activate(self, treeIter):
		self._view.row_activated(self._view.get_model().get_path(treeIter), self._view.get_column(0))
	
	def clear(self):
		self._view.get_model().clear()

