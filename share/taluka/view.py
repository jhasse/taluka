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
import pango
from debug import *

class View(gtksourceview2.View):
	def __init__(self, document):
		super(type(self), self).__init__()

		assert document != None
		
		self.set_buffer(document)
		
		self.set_show_line_numbers(True)
		self.set_show_line_marks(True)
		self.set_show_right_margin(True)
		self.set_auto_indent(True)
		self.set_insert_spaces_instead_of_tabs(False)
		self.set_tab_width(4)
		self.set_highlight_current_line(True)
		self.set_font(False, "Monospace 10")
		
		self._document = document
	
	def cut_clipboard(self):
		self._document.cut_clipboard(gtk.Clipboard(), True)

	def copy_clipboard(self):
		self._document.copy_clipboard(gtk.Clipboard())

	def paste_clipboard(self):
		self._document.paste_clipboard(gtk.Clipboard(), None, True)
					
	def delete_selection(self):
		raise NotImplementedError
	
	def select_all(self):
		raise NotImplementedError
	
	def scroll_to_cursor(self):
		debug(DEBUG_VIEW)
		buffer = self.get_buffer()
		if buffer == None:
			return
		self.scroll_to_mark(buffer.get_insert(), 0.25, False, 0.0, 0.0)
	
	def set_colors(use_default, background, text, selection, sel_text):
		raise NotImplementedError
	
	def set_font(self, font_name):
		font_desc = pango.FontDescription(font_name)
		if font_desc:
			self.modify_font(font_desc)
		
	def set_font(self, use_default, font_name):
		debug(DEBUG_VIEW)
		if use_default:
			font = prefs_manager_get_system_font()
			font_desc = pango.FontDescription(font)
		else:
			font_desc = pango.FontDescription(font_name)
		self.modify_font(font_desc)
