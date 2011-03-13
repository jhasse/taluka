#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Taluka IDE
# Copyright 2007-2008 Jan Niklas Hasse <jhasse@gmail.com>
#                     Jannes Meyer <jannes.meyer@gmail.com>
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
import project
import urllib
from newproject import *
from panel import *
from gnome import url_show
from window import Window

### MSGBOX FUNCTIONS START ###
def msg(text):
	# this function is deprecated, use info() instead
	info(text)

def info(text):
	dialog = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK, message_format='%s' % (text))
	dialog.run()
	dialog.destroy()

def error(text):
	dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK, message_format='%s' % (text))
	dialog.run()
	dialog.destroy()
###  MSGBOX FUNCTIONS END  ###

class App:
	def __init__(self):
		self._window = Window()

