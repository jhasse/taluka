#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007-2008 Jan Niklas Hasse <jhasse@gmail.com>
#                     Jannes Meyer <jannes.meyer@gmail.com>
#
# As this code is based on gedit: Copyright 2003-2006 Paolo Maggi
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

style_scheme_manager = None

def get():
	style_scheme_manager = globals()['style_scheme_manager']
	if style_scheme_manager == None:
		import gtksourceview2
		style_scheme_manager = gtksourceview2.StyleSchemeManager();
		add_gedit_styles_path(style_scheme_manager)

	return style_scheme_manager

def add_gedit_styles_path(mgr):
	dir = get_gedit_styles_path();

	if dir != None:
		mgr.append_search_path(dir)

GEDIT_STYLES_DIR=".gnome2/gedit/styles"

def get_gedit_styles_path():
	# FIXME: We shouldn't return None
	return None
