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

from scons import *

class Build:
	def __init__(self, main):
		self.main = main
		self.menuitem = self.main.glade.get_widget('menuitem_project')
		self.menuitem.set_sensitive(True)
		self.main.glade.get_widget('build_and_run').connect('activate', self.build_and_run)
		self.main.glade.get_widget('build').connect('activate', self.build)
		self.main.glade.get_widget('run').connect('activate', self.run)
		self.main.glade.get_widget('rebuild').connect('activate', self.rebuild)
		self.main.glade.get_widget('clean').connect('activate', self.clean)
		
		self._scons = Scons(self.main)
	
	def build_and_run(self, data=None):
		if(self.build()):
			return self.run()
		return False
	
	def build(self, data=None):
		self._scons.create()
		self._scons.build()
		return True
	
	def run(self, data=None):
		print "run"
		return True
	
	def clean(self, data=None):
		print "clean"
		return True
	
	def rebuild(self, data=None):
		if(self.clean()):
			return self.build()
		return False
