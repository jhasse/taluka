#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Taluka IDE
# Copyright (C) 2007 Jan Niklas Hasse <jhasse@gmail.com>
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
import gtk.glade
import os
import reloc
import newproject
import urllib
import project
import shutil
import reloc
import project

class NewProject:
	def __init__(self, main):
		self.main = main
		window = main.window
		self.glade = gtk.glade.XML(os.path.join(reloc.DATADIR, 'taluka/newproject.glade'))
		self.glade.signal_autoconnect(self)
		self.assistant = self.glade.get_widget('assistant1')
		self.assistant.set_transient_for(window)
		self.assistant.connect('prepare', self.on_prepare)
		self.assistant.show()
		self.iconview = self.glade.get_widget('iconview1')
		assert self.iconview != None
		self.model = gtk.ListStore(str, gtk.gdk.Pixbuf)
		pixbuf = self.iconview.render_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_DND, None)
		self.model.append(['Empty Project', pixbuf])
  		try:
  			icon_theme = gtk.icon_theme_get_default()
  			pixbuf = icon_theme.load_icon("utilities-terminal", 32, 0)
  		except:
  			pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(reloc.DATADIR, 'taluka/templates/console.png'))
		self.model.append(['Console Application', pixbuf])
		pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(reloc.DATADIR, 'taluka/templates/gtk.png'))
		self.model.append(['GTK Application', pixbuf])
		pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(reloc.DATADIR, 'taluka/templates/wxwidgets.png'))
		self.model.append(['wxWidgets Application', pixbuf])
		pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(reloc.DATADIR, 'taluka/templates/opengl.png'))
		self.model.append(['OpenGL Application', pixbuf])
		self.iconview.set_model(self.model)
		self.iconview.set_text_column(0)
		self.iconview.set_pixbuf_column(1)
		self.iconview.connect('selection-changed', self.on_select, self.model)
		
		# Page 2
		self.assistant.set_page_complete(self.assistant.get_nth_page(1), True)
		self.radio_c = self.glade.get_widget('c')
		self.radio_cpp = self.glade.get_widget('cpp')
		self.radio_py = self.glade.get_widget('python')
		
		# Page 3
		self.filechooserbutton = self.glade.get_widget('filechooserbutton1')
		self.filechooserbutton.set_current_folder(os.path.expanduser('~'))
		self.entry_title = self.glade.get_widget('entry_title')
		self.entry_result = self.glade.get_widget('entry_result')
		
	
	def on_cancel(self, widget):
		self.assistant.destroy()
	
	def on_prepare(self, widget, page):
		self.assistant.set_page_title(page, 'Project Wizard - Page %d' % (self.assistant.get_current_page() + 1))
		if self.assistant.get_current_page() == 1: # Language Selection
			if self.iconview.get_selected_items()[0][0] == 3: # wxWidgets is C++/Python only
				if self.radio_c.get_active():
					self.radio_cpp.set_active(True)
	
	def on_select(self, iconview, model=None):
		complete = True
		selected = iconview.get_selected_items()
		if len(selected) == 0:
			complete = False
		else:
			if selected[0][0] == 3: # wxWidgets is C++/Python only
				self.radio_c.set_sensitive(False)
			else:
				self.radio_c.set_sensitive(True)
		self.assistant.set_page_complete(self.assistant.get_nth_page(self.assistant.get_current_page()), complete)
	
	def on_insert(self, entry_DONTUSE):
		self.entry_result.set_text(
				os.path.join(urllib.unquote(self.filechooserbutton.get_current_folder_uri()),
					self.entry_title.get_text().replace("/", "")
				).replace("file://", "")
				)
		complete = True
		if len(self.entry_title.get_text()) == 0:
			complete = False
		self.assistant.set_page_complete(self.assistant.get_nth_page(self.assistant.get_current_page()), complete)
		
	def on_apply(self, widget):
		folder = self.entry_result.get_text()
		for verz in get_path_nodes(folder):
			if not verz == "" and not os.path.isdir(verz): #Prüfen ob es das Verzeichnis schon gibt
				os.mkdir(verz)
		bin_name = self.entry_title.get_text().replace("/", "") # / is not a valid file name character
		project_filename = os.path.join(folder, bin_name) + ".taluka"
		project_type = self.iconview.get_selected_items()[0][0]
		if self.radio_c.get_active():
			language = 'c'
		if self.radio_cpp.get_active():
			language = 'cpp'
		if self.radio_py.get_active():
			language = 'py'
			
		main_file = 'main.' + language
		
		if project_type == 0: # Empty Project
			template_file = None
		elif project_type == 1:
			template_file = 'console.' + language
		elif project_type == 2:
			template_file = 'gtk.' + language
		elif project_type == 3:
			template_file = 'wxwidgets.' + language
		elif project_type == 4:
			template_file = 'opengl.' + language

		if template_file != None:
			shutil.copyfile(os.path.join(reloc.DATADIR, 'taluka/templates/' + template_file), os.path.join(folder, main_file))
		else:
			file = open(os.path.join(folder, main_file), 'w')
			file.close()

		fout = open(project_filename, 'w')
		
		fout.write("""<?xml version="1.0" encoding="utf-8" ?>
<taluka version="0.1">
	<title>%s</title>\n""" % self.entry_title.get_text())
	
		if language == 'py':
			fout.write('	<file src="%s"/>' % main_file)
		else:
			fout.write('	<target src="bin/%s">\n		<file src="%s"/>\n	</target>' % (bin_name, main_file))

		fout.write("\n</taluka>")
		fout.close()

		newproject = project.Project(self.main)
		newproject.filename = project_filename
		newproject.open()

def get_path_nodes(was):
	splitted = was.split('/')
	ergebnis = []
	for i in range(len(splitted)):
			ergebnis.append('/'.join(splitted[0:i+1]))
	return ergebnis
