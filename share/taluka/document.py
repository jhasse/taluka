#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Jan Niklas Hasse <jhasse@gmail.com>
#                    Jannes Meyer <jannes.meyer@gmail.com>
#                    Fabian Franzen <flammenvogel@arcor.de>
#
# This file is part of Taluka.
#
# Taluka is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Taluka is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Taluka.  If not, see <http://www.gnu.org/licenses/>.

import gtksourceview2
import gtk
import gnomevfs
import gobject
import os
import pango
import urllib
import encoding
from encoding import encoding_get_utf8
from prefs_manager import *
from textregion import TextRegion
import style_scheme_manager
import gio
import utils

CURSOR_MOVED = 0
LOAD = 1
LOADING = 2
LOADED = 3
SAVE = 4
SAVING = 5
SAVED = 6
SEARCH_HIGHLIGHT_UPDATED = 7
LAST_SIGNAL = 8

class Document(gtksourceview2.Buffer):
	__gsignals__ = { 'load' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING, encoding.Encoding, gobject.TYPE_INT, gobject.TYPE_BOOLEAN,)) }
	def __init__(self):
		super(type(self), self).__init__()
		
		self._to_search_region = None
		self._search_text = None
		
		self._uri = None
		self._vfs_uri = None
		self._untitled_number = get_untitled_number()
		
		self._mime_type = "text/plain"
		
		self._readonly = False
		
		self._stop_cursor_moved_emission = False
		
		self._last_save_was_manually = True
		self._language_set_by_user = False
		
		self._dispose_has_run = False
		
		self._mtime = 0
		
		self._time_of_last_save_or_load = gobject.get_current_time()
		
		self._encoding = encoding_get_utf8()
		
		self.set_max_undo_levels(prefs_manager_get_undo_actions_limit())
		
		self.set_highlight_matching_brackets(prefs_manager_get_bracket_matching())
		
		self.set_enable_search_highlighting(prefs_manager_get_enable_search_highlighting())
		self.set_highlight_syntax(True)

		style_scheme = get_default_style_scheme()
		if style_scheme != None:
			self.set_style_scheme(style_scheme)

# FIXME:
#		g_signal_connect_after (doc, 
#				  	"insert-text",
#				  	G_CALLBACK (insert_text_cb),
#				  	NULL);

#		g_signal_connect_after (doc, 
#				  	"delete-range",
#				  	G_CALLBACK (delete_range_cb),
#				  	NULL);
	
	def get_uri(self):
		return self._uri
	
	def get_uri_for_display(self):
		if self._uri == None:
			return "Unsaved Document %d" % self._untitled_number
		elif self._vfs_uri == None:
			return gnomevfs.uri_for_display(self._uri)
		else:
			name = gnomevfs.uri_to_string(self._vfs_uri, GNOME_VFS_URI_HIDE_PASSWORD)
			if name == None:
				return gnomevfs.uri_for_display(self._uri)
			
			uri_for_display = gnomevfs.format_uri_for_display(name)
			return uri_for_display;
	
	def get_short_name_for_display(self):
		if self._uri == None:
			return "Unnamed"
		return self._uri.short_name
	
	def get_mime_type(self):
		if self._mime_type == None:
			return "text/plain"
		return self._mime_type
	
	def get_readonly(self):
		return self._readonly
	
	def load(self, uri, encoding, line_pos, create):
		self.emit('load', uri, encoding, line_pos, create)
		
		# The loading differs from original gedit. I'm using the example code
		# of python-gtksourceview2

		self.begin_not_undoable_action()
		# FIXME: This is ulgy!!!
		txt = open(uri[0][7:].replace("%20", " ")).read()
		self.set_text(txt)
		self.set_data('filename', uri)
		self.end_not_undoable_action()

		self.set_modified(False)
		self.place_cursor(self.get_start_iter())
	
	def save(self, flags):
		if self._uri == None:
			return

		self.emit(document_signals[SAVE], self._uri, self._encoding, flags)
	
	def save_as(self, uri, encoding, _save_flags):
		gio.File(uri).replace_contents(self.get_text(self.get_start_iter(), self.get_end_iter()))
	
	def is_untouched(self):
		return self._uri == None and not self.get_modified();
	
	def is_untitled(self):
		if self._uri == None:
			return True
		else:
			return False
	
	def goto_line(self, line):
		text_iter = gtk.TextIter()
		text_iter.set_line(line)
		self.place_cursor(text_iter)

	def get_can_search_again(self):
		return ((self._search_text != None) and (self._search_text != '\0'))
	
	def set_enable_search_highlighting(self, enable):
		
		enable = enable != False # TODO: Fint out what this is for
		
		if (self._to_search_region != None) == enable:
			return
		
		if self._to_search_region != None:
			# Disable search highlighting
			if self._found_tag != None:
				# If needed remove the found_tag
				
				bounds = self.get_bounds()

				self.remove_tag(self._found_tag, bounds[0], bounds[1])
		
			text_region_destroy(self._to_search_region, True)
			self._to_search_region = None
		else:
			self._to_search_region = TextRegion(self)
			if self.get_can_search_again():
				# If search_text is not empty, highligth all its occurrences
				
				bounds = self.get_bounds()
				
				to_search_region_range(self, bounds[0], bounds[1])

	def get_encoding(self):
		return self._encoding
	
	def get_deleted(self):
		return self._uri and not utils.uri_exists(self._uri)

def get_default_style_scheme():
	manager = style_scheme_manager.get()
	scheme_id = prefs_manager_get_source_style_scheme()
	def_style = manager.get_scheme(scheme_id)

	if def_style == None:
		# Should I use something like g_warning here?
		print "Default style scheme '%s' cannot be found, falling back to 'classic' style scheme " % scheme_id
		def_style = manager.get_scheme("classic")
		if def_style == None:
			print "Style scheme 'classic' cannot be found, check your GtkSourceView installation."

	return def_style

def get_untitled_number():
	i = 1
	# TODO: Implement something better
	return ++i

# 		
# 		self.main = main
# 		notebook = main.notebook_files
# 		lm = gtksourceview2.SourceLanguagesManager()
# 		buffer = gtksourceview2.SourceBuffer()
# 		buffer.set_check_brackets(True)
# 		buffer.set_highlight(True)
# 		buffer.set_data('languages-manager', lm)

# 		if filename == None:
# 			self.label = "Unbenannt"
# 		else:
# 			try:
# 				self.label = os.path.basename(filename)
# 				manager = buffer.get_data('languages-manager')
# 				assert manager != None
# 				if not os.path.isabs(filename):
# 					filename = os.path.abspath(os.path.join(workingdir, filename))
# 				path = filename
# 				uri = gnomevfs.URI(path)

# 				mime_type = gnomevfs.get_mime_type(path) # needs ASCII filename, not URI
# 				if mime_type:
# 					language = manager.get_language_from_mime_type(mime_type)
# 					if language:
# 						buffer.set_language(language)

# 				buffer.begin_not_undoable_action()
# 				# TODO: use g_io_channel when pygtk supports it
# 				txt = open(urllib.unquote(uri.path)).read()
# 			except Exception, e:
# 				raise FileException(filename, str(e))
# 			buffer.set_text(txt)
# 			buffer.set_data('filename', uri.path)
# 			buffer.end_not_undoable_action()
# 			buffer.set_modified(False)
# 			buffer.place_cursor(buffer.get_start_iter())

# 		
# 		buffer.connect('changed', self.on_changed, notebook)

# #		self = gtk.ScrolledWindow() # Wird später dafür gebraucht, den Tab wieder zu identifizieren.
# 		self = self
# 		self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
# 		self.add(self.sourceview)
# 		notebook.append_page(self, gtk.Label(self.label))
# 		self.show_all()
# 		notebook.set_current_page(-1)
# 		self.notebook_page = notebook.get_current_page()
# 		self.filename = filename
# 		self.modified = False
# 		self.notebook = notebook
# 	
# 	def save(self):
# 		if self.filename == None:
# 			self.label = gtk.Label("Unbenannt")
# 		else:
# 			try:
# 				file = open(self.filename, 'w')
# 				buffer = self.sourceview.get_buffer()
# 				file.write(buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter()))
# 				file.close()
# 			except Exception, e:
# 				raise FileException(self.filename, str(e))
# 		self.set_modified(False)
# 	
# 	def set_modified(self, modified):
# 		self.modified = modified
# 		if modified:
# 			self.notebook.set_tab_label(self, gtk.Label("*%s" % (self.label)))
# 		else:
# 			self.notebook.set_tab_label(self, gtk.Label("%s" % (self.label)))
# 	
# 	
# 	
# 	def can_close(self): # Returns True if the file can be closed
# 		main = self.main
# 		if self.modified:
# 			dialog = self.main.glade.get_widget('save_dialog')
# 			dialog.show()
# 			title = self.main.glade.get_widget('title')
# 			text = self.main.glade.get_widget('text')
# 			title.set_label('<b>Save the changes to document "%s" before closing?</b>' % (self.filename))
# 			text.set_label('If you don\'t save, changes will be permanently lost.')
# 			
# 			dialog = gtk.MessageDialog(main.window, type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_YES_NO,
# 				message_format='File %s is modified...\nDo you want to save the changes?' % (self.filename))
# 			dialog.set_title("Save file")
# 			response = dialog.run()
# 			if response == gtk.RESPONSE_YES:
# 				self.save()
# 				return True
# 			if response == gtk.RESPONSE_NO:
# 				return True
# 			return False
# 		return True
# 	
# 	def close(self):
# 		self.destroy()
# 	
# 	def on_changed(self, data, notebook):
# 		if not self.modified:
# 			self.set_modified(True)
# 	

