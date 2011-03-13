#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007-2009 Jan Niklas Hasse <jhasse@gmail.com>
#                     Jannes Meyer <jannes.meyer@gmail.com>
#                     Fabian Franzen <flammenvogel@arcor.de>
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

class DocumentLoader:
	# If encoding == None, the encoding will be autodetected
	def __init__(self, doc, uri, encoding):
		self._doc = doc
		self._uri = uri
		self._encoding = encoding
	
	def get_document(self):
		return self._doc


def insert_text_in_document(loader, text, length):

	doc = loader.get_document()
	if text == None:
		return
	doc.begin_not_undoable_action()

# TODO: Implement this:
#	/* If the last char is a newline, don't add it to the buffer (otherwise
#	   GtkTextView shows it as an empty line). See bug #324942. */
#	if ((len > 0) && (text[len-1] == '\n'))
#		len--;

	# Insert text in the buffer
	doc.set_text(text, length)
	doc.set_modified(False)

	doc.end_not_undoable_action()
