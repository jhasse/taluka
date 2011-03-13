#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Jan Niklas Hasse <jhasse@gmail.com>
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
import encoding

ALL_FILES = "All Files"
ALL_TEXT_FILES = "All Text Files"

class FileChooserDialog(gtk.FileChooserDialog):
	def __init__(self, title, parent, action, encoding, buttons):
		super(type(self), self).__init__(title, parent, action)

		self._title = title
		self._file_system_backen = None
		self._local_only = False
		self._action = action
		self._select_multiple = (action == gtk.FILE_CHOOSER_ACTION_OPEN)
		
		self.create_option_menu()
		
		self.connect("notify::action", self.action_changed)

		if encoding:
			self._option_menu.set_selected_encoding(encoding)

#	active_filter = gedit_prefs_manager_get_active_file_filter ();
#	gedit_debug_message (DEBUG_COMMANDS, "Active filter: %d", active_filter);

		filter = gtk.FileFilter()
		
		filter.set_name(ALL_FILES)
		filter.add_pattern("*")
		self.add_filter(filter)
		
		

#	if (active_filter != 1)
#	{
#		/* Make this filter the default */
#		gtk_file_chooser_set_filter (GTK_FILE_CHOOSER (result), filter);
#	}

		filter = gtk.FileFilter()
		filter.set_name(ALL_TEXT_FILES)
		filter.add_custom(gtk.FILE_FILTER_MIME_TYPE, all_text_files_filter)
		self.add_filter(filter)

#	if (active_filter == 1)
#	{
#		/* Make this filter the default */
#		gtk_file_chooser_set_filter (GTK_FILE_CHOOSER (result), filter);
#	}

		self.connect("notify::filter", self.filter_changed)

		self.set_transient_for(parent)
		self.set_destroy_with_parent(True)
		
		# buttons should be an array in the form: [[text, response_id],[text, response_id], ...]
		for button in buttons:
			text = button[0]
			response_id = button[1]
			
			self.add_button(text, response_id)
			
			if response_id == gtk.RESPONSE_OK or \
			response_id == gtk.RESPONSE_ACCEPT or \
			response_id == gtk.RESPONSE_YES or \
			response_id == gtk.RESPONSE_APPLY:
				self.set_default_response(response_id)

	def create_option_menu(self):
		pass
#static void
#create_option_menu (GeditFileChooserDialog *dialog)
#{
#	GtkWidget *hbox;
#	GtkWidget *label;
#	GtkWidget *menu;

#	hbox = gtk_hbox_new (FALSE, 6);

#	label = gtk_label_new_with_mnemonic (_("C_haracter Coding:"));
#	menu = gedit_encodings_option_menu_new (
#		gtk_file_chooser_get_action (GTK_FILE_CHOOSER (dialog)) == GTK_FILE_CHOOSER_ACTION_SAVE);

#	gtk_label_set_mnemonic_widget (GTK_LABEL (label), menu);
#	gtk_box_pack_start (GTK_BOX (hbox),
#			    label,
#			    FALSE,
#			    FALSE,
#			    0);

#	gtk_box_pack_end (GTK_BOX (hbox),
#			  menu,
#			  TRUE,
#			  TRUE,
#			  0);

#	gtk_file_chooser_set_extra_widget (GTK_FILE_CHOOSER (dialog),
#					   hbox);
#	gtk_widget_show_all (hbox);

#	dialog->priv->option_menu = menu;
#}
	
	def action_changed(self, pspec, data):
		action = self.get_action()
		
		if action == gtk.FILE_CHOOSER_ACTION_OPEN:
			self._option_menu.set_property("save_mode", False)
			self._option_menu.show()
		elif action == gtk.FILE_CHOOSER_ACTION_SAVE:
			self._option_menu.set_property("save_mode", True)
			self._option_menu.show()
		else:
			self._option_menu.hide()
	
	def filter_changed(self, pspec, data):
		id = 0

		# FIXME:
		#	if (!gedit_prefs_manager_active_file_filter_can_set ())
		#		return;
		
		filter = self.get_filter()
		name = filter.get_name()
		
		if not name:
			return
		
		if name == ALL_TEXT_FILES:
			id = 1

		#	gedit_debug_message (DEBUG_COMMANDS, "Active filter: %s (%d)", name, id);

		#	gedit_prefs_manager_set_active_file_filter (id);
	
	def get_encoding(self):
		#FIXME: Support other encodings than UTF-8
		return encoding.utf8_encoding

	def set_encoding(self, encoding):
		# TODO: Support other encodings than UTF-8
		return
#	g_return_if_fail (GEDIT_IS_FILE_CHOOSER_DIALOG (dialog));
#	g_return_if_fail (GEDIT_IS_ENCODINGS_OPTION_MENU (dialog->priv->option_menu));

#	gedit_encodings_option_menu_set_selected_encoding (
#				GEDIT_ENCODINGS_OPTION_MENU (dialog->priv->option_menu),
#				encoding);
#}

def all_text_files_filter(filter_info, data):
	return True # TODO: Implement me
	

#/* FIXME: use globs too - Paolo (Aug. 27, 2007) */
#static gboolean
#all_text_files_filter (const GtkFileFilterInfo *filter_info,
#		       gpointer                 data)
#{
#	static GSList *known_mime_types = NULL;
#	GSList *mime_types;

#	if (known_mime_types == NULL)
#	{
#		GtkSourceLanguageManager *lm;
#		const gchar * const *languages;

#		lm = gedit_get_language_manager ();
#		languages = gtk_source_language_manager_get_language_ids (lm);

#		while ((languages != NULL) && (*languages != NULL))
#		{
#			gchar **mime_types;
#			gint i;
#			GtkSourceLanguage *lang;

#			lang = gtk_source_language_manager_get_language (lm, *languages);
#			g_return_val_if_fail (GTK_IS_SOURCE_LANGUAGE (lang), FALSE);
#			++languages;

#			mime_types = gtk_source_language_get_mime_types (lang);
#			if (mime_types == NULL)
#				continue;

#			for (i = 0; mime_types[i] != NULL; i++)
#			{
#				GnomeVFSMimeEquivalence res;

#				res = gnome_vfs_mime_type_get_equivalence (mime_types[i],
#									   "text/plain");

#				if (res == GNOME_VFS_MIME_UNRELATED)
#				{
#					gedit_debug_message (DEBUG_COMMANDS,
#							     "Mime-type %s is not related to text/plain",
#							     mime_types[i]);

#					known_mime_types = g_slist_prepend (known_mime_types,
#									    g_strdup (mime_types[i]));
#				}
#			}

#			g_strfreev (mime_types);
#		}

#		/* known_mime_types always has "text/plain" as first item" */
#		known_mime_types = g_slist_prepend (known_mime_types, g_strdup ("text/plain"));
#	}

#	/* known mime_types contains "text/plain" and then the list of mime-types unrelated to "text/plain"
#	 * that gedit recognizes */

#	if (filter_info->mime_type == NULL)
#		return FALSE;

#	/*
#	 * The filter is matching:
#	 * - the mime-types beginning with "text/"
#	 * - the mime-types inheriting from a known mime-type (note the text/plain is
#	 *   the first known mime-type)
#	 */

#	if (strncmp (filter_info->mime_type, "text/", 5) == 0)
#		return TRUE;

#	mime_types = known_mime_types;
#	while (mime_types != NULL)
#	{
#		GnomeVFSMimeEquivalence res;
#		res = gnome_vfs_mime_type_get_equivalence (filter_info->mime_type,
#							   (const gchar*)mime_types->data);

#		if (res != GNOME_VFS_MIME_UNRELATED)
#			return TRUE;

#		mime_types = g_slist_next (mime_types);
#	}

#	return FALSE;
#}

#static void
#gedit_file_chooser_dialog_init (GeditFileChooserDialog *dialog)
#{
#	dialog->priv = GEDIT_FILE_CHOOSER_DIALOG_GET_PRIVATE (dialog);
#}

#static GtkWidget *
#gedit_file_chooser_dialog_new_valist (const gchar          *title,
#				      GtkWindow            *parent,
#				      GtkFileChooserAction  action,
#				      const GeditEncoding  *encoding,
#				      const gchar          *first_button_text,
#				      va_list               varargs)
#{
#	GtkWidget *result;
#	const char *button_text = first_button_text;
#	gint response_id;
#	GtkFileFilter *filter;
#	gint active_filter;

#	g_return_val_if_fail (parent != NULL, NULL);

#	result = g_object_new (GEDIT_TYPE_FILE_CHOOSER_DIALOG,
#			       "title", title,
#			       "file-system-backend", NULL,
#			       "local-only", FALSE,
#			       "action", action,
#			       "select-multiple", action == GTK_FILE_CHOOSER_ACTION_OPEN,
#			       NULL);

#	create_option_menu (GEDIT_FILE_CHOOSER_DIALOG (result));

#	g_signal_connect (result,
#			  "notify::action",
#			  G_CALLBACK (action_changed),
#			  NULL);

#	if (encoding != NULL)
#		gedit_encodings_option_menu_set_selected_encoding (
#				GEDIT_ENCODINGS_OPTION_MENU (GEDIT_FILE_CHOOSER_DIALOG (result)->priv->option_menu),
#				encoding);

#	active_filter = gedit_prefs_manager_get_active_file_filter ();
#	gedit_debug_message (DEBUG_COMMANDS, "Active filter: %d", active_filter);

#	/* Filters */
#	filter = gtk_file_filter_new ();

#	gtk_file_filter_set_name (filter, ALL_FILES);
#	gtk_file_filter_add_pattern (filter, "*");
#	gtk_file_chooser_add_filter (GTK_FILE_CHOOSER (result), filter);

#	if (active_filter != 1)
#	{
#		/* Make this filter the default */
#		gtk_file_chooser_set_filter (GTK_FILE_CHOOSER (result), filter);
#	}

#	filter = gtk_file_filter_new ();
#	gtk_file_filter_set_name (filter, ALL_TEXT_FILES);
#	gtk_file_filter_add_custom (filter,
#				    GTK_FILE_FILTER_MIME_TYPE,
#				    all_text_files_filter,
#				    NULL,
#				    NULL);
#	gtk_file_chooser_add_filter (GTK_FILE_CHOOSER (result), filter);

#	if (active_filter == 1)
#	{
#		/* Make this filter the default */
#		gtk_file_chooser_set_filter (GTK_FILE_CHOOSER (result), filter);
#	}

#	g_signal_connect (result,
#			  "notify::filter",
#			  G_CALLBACK (filter_changed),
#			  NULL);

#	gtk_window_set_transient_for (GTK_WINDOW (result), parent);
#	gtk_window_set_destroy_with_parent (GTK_WINDOW (result), TRUE);

#	while (button_text)
#	{
#		response_id = va_arg (varargs, gint);

#		gtk_dialog_add_button (GTK_DIALOG (result), button_text, response_id);
#		if ((response_id == GTK_RESPONSE_OK) ||
#		    (response_id == GTK_RESPONSE_ACCEPT) ||
#		    (response_id == GTK_RESPONSE_YES) ||
#		    (response_id == GTK_RESPONSE_APPLY))
#			gtk_dialog_set_default_response (GTK_DIALOG (result), response_id);

#		button_text = va_arg (varargs, const gchar *);
#	}

#	return result;
#}

#/**
# * gedit_file_chooser_dialog_new:
# * @title: Title of the dialog, or %NULL
# * @parent: Transient parent of the dialog, or %NULL
# * @action: Open or save mode for the dialog
# * @first_button_text: stock ID or text to go in the first button, or %NULL
# * @Varargs: response ID for the first button, then additional (button, id) pairs, ending with %NULL
# *
# * Creates a new #GeditFileChooserDialog.  This function is analogous to
# * gtk_dialog_new_with_buttons().
# *
# * Return value: a new #GeditFileChooserDialog
# *
# **/
#GtkWidget *
#gedit_file_chooser_dialog_new (const gchar          *title,
#			       GtkWindow            *parent,
#			       GtkFileChooserAction  action,
#			       const GeditEncoding  *encoding,
#			       const gchar          *first_button_text,
#			       ...)
#{
#	GtkWidget *result;
#	va_list varargs;

#	va_start (varargs, first_button_text);
#	result = gedit_file_chooser_dialog_new_valist (title, parent, action,
#						       encoding, first_button_text,
#						       varargs);
#	va_end (varargs);

#	return result;
#}

#const GeditEncoding *
#gedit_file_chooser_dialog_get_encoding (GeditFileChooserDialog *dialog)
#{
#	g_return_val_if_fail (GEDIT_IS_FILE_CHOOSER_DIALOG (dialog), NULL);
#	g_return_val_if_fail (GEDIT_IS_ENCODINGS_OPTION_MENU (dialog->priv->option_menu), NULL);
#	g_return_val_if_fail ((gtk_file_chooser_get_action (GTK_FILE_CHOOSER (dialog)) == GTK_FILE_CHOOSER_ACTION_OPEN ||
#			       gtk_file_chooser_get_action (GTK_FILE_CHOOSER (dialog)) == GTK_FILE_CHOOSER_ACTION_SAVE), NULL);

#	return gedit_encodings_option_menu_get_selected_encoding (
#				GEDIT_ENCODINGS_OPTION_MENU (dialog->priv->option_menu));
#}
