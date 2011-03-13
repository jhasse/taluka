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

import gtk

class StartHere(gtk.VBox):
	def __init__(self):
		super(type(self), self).__init__(self)
		
		self._label = gtk.Label("Start here")
		self.add(self._label)
		self.show_all()
		
		self._hbox = gtk.HBox()
		
		box = gtk.VButtonBox()
		box.set_layout(gtk.BUTTONBOX_START)
		box.set_border_width(30)
		
		button = gtk.Button("Create a new project")
		button.set_alignment(0, 0.5)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_BUTTON))
		box.add(button)

		button = gtk.Button("Open an existing project")
		button.set_alignment(0, 0.5)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_BUTTON))
		box.add(button)

		button = gtk.Button("About Taluka")
		button.set_alignment(0, 0.5)
		button.set_image(gtk.image_new_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_BUTTON))
		box.add(button)
		
		self._hbox.add(box)
		
		self._hbox.show_all()

	def get_content(self):
		return self._hbox

	def get_view(self):
		return None
	
	def get_document(self):
		return None
	
	def get_state(self):
		return None
	
	def _get_name(self):
		return self._label.get_text()
