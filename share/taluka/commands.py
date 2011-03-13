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

import commands
import window
#include "gedit-window-private.h"
#include "gedit-statusbar.h"
#import debug
import utils
#include "dialogs/gedit-close-confirmation-dialog.h"
#include "dialogs/gedit-open-location-dialog.h"
from file_chooser_dialog import *
import gnomevfs
import gtk
from enums import *
from debug import *
from tab import *

OPEN_DIALOG_KEY           = "gedit-open-dialog-key"
OPEN_LOCATION_DIALOG_KEY  = "gedit-open-location-dialog-key"
TAB_TO_SAVE_AS            = "gedit-tab-to-save-as"
LIST_OF_TABS_TO_SAVE_AS   = "gedit-list-of-tabs-to-save-as"
IS_CLOSING_ALL            = "gedit-is-closing-all"
IS_QUITTING               = "gedit-is-quitting"
IS_CLOSING_TAB            = "gedit-is-closing-tab"

def _file_new(action, window):
#	gedit_debug(DEBUG_COMMANDS)
	window.create_tab(True)

def get_tab_from_uri(docs, uri):
	for d in docs:
		u = d.get_uri()
		
		if u != None and gnomevfs.uris_match(uri, u):
			return tab_get_from_document(d)
	
	return None

def is_duplicated_uri(uris, u):
	for uri in uris:
		if gnomevfs.uris_match(u, uri):
			return True
	return False

def load_file_list(window, uris, encoding, line_pos, create):
	loaded_files = 0
	jump_to = True
	flash = True # Whether to flash a message in the statusbar
	
	debug(DEBUG_COMMANDS)

	if uris == None:
		return 0

	win_docs = window.get_documents()
	
	files_to_load = []
	
	for uri in uris:
		if not is_duplicated_uri(files_to_load, uri):
			tab = get_tab_from_uri(win_docs, uri)
			if tab != None:
				if uri == uris[0]:
					window.set_active_tab(tab)
					jump_to = False
					if line_pos > 0:
						doc = tab.get_document();
						view = tab.get_view();
						# document counts lines starting from 0
						document.goto_line(line_pos - 1)
						view.scroll_to_cursor()
						
				++loaded_files
			else:
				files_to_load.append(uris); # TODO: Or prepend?
	if files_to_load == None:
		return loaded_files
	
	
#	files_to_load = g_slist_reverse (files_to_load);
	tab = window.get_active_tab()
	if tab != None:
		doc = tab.get_document()
		
		if doc.is_untouched() and tab.get_state == TAB_STATE_NORMAL:
			uri = files_to_load.pop(0) # Removes the first element and returns it

			tab.load(uri, encoding, line_pos, create)

			jump_to = False;

			if len(files_to_load) == 0:
				# There is only a single file to load
				uri_for_display = utils.format_uri_for_display(uri)
				
				statusbar.flash_message(window.get_statusbar(), window._generic_message_cid,
				                        "Loading file '%s'\342\200\246" % uri_for_display)
				
				flash = False

			++loaded_files

	for uri_to_load in files_to_load:
		if uri_to_load == None:
			return 0
		
		tab = window.create_tab_from_uri(uri_to_load, encoding, line_pos, create, jump_to)
		
		if tab != None:
			jump_to = False
			++loaded_files
	
	if flash:
		if loaded_files == 1:
			if tab == None:
				return loaded_files
			
			doc = tab.get_document()
			
			uri_for_display = doc.get_uri_for_display()
			
#			gedit_statusbar_flash_message (GEDIT_STATUSBAR (window->priv->statusbar),
#						       window->priv->generic_message_cid,
#						       _("Loading file '%s'\342\200\246"),
#						       uri_for_display);
		else:
			pass
#			gedit_statusbar_flash_message (GEDIT_STATUSBAR (window->priv->statusbar),
#						       window->priv->generic_message_cid,
#						       ngettext("Loading %d file\342\200\246",
#								"Loading %d files\342\200\246",
#								loaded_files),
#						       loaded_files);

	return loaded_files

#/**
# * gedit_commands_load_uri:
# *
# * Do nothing if URI does not exist
# */
#void
#gedit_commands_load_uri (GeditWindow         *window,
#			 const gchar         *uri,
#			 const GeditEncoding *encoding,
#			 gint                 line_pos)
#{
#	GSList *uris = NULL;

#	g_return_if_fail (GEDIT_IS_WINDOW (window));
#	g_return_if_fail (uri != NULL);
#	g_return_if_fail (gedit_utils_is_valid_uri (uri));

#	gedit_debug_message (DEBUG_COMMANDS, "Loading URI '%s'", uri);

#	uris = g_slist_prepend (uris, (gchar *)uri);

#	load_file_list (window, uris, encoding, line_pos, FALSE);

#	g_slist_free (uris);
#}

def load_uris(window, uris, encoding, line_pos):
	print "[DEBUG] load_uris(",window,",",uris,",",encoding,",",line_pos,")"

	if window == None:
		return
	if uris == None:
		return
	
	return load_file_list(window, uris, encoding, line_pos, False)

#/*
# * From the command line we can specify a line position for the
# * first doc. Beside specifying a not existing uri creates a
# * titled document.
# */
#gint
#_gedit_cmd_load_files_from_prompt (GeditWindow         *window,
#				   const GSList        *uris,
#				   const GeditEncoding *encoding,
#				   gint                 line_pos)
#{
#	gedit_debug (DEBUG_COMMANDS);

#	return load_file_list (window, uris, encoding, line_pos, TRUE);
#}

def _file_save(action, window):
	tab = window.get_active_tab()
	if tab == None:
		return

	file_save(tab, window)

def open_dialog_response_cb(dialog, response_id, window):
	#	gedit_debug (DEBUG_COMMANDS);
	
	if response_id != gtk.RESPONSE_OK:
		dialog.destroy()
		return
	
	uris = dialog.get_uris()
	
	if uris == None:
		return

	encoding = dialog.get_encoding()

	dialog.destroy()

# FIXME: Implement this:
#
#	/* Remember the folder we navigated to */
#	 _gedit_window_set_default_path (window, uris->data);

	load_uris(window, uris, encoding, 0)

def open_dialog_destroyed(window):
	debug(DEBUG_COMMANDS)
	window.set_data(OPEN_DIALOG_KEY, None)

def _file_open(action, window):
	debug(DEBUG_COMMANDS)

	data = window.get_data(OPEN_DIALOG_KEY)

	if data != None:
		data.present()
		return

	open_dialog = FileChooserDialog("Open Files", window, gtk.FILE_CHOOSER_ACTION_OPEN, None,
	                                [[gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL],
	                                 [gtk.STOCK_OPEN, gtk.RESPONSE_OK]])

	window.set_data(OPEN_DIALOG_KEY, open_dialog)

	open_dialog.weak_ref(open_dialog_destroyed, window)

#	TODO: Set the curret folder uri

	open_dialog.connect("response", open_dialog_response_cb, window)
	open_dialog.show()


def save_dialog_response_cb(dialog, response_id, window):
	tab = dialog.get_data(TAB_TO_SAVE_AS)

	if response_id != gtk.RESPONSE_OK:
		dialog.destroy()
#	FIXME: Implment this ugly goto shit
#		goto save_next_tab;

	uri = dialog.get_uri()
	if uri == None:
		return

	encoding = dialog.get_encoding()
	
	dialog.destroy()

	if tab != None:
		doc = tab.get_document()

		doc = tab.get_document()

		uri_for_display = utils.uri_for_display(uri)

# TODO
#		/* let's remember the dir we navigated too,
#		 * even if the saving fails... */
#		 _gedit_window_set_default_path (window, uri);

		tab._save_as(uri, encoding)

# TODO:
#save_next_tab:

#	data = g_object_get_data (G_OBJECT (window),
#				  GEDIT_LIST_OF_TABS_TO_SAVE_AS);
#	if (data == NULL)
#		return;

#	/* Save As the next tab of the list (we are Saving All files) */
#	tabs_to_save_as = (GSList *)data;
#	g_return_if_fail (tab == GEDIT_TAB (tabs_to_save_as->data));

#	/* Remove the first item of the list */
#	tabs_to_save_as = g_slist_delete_link (tabs_to_save_as,
#					       tabs_to_save_as);

#	g_object_set_data (G_OBJECT (window),
#			   GEDIT_LIST_OF_TABS_TO_SAVE_AS,
#			   tabs_to_save_as);

#	if (tabs_to_save_as != NULL)
#	{
#		tab = GEDIT_TAB (tabs_to_save_as->data);

#		if (GPOINTER_TO_BOOLEAN (g_object_get_data (G_OBJECT (tab),
#							    GEDIT_IS_CLOSING_TAB)) == TRUE)
#		{
#			g_object_set_data (G_OBJECT (tab),
#					   GEDIT_IS_CLOSING_TAB,
#					   NULL);

#			/* Trace tab state changes */
#			g_signal_connect (tab,
#					  "notify::state",
#					  G_CALLBACK (tab_state_changed_while_saving),
#					  window);
#		}

#		gedit_window_set_active_tab (window, tab);
#		file_save_as (tab, window);
#	}
#}

def confirm_overwrite_callback(dialog, data):
	#	gedit_debug (DEBUG_COMMANDS);

	uri = dialog.get_uri();

	if is_read_only(uri):
		if replace_only_file(dialog, uri):
			res = gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME
		else:
			res = gtk.FILE_CHOOSER_CONFIRMATION_ACCEPT_FILENAME
	else:
		# fall back to the default confirmation dialog
		res = gtk.FILE_CHOOSER_CONFIRMATION_CONFIRM
	
	return res

def file_save_as(tab, window):
	uri_set = False

#	gedit_debug (DEBUG_COMMANDS);

	save_dialog = FileChooserDialog("Save As\342\200\246",
	                                window,
	                                gtk.FILE_CHOOSER_ACTION_SAVE,
	                                None,
	                                [[gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL],
	                                 [gtk.STOCK_SAVE, gtk.RESPONSE_OK]])

	save_dialog.set_do_overwrite_confirmation(True)

	save_dialog.connect("confirm-overwrite", confirm_overwrite_callback)
	
	wg = window.get_group()
	
	wg.add_window(save_dialog)
	save_dialog.set_modal(True)
	
	# Set the suggested file name
	doc = tab.get_document()
	uri = doc.get_uri()
	
	if uri and utils.uri_has_file_scheme():
		uri_set = save_dialog = set_uri(uri)
	
	if not uri_set:
		default_path = window.get_default_path()
		
		if default_path:
			save_dialog.set_current_folder_uri(default_path)
		
		docname = doc.get_short_name_for_display()
		save_dialog.set_current_name(docname)

	encoding = doc.get_encoding()
	
	save_dialog.set_encoding(encoding)

	save_dialog.set_data(TAB_TO_SAVE_AS, tab)
#	g_object_set_data (G_OBJECT (save_dialog),
#			   GEDIT_TAB_TO_SAVE_AS,
#			   tab);

	save_dialog.connect("response", save_dialog_response_cb, window)
	
	save_dialog.show()

def file_save(tab, window):
	doc = tab.get_document()
	
	if doc.is_untitled() or doc.get_readonly():
		file_save_as(tab, window)
		return
	
	
	uri_for_display = doc.get_uri_for_display()

	tab._save()

#void
#_gedit_cmd_file_save (GtkAction   *action,
#		     GeditWindow *window)
#{
#	GeditTab *tab;

#	gedit_debug (DEBUG_COMMANDS);

#	tab = gedit_window_get_active_tab (window);
#	if (tab == NULL)
#		return;

#	file_save (tab, window);
#}

def _file_save_as(action, window):
#	gedit_debug (DEBUG_COMMANDS);

	tab = window.get_active_tab()

	file_save_as(tab, window)

def _file_close_tab(tab, window):
	debug(DEBUG_COMMANDS)

	if window != tab.get_toplevel():
		return

	window.set_data(IS_CLOSING_ALL, False)
	window.set_data(IS_QUITTING, False)
	
	if tab._can_close():
		window.close_tab(tab)

def _file_close(action, window):
	debug(DEBUG_COMMANDS)

	active_tab = window.get_active_tab()
	if active_tab == None:
		return

	_file_close_tab(active_tab, window)

# Close all tabs
def file_close_all(window, is_quitting):
	debug(DEBUG_COMMANDS)

	if window.get_state() & (WINDOW_STATE_SAVING | WINDOW_STATE_PRINTING | WINDOW_STATE_SAVING_SESSION):
		return
		
	window.set_data(IS_CLOSING_ALL, True)
	window.set_data(IS_QUITTING, is_quitting)
			   
	unsaved_docs = window.get_unsaved_documents()

	if len(unsaved_docs) == 0:
		# There is no document to save -> close all tabs
		window.close_all_tabs()

		if is_quitting:
			window.destroy()
		
		return
	
	if len(unsaved_docs) == 1:
		# There is only one unsaved document

		doc = unsaved_docs[0]
		tab = tab_get_from_document(doc)
		if tab == None:
			return

		window.set_active_tab(tab)
		
		dlg = close_confirmation_dialog_new_single(window, doc, False)
	else:
		dlg = close_confirmation_dialog_new(window, unsaved_docs, False)

	dlg.connect("response", close_confirmation_dialog_response_handler, window)
	dlg.show()

def _file_quit(action, window):
	debug(DEBUG_COMMANDS)

	if window.get_state() & (WINDOW_STATE_SAVING | WINDOW_STATE_PRINTING | WINDOW_STATE_SAVING_SESSION):
		return

	file_close_all(window, True)

def _edit_undo(action, window):
	debug(DEBUG_COMMANDS)
	active_view = window.get_active_view()
	if warn_if_equal(active_view, None):
		return
	active_view.get_buffer().undo()
	active_view.scroll_to_cursor()
	active_view.grab_focus()

def _edit_redo(action, window):
	debug(DEBUG_COMMANDS)
	active_view = window.get_active_view()
	if active_view == None:
		return
	active_view.get_buffer().redo()
	active_view.scroll_to_cursor()
	active_view.grab_focus()

def _edit_cut(action, window):
	debug(DEBUG_COMMANDS)
	active_view = window.get_active_view()
	if warn_if_equal(active_view, None):
		return
	active_view.cut_clipboard()
	active_view.grab_focus()

def _edit_copy(action, window):
	debug(DEBUG_COMMANDS)
	active_view = window.get_active_view()
	if warn_if_equal(active_view, None):
		return
	active_view.copy_clipboard()
	active_view.grab_focus()

def _edit_paste(action, window):
	debug(DEBUG_COMMANDS)
	active_view = window.get_active_view()
	if warn_if_equal(active_view, None):
		return
	active_view.paste_clipboard()
	active_view.grab_focus()


def _edit_select_all(action, window):
	debug(DEBUG_COMMANDS)
	active_view = window.get_active_view()
	if warn_if_equal(active_view, None):
		return
	active_view.select_all()
	active_view.grab_focus()
