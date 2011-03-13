#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2008-2009 Jan Niklas Hasse <jhasse@gmail.com>
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

import os.path
import gio

def replace_home_dir_with_tilde(uri):
	if uri == None:
		return None
	
	home = os.path.expanduser('~')

	if uri.find(home) == 0:
		uri = uri.replace(home, '~', 1)

	return uri

def uri_for_display(uri):
	gfile = gio.File(uri)
	return gfile.get_parse_name()

def uri_exists(text_uri):
	debug_message(DEBUG_UTILS, "text_uri: %s" % text_uri)

	gfile = gio.File(text_uri)
	res = gfile.query_exists(None)

	gedit_debug_message(DEBUG_UTILS, res);

	return res
