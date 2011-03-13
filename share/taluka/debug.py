#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Jan Niklas Hasse <jhasse@gmail.com>
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

NO_DEBUG       =-1
DEBUG_VIEW     = 0
DEBUG_SEARCH   = 1
DEBUG_PRINT    = 2
DEBUG_PREFS    = 3
DEBUG_PLUGINS  = 4
DEBUG_TAB      = 5
DEBUG_DOCUMENT = 6
DEBUG_COMMANDS = 7
DEBUG_APP      = 8
DEBUG_SESSION  = 9
DEBUG_UTILS    = 10
DEBUG_METADATA = 11
DEBUG_WINDOW   = 12
DEBUG_LOADER   = 13
DEBUG_SAVER    = 14

def debug(section):
	print "[DEBUG] %d" % section

def debug_message(section, message):
	print "[DEBUG] {0} - {1}".format(section, message)

def warn_if_equal(expr1, expr2):
	result = expr1 == expr2
	if result:
		print "[DEBUG] Warning: {0} == {1}".format(expr1, expr2)
	return result
