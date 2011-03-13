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

import xml.dom.minidom
import os

class Configuration:
	def __init__(self, filename, main):
		self.project_dir = os.path.dirname(filename)
		self.main = main
		self.data_model = main.manager.model
		self.dom = xml.dom.minidom.parse(filename)
		taluka = self.dom.getElementsByTagName("taluka")[0]

		self.version = taluka.getAttribute("version")
		self.title = taluka.getElementsByTagName("title")[0].firstChild.nodeValue
		
		expand_me = [] # Expand must be done after inserting the rows

		for node in taluka.childNodes:
			if node.nodeName == "target":
				target = self.append_item(None, node, 'binary', False)
				if node.getAttribute("expanded") == "True":
					expand_me.append(target)
				for cnode in node.childNodes:
					if cnode.nodeName == "file":
						self.append_item(target, cnode, 'text-x-c++src', True)
			elif node.nodeName == "file":
				self.append_item(None, node, 'text-x-c++src', True)

		for target in expand_me: # Now we can expand
			self.main.manager.treeview.expand_row(self.main.manager.model.get_path(target), False)

	def append_item(self, target, node, icon, is_file):
		filename = node.getAttribute("src")
		
		if is_file and node.getAttribute("opened") == "True":
			try:
				self.main.open_file(filename, self.project_dir)
			except:
				pass

		return self.data_model.append(target, [node.getAttribute("src"), icon])

	def get_title(self):
		return self.title

	def get_version(self):
		return self.version
