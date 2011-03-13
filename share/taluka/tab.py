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

import gtk
from document import Document
from view import View
import utils
import gobject
import gnomevfs
from enums import *

TAB_KEY = "GEDIT_TAB_KEY"

class Tab(gtk.VBox):
	def __init__(self):
		super(type(self), self).__init__()

		self._state = TAB_STATE_NORMAL

		self._not_editable = False

		self._save_flags = 0
		
		self._ask_if_externally_modified = True;
		
		# Create the scrolled window
		sw = gtk.ScrolledWindow()
		self._view_scrolled_window = sw

		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)


		self._auto_save_timeout = 0 # Not Implemented
#TODO:
#	/* Manage auto save data */
#	lockdown = gedit_app_get_lockdown (gedit_app_get_default ());
#	tab->priv->auto_save = gedit_prefs_manager_get_auto_save () &&
#			       !(lockdown & GEDIT_LOCKDOWN_SAVE_TO_DISK);
#	tab->priv->auto_save = (tab->priv->auto_save != FALSE);

#	tab->priv->auto_save_interval = gedit_prefs_manager_get_auto_save_interval ();
#	if (tab->priv->auto_save_interval <= 0)
#		tab->priv->auto_save_interval = GPM_DEFAULT_AUTO_SAVE_INTERVAL;

		doc = Document()
		doc.set_data(TAB_KEY, self)
		
		self._document = doc

#	_gedit_document_set_mount_operation_factory (doc,
#						     tab_mount_operation_factory,
#						     tab);

		self._view = View(doc)
		self._view.show()
		self._view.set_data(TAB_KEY, self)
		
		self.pack_end(sw, True, True, 0)
#	gtk_box_pack_end (GTK_BOX (tab), sw, TRUE, TRUE, 0);

		sw.add(self._view)
#	gtk_container_add (GTK_CONTAINER (sw), tab->priv->view);

		sw.set_shadow_type(gtk.SHADOW_IN)
#	gtk_scrolled_window_set_shadow_type (GTK_SCROLLED_WINDOW (sw),
#					     GTK_SHADOW_IN);

		sw.show()
		
		self._scrolledwindow = sw
#	gtk_widget_show (sw);

#	g_signal_connect (doc,
#			  "notify::uri",
#			  G_CALLBACK (document_uri_notify_handler),
#			  tab);
#	g_signal_connect (doc,
#			  "modified_changed",
#			  G_CALLBACK (document_modified_changed),
#			  tab);
#	g_signal_connect (doc,
#			  "loading",
#			  G_CALLBACK (document_loading),
#			  tab);
#	g_signal_connect (doc,
#			  "loaded",
#			  G_CALLBACK (document_loaded),
#			  tab);
#	g_signal_connect (doc,
#			  "saving",
#			  G_CALLBACK (document_saving),
#			  tab);
#	g_signal_connect (doc,
#			  "saved",
#			  G_CALLBACK (document_saved),
#			  tab);

#	g_signal_connect_after (tab->priv->view,
#				"focus-in-event",
#				G_CALLBACK (view_focused_in),
#				tab);

#	g_signal_connect_after (tab->priv->view,
#				"realize",
#				G_CALLBACK (view_realized),
#				tab);
	
	def load(self, uri, encoding, line_pos, create):
		print "[DEBUG] load(",uri,",",encoding,",",line_pos,",",create,")"

#		g_return_if_fail (tab->priv->state == GEDIT_TAB_STATE_NORMAL);
		doc = self.get_document()
		if doc == None:
			return

		self.set_state(TAB_STATE_LOADING);
		
		self._tmp_line_pos = line_pos
		self._tmp_encoding = encoding
		
		if self._auto_save_timeout > 0:
			self.remove_auto_save_timeout()
		
		doc.load(uri, encoding, line_pos, create)
	
	def save(self):
		if self._state != GEDIT_TAB_STATE_NORMAL and self._state != GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION and self._state != GEDIT_TAB_STATE_SHOWING_PRINT_PREVIEW:
			return
		if self._tmp_save_uri != None:
			return
		if self._tmp_encoding != None:
			return

		doc = self.get_document()
		assert doc != None
		if doc.is_untitled():
			return
		
		if self._state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION:
			tab.set_message_area(None)
			save_flags = self._save_flags | GEDIT_DOCUMENT_SAVE_IGNORE_MTIME
		else:
			save_flags = self._save_flags;
		
		self.set_state(GEDIT_TAB_STATE_SAVING)
		
		self._tmp_save_uri = doc.get_uri()
		self._tmp_encoding = doc.get_encoding()

		if tab._auto_save_timeout > 0:
			self.auto_save_timeout()
		
		doc.save(save_flags)

	def get_content(self):
		return self._scrolledwindow

	def get_view(self):
		return self._view
	
	def get_document(self):
		return self._document
	
	def get_state(self):
		return self._state
	
	def set_auto_save_enabled(self, enabled):
		self._auto_save = enabled
	
	def get_auto_save_enabled(self):
		return self._auto_save
	
	def get_auto_save_interval(self, interval):
		self._auto_save_interval = interval

	def get_auto_save_interval(self):
		return self._auto_save_interval

	def _get_name(self):
		doc = self.get_document();
		
		name = doc.get_short_name_for_display();

		# FIXME:
		#	/* Truncate the name so it doesn't get insanely wide. */
		#	docname = gedit_utils_str_middle_truncate (name, MAX_DOC_NAME_LENGTH);
		docname = name;

		if doc.get_modified():
			tab_name = "*" + docname;
		else:
			if doc.get_readonly():
				tab_name = "%s [%s]" % (docname, "Read only")
			else:
				tab_name = docname
		return tab_name
	
	def get_uri(self):
		return self.get_document().get_uri()
	
	def get_tooltips(self):
		doc = self.get_document()
		
		uri = doc.get_uri_for_display()
		if uri == None:
			return
		
		ruri = utils.replace_home_dir_with_tilde(uri)

		# Not sure: ruri_markup = g_markup_printf_escaped ("<i>%s</i>", ruri);
		ruri_markup = "<i>%s</i>" % gobject.markup_escape_text(uri);

		if(self._state == TAB_STATE_LOADING_ERROR):
			tip = "Error opening file %s" % ruri_marup
		elif(self._state == TAB_STATE_REVERTING_ERROR):
			tip = "Error reverting file %s" % ruri_markup
		elif(self._state == TAB_STATE_SAVING_ERROR):
			tip = "Error saving file %s" % ruri_markup
		else:
			mime_type = doc.get_mime_type()
			mime_description = None
			if mime_type != None:
				mime_description = gnomevfs.mime_get_description(mime_type)
			
			if mime_description == None:
				mime_full_description = mime_type
			else:
				mime_full_description = "%s (%s)" % (mime_description, mime_type)
			
			enc = doc.get_encoding()
			
			if enc == None:
				encoding = "Unicode (UTF-8)"
			else:
				encoding = enc.to_string()

			tip = "<b>%s</b> %s\n\n<b>%s</b> %s\n<b>%s</b> %s" % (
			                 gobject.markup_escape_text("Name:"),
			                 gobject.markup_escape_text(ruri),
			                 gobject.markup_escape_text("MIME Type:"),
			                 gobject.markup_escape_text(mime_full_description),
			                 gobject.markup_escape_text("Encoding"),
			                 gobject.markup_escape_text(encoding));
			                          

			# FIXME: Unsure about this:
			#tip =  g_markup_printf_escaped ("<b>%s</b> %s\n\n"
			#			        "<b>%s</b> %s\n"
			#			        "<b>%s</b> %s",
			#			        _("Name:"), ruri,
			#			        _("MIME Type:"), mime_full_description,
			#			        _("Encoding:"), encoding);

		return tip

	# FIXME: add support for theme changed. I think it should be as easy as
	# call g_object_notify (tab, "name") when the icon theme changes
	def _get_icon(self):
		screen = self.get_screen()

		theme = gtk.icon_theme_get_for_screen(screen)
		if theme == None:
			return None

		icon_size = gtk.icon_size_lookup_for_settings(self.get_settings(), gtk.ICON_SIZE_MENU)[1]

		if self._state == TAB_STATE_LOADING:
			pixbuf = get_stock_icon(theme, gtk.STOCK_OPEN, icon_size)
		elif self._state == TAB_STATE_REVERTING:
			pixbuf = get_stock_icon (theme, gtk.STOCK_REVERT_TO_SAVED, icon_size)
		elif self._state == TAB_STATE_SAVING:
			pixbuf = get_stock_icon(theme, gtk.STOCK_SAVE, icon_size)
		elif self._state == TAB_STATE_PRINTING:
			pixbuf = get_stock_icon(theme, gtk.STOCK_PRINT, icon_size)
		elif self._state == TAB_STATE_PRINT_PREVIEWING or self._state == TAB_STATE_SHOWING_PRINT_PREVIEW:
			pixbuf = get_stock_icon (theme, gtk.STOCK_PRINT_PREVIEW, icon_size)
		elif self._state == TAB_STATE_LOADING_ERROR or \
		     self._state == TAB_STATE_REVERTING_ERROR or \
		     self._state == TAB_STATE_SAVING_ERROR or \
		     self._state == TAB_STATE_GENERIC_ERROR:
			pixbuf = get_stock_icon (theme, gtk.STOCK_DIALOG_ERROR, icon_size)
		elif self._state == TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION:
			pixbuf = get_stock_icon(theme, GTK_STOCK_DIALOG_WARNING, icon_size)
		else:
			doc = self.get_document()

			raw_uri = doc.get_uri()
			mime_type = doc.get_mime_type()

			pixbuf = get_icon(theme, raw_uri, mime_type, icon_size)

		return pixbuf

	def _save(self):
		if not ((self._state == TAB_STATE_NORMAL) or (self._state == TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION) or
			    (self._state == TAB_STATE_SHOWING_PRINT_PREVIEW)):
			return
		if self._tmp_save_uri != None:
			return
		if self._tmp_encoding != None:
			return
		
		doc = self.get_document()
		
		if doc.is_untitled():
			return
			
		if self._state == TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION:
			self.set_message_area(None)
			save_flags = self._save_flags | GEDIT_DOCUMENT_SAVE_IGNORE_MTIME;
		else:
			save_flags = self._save_flags

		self.set_state(TAB_STATE_SAVING)

		# uri used in error messages, will be freed in document_saved
		self._tmp_save_uri = doc.get_uri()
		self._tmp_encoding = doc.get_encoding()
		
		if self._auto_save_timeout > 0:
			self.remove_auto_save_timeout()
		
		doc.save(save_flags)

	def _save_as(self, uri, encoding):
		
		# TODO:	g_return_if_fail ((tab->priv->state == GEDIT_TAB_STATE_NORMAL) ||
#			  (tab->priv->state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION) ||
#			  (tab->priv->state == GEDIT_TAB_STATE_SHOWING_PRINT_PREVIEW));
	 #g_return_if_fail (encoding != NULL);

#	g_return_if_fail (tab->priv->tmp_save_uri == NULL);
#	g_return_if_fail (tab->priv->tmp_encoding == NULL);

		doc = self.get_document()

		# reset the save flags, when saving as
		self._save_flags = 0
		save_flags = 0

		if self._state == TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION:
			# We already told the user about the external
			# modification: hide the message area and set
			# the save flag.

			set_message_area (tab, NULL);
			save_flags = DOCUMENT_SAVE_IGNORE_MTIME

		self.set_state(TAB_STATE_SAVING)

		# uri used in error messages... strdup because errors are async
		# and the string can go away, will be freed in document_saved
	#	FIXME: tab->priv->tmp_save_uri = g_strdup (uri);
		self._tmp_encoding = encoding;

		if self._auto_save_timeout > 0:
			tab.remove_auto_save_timeout()

		doc.save_as(uri, encoding, self._save_flags)

	def _can_close(self):
		ts = self.get_state()

		# if we are loading or reverting, the tab can be closed
		if ts == TAB_STATE_LOADING       or \
		   ts == TAB_STATE_LOADING_ERROR or \
		   ts == TAB_STATE_REVERTING     or \
		   ts == TAB_STATE_REVERTING_ERROR:
			return True

		# Do not close tab with saving errors
		if ts == TAB_STATE_SAVING_ERROR:
			return False
		
		doc = self.get_document()

		# TODO: we need to save the file also if it has been externally
		# modified - Paolo (Oct 10, 2005)

		return not doc.get_modified() and not doc.get_deleted()
	
def tab_new_from_uri(uri, encoding, line_pos, create):
	tab = Tab()
	tab.load(uri, encoding, line_pos, create)
	return tab

def get_stock_icon(theme, stock, size):
	pixbuf = theme.load_icon(stock, size, 0);
	if pixbuf == None:
		return None
	return pixbuf # FIXME: resize(pixbuf, size)
	
def get_icon(theme, uri, mime_type, size):
	pixbuf = theme.load_icon('stock_people', size, 0)
	return pixbuf
	
def tab_get_from_document(doc):
	return doc.get_data(TAB_KEY)
