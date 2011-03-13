#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007-2008 Jan Niklas Hasse <jhasse@gmail.com>
#                     Jannes Meyer <jannes.meyer@gmail.com>
#
# This code is based on gedit: Copyright 2003-2006 Paolo Maggi
# Also check out gedit's AUTHORS file.
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

class TextRegion:
	def __init__(self, buffer):
		self.buffer = buffer
		self.subregions = None
		self.time_stamp = 0
