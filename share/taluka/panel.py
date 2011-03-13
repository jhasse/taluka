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

class Panel(gtk.VBox):
	def __init__(self):
		super(type(self), self).__init__(self)
		self._notebook = gtk.Notebook()
	
	def add_item(self, item, name, image):
		hbox = gtk.HBox()
		hbox.add(image)
		hbox.add(gtk.Label(name))
		self._notebook.append_page(item, hbox)
		item.show_all()
		hbox.show_all()
	
	def activate_item(self, item):
		self._notebook.set_current_page(self._notebook.page_num(item))
