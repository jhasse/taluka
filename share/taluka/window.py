#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007-2011 Jan Niklas Hasse <jhasse@gmail.com>
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
import gtk.glade
import os
import reloc
import project
import urllib
import commands
from gettext import gettext as _
from newproject import *
from panel import *
from gnome import url_show
from tab import *
from notebook import Notebook
from debug import *
from app import *
from debug import *
from ui import *
from prefs_manager import *

def _(s):
	return s #FIXME: use gettext

PROGRAM_NAME = "Taluka IDE"
PROGRAM_VERSION = "0.1"

TARGET_URI_LIST = 100

class Window(gtk.Window):
	__gsignals__ = { 'active_tab_changed' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (Tab,)) }

	def __init__(self):
		super(type(self), self).__init__()
		debug(DEBUG_WINDOW)

		self._active_tab = None
		self._num_tabs = 0
		self._removing_tabs = False
		self._state = WINDOW_STATE_NORMAL
		self._dispose_has_run = False
		self._fullscreen_controls = None
		self._fullscreen_animation_timeout_id = 0

		#TODO
		#self._message_bus = MessageBus()

		self._window_group = gtk.WindowGroup()
		self._window_group.add_window(self)

		main_box = gtk.VBox(False, 0)
		self.add(main_box)
		main_box.show()

		# Add menu bar and toolbar bar
		self.create_menu_bar_and_toolbar(main_box)

		# Add status bar
		self.create_statusbar(main_box)

		# Add the main area
		debug_message(DEBUG_WINDOW, "Add main area")
		self._hpaned = gtk.HPaned()
		main_box.pack_start(self._hpaned, True, True, 0)

		self._vpaned = gtk.VPaned()
		self._hpaned.pack2(self._vpaned, True, False)
		
		debug_message(DEBUG_WINDOW, "Create taluka notebook")
		self._notebook = Notebook()
		self.add_notebook(self._notebook)

		# side and bottom panels
	  	self.create_side_panel()
		self.create_bottom_panel()

		# panes' state must be restored after panels have been mapped,
		# since the bottom pane position depends on the size of the vpaned.
		self._side_panel_size = prefs_manager_get_side_panel_size()
		self._bottom_panel_size = prefs_manager_get_bottom_panel_size()

		self._hpaned.connect_after("map", self.hpaned_restore_position)
		self._vpaned.connect_after("map", self.vpaned_restore_position)

		self._hpaned.show()
		self._vpaned.show()

		# Drag and drop support, set targets to None because we add the
		# default uri_targets below
		self.drag_dest_set(gtk.DEST_DEFAULT_MOTION | gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP, (), gtk.gdk.ACTION_COPY)

		# Add uri targets
		tl = self.drag_dest_get_target_list()
	
		if tl == None:
			tl = ()
			self.drag_dest_set_target_list(tl)

		tl += (TARGET_URI_LIST,)

		# connect instead of override, so that we can
		# share the cb code with the view TODO
#		self.connect("drag_data_received", drag_data_received_cb)

		# we can get the clipboard only after the widget
		# is realized TODO
#		self.connect("realize", window_realized)
#		self.connect("unrealize", window_unrealized)

		# Check if the window is active for fullscreen TODO
#		self.connect("notify::is-active", check_window_is_active)

		debug_message(DEBUG_WINDOW, "Update plugins ui")
	
#		plugins_engine_get_default().activate_plugins(self) TODO

		# set visibility of panes.
		# This needs to be done after plugins activatation TODO
#		self.init_panels_visibility()

#		self.update_sensitivity_according_to_open_tabs() TODO

		debug_message(DEBUG_WINDOW, "END")
		
#		self._action_group = gtk.ActionGroup("ExamplePyPluginActions")
#		self._action_group.add_actions(
#		                               [
#		                                ("File", None, "File", None, None, None),
#		                                ("FileNew", gtk.STOCK_NEW, None, None, None, commands._file_new),
#		                                ("FileOpen", gtk.STOCK_OPEN, None, None, None, commands._file_open),
#		                                ("FileSave", gtk.STOCK_SAVE, None, None, None, commands._file_save),
#		                                ("FileSaveAs", gtk.STOCK_SAVE_AS, None, "<shift><control>S",
#		                                 "Save the current file with a different name", commands._file_save_as),
#		                                ("FileClose", gtk.STOCK_CLOSE, None, None, None, commands._file_close),
#		                                ("FileQuit", gtk.STOCK_QUIT, None, None, None, commands._file_quit),
#		                                ("Edit", None, "Edit", None, None, None),
#		                                ("EditUndo", gtk.STOCK_UNDO, None, "<control>Z", None, commands._edit_undo),
#		                                ("EditRedo", gtk.STOCK_REDO, None, "<shift><control>Z", None, commands._edit_redo),
#		                                ("EditCut", gtk.STOCK_CUT, None, None, None, commands._edit_cut),
#		                                ("EditCopy", gtk.STOCK_COPY, None, None, None, commands._edit_copy),
#		                                ("EditPaste", gtk.STOCK_PASTE, None, None, None, commands._edit_paste),
#		                                ("EditSelectAll", gtk.STOCK_SELECT_ALL, None, None, None, commands._edit_select_all)
#		                               ],
#		                               self
#		                              )
#		
#		self._ui_manager = gtk.UIManager()
#		self._ui_manager.add_ui_from_file(os.path.join(reloc.DATADIR, 'taluka/taluka-ui.xml'))
#		self._ui_manager.insert_action_group(self._action_group, -1)
#		
#		vbox = gtk.VBox()
#		
#		self._menubar = self._ui_manager.get_widget("/MenuBar")
#		vbox.pack_start(self._menubar, expand=False)
#		
#		self._toolbar = self._ui_manager.get_widget("/ToolBar")
#		assert self._toolbar != None
#		vbox.pack_start(self._toolbar, expand=False)
#		
#		hpaned = gtk.HPaned()
#		
#		self._side_panel = Panel()
#		hpaned.pack1(self._side_panel, False, False)
#		
#		vpaned = gtk.VPaned()
#		self._notebook = Notebook()
#		vpaned.pack1(self._notebook, True, False)
#		
#		self._bottom_panel = Panel()
#		vpaned.pack2(self._bottom_panel, False, False)
#		
#		hpaned.pack2(vpaned, True, False)
#		
#		vbox.add(hpaned)
#		
#		self.add(vbox)
#		
#		self.connect("delete_event", self.on_delete_event)
#		self.connect("destroy", self.on_destroy)
#		self.show_all()
#		
#		#	static gboolean is_first = True;
#		#	GtkWidget *main_box;
#		#	GtkTargetList *tl;

#		debug(DEBUG_WINDOW)

#		#	window->priv = GEDIT_WINDOW_GET_PRIVATE (window);
#		
#		self._active_tab = None
#		
#		#	self._num_tabs = 0;
#		#	self._removing_tabs = FALSE;
#		self._state = WINDOW_STATE_NORMAL;
#		#	self._destroy_has_run = FALSE;

#		self._window_group = gtk.WindowGroup()
#		self._window_group.add_window(self)

#		#	main_box = gtk_vbox_new (FALSE, 0);
#		#	gtk_container_add (GTK_CONTAINER (window), main_box);
#		#	gtk_widget_show (main_box);

#		#	/* Add menu bar and toolbar bar */
#		#	create_menu_bar_and_toolbar (window, main_box);

#		#	/* Add status bar */
#		#	create_statusbar (window, main_box);

#		#	/* Add the main area */
#		#	gedit_debug_message (DEBUG_WINDOW, "Add main area");		
#		#	self._hpaned = gtk_hpaned_new ();
#		#  	gtk_box_pack_start (GTK_BOX (main_box), 
#		#  			    self._hpaned, 
#		#  			    True, 
#		#  			    True, 
#		#  			    0);

#		#	self._vpaned = gtk_vpaned_new ();
#		#  	gtk_paned_pack2 (GTK_PANED (self._hpaned), 
#		#  			 self._vpaned, 
#		#  			 True, 
#		#  			 FALSE);
#		#  	
#		#	gedit_debug_message (DEBUG_WINDOW, "Create gedit notebook");
#		#	self._notebook = gedit_notebook_new ();
#		#  	gtk_paned_pack1 (GTK_PANED (self._vpaned), 
#		#  			 self._notebook,
#		#  			 True, 
#		#  			 True);
#		#  	gtk_widget_show (self._notebook);  			 

#		#	/* side and bottom panels */
#		#  	create_side_panel (window);
#		#	create_bottom_panel (window);

#		#	/* restore paned positions as soon as we know the panes allocation.
#		#	 * This needs to be done only for the first window, the successive
#		#	 * windows are created by cloning the first one */
#		#	if (is_first)
#		#	{
#		#		is_first = FALSE;

#		#		self._side_panel_size = gedit_prefs_manager_get_side_panel_size ();
#		#		self._bottom_panel_size = gedit_prefs_manager_get_bottom_panel_size ();
#		#		g_signal_connect_after (self._hpaned,
#		#					"map",
#		#					G_CALLBACK (hpaned_restore_position),
#		#					window);
#		#		g_signal_connect_after (self._vpaned,
#		#					"map",
#		#					G_CALLBACK (vpaned_restore_position),
#		#					window);
#		#	}

#		#	gtk_widget_show (self._hpaned);
#		#	gtk_widget_show (self._vpaned);

#		#	/* Drag and drop support, set targets to NULL because we add the
#		#	   default uri_targets below */
#		#	gtk_drag_dest_set (GTK_WIDGET (window),
#		#			   GTK_DEST_DEFAULT_MOTION |
#		#			   GTK_DEST_DEFAULT_HIGHLIGHT |
#		#			   GTK_DEST_DEFAULT_DROP,
#		#			   NULL,
#		#			   0,
#		#			   GDK_ACTION_COPY);

#		#	/* Add uri targets */
#		#	tl = gtk_drag_dest_get_target_list (GTK_WIDGET (window));
#		#	
#		#	if (tl == NULL)
#		#	{
#		#		tl = gtk_target_list_new (NULL, 0);
#		#		gtk_drag_dest_set_target_list (GTK_WIDGET (window), tl);
#		#		gtk_target_list_unref (tl);
#		#	}
#		#	
#		#	gtk_target_list_add_uri_targets (tl, TARGET_URI_LIST);

#		# Connect signals
#		self._notebook.connect("switch_page", notebook_switch_page, self)
#		
#		#	g_signal_connect (self._notebook,
#		#			  "tab_added",
#		#			  G_CALLBACK (notebook_tab_added),
#		#			  window);
#		#	g_signal_connect (self._notebook,
#		#			  "tab_removed",
#		#			  G_CALLBACK (notebook_tab_removed),
#		#			  window);
#		#	g_signal_connect (self._notebook,
#		#			  "tabs_reordered",
#		#			  G_CALLBACK (notebook_tabs_reordered),
#		#			  window);			  
#		#	g_signal_connect (self._notebook,
#		#			  "tab_detached",
#		#			  G_CALLBACK (notebook_tab_detached),
#		#			  window);
#		#	g_signal_connect (self._notebook,
#		#			  "tab_close_request",
#		#			  G_CALLBACK (notebook_tab_close_request),
#		#			  window);
#		#	g_signal_connect (self._notebook,
#		#			  "button-press-event",
#		#			  G_CALLBACK (notebook_button_press_event),
#		#			  window);
#		#	g_signal_connect (self._notebook,
#		#			  "popup-menu",
#		#			  G_CALLBACK (notebook_popup_menu),
#		#			  window);

#		#	/* connect instead of override, so that we can
#		#	 * share the cb code with the view */
#		#	g_signal_connect (window,
#		#			  "drag_data_received",
#		#	                  G_CALLBACK (drag_data_received_cb), 
#		#	                  None)

#		#	/* we can get the clipboard only after the widget
#		#	 * is realized */
#		#	g_signal_connect (window,
#		#			  "realize",
#		#			  G_CALLBACK (window_realized),
#		#			  None)
#		#	g_signal_connect (window,
#		#			  "unrealize",
#		#			  G_CALLBACK (window_unrealized),
#		#			  None)

#		#	gedit_debug_message (DEBUG_WINDOW, "Update plugins ui");
#		#	gedit_plugins_engine_update_plugins_ui (gedit_plugins_engine_get_default (),
#		#						window, True);

#		#	/* set visibility of panes.
#		#	 * This needs to be done after plugins activatation */
#		#	init_panels_visibility (window);

#		#	gedit_debug_message (DEBUG_WINDOW, "END");
#		self.create_tab(True)

		self.show() # FIXME: Remove this file and use something like gedit-session.c instead.

	def add_notebook(self, notebook):
		self._vpaned.pack1(notebook, True, True)
		notebook.show()
		self.connect_notebook_signals(notebook)

	def	init_panels_visibility(self):
		debug(DEBUG_WINDOW)

		# side pane
		active_page = prefs_manager_get_side_panel_active_page()
		self._side_panel._set_active_item_by_id(active_page)

		if prefs_manager_get_side_pane_visible():
			self._side_panel.show()

#TODO:
#		/* bottom pane, it can be empty */
#		if (gedit_panel_get_n_items (GEDIT_PANEL (window->priv->bottom_panel)) > 0)
#		{
#			active_page = gedit_prefs_manager_get_bottom_panel_active_page ();
#			_gedit_panel_set_active_item_by_id (GEDIT_PANEL (window->priv->bottom_panel),
#								active_page);

#			if (gedit_prefs_manager_get_bottom_panel_visible ())
#			{
#				gtk_widget_show (window->priv->bottom_panel);
#			}
#		}
#		else
#		{
#			GtkAction *action;
#			action = gtk_action_group_get_action (window->priv->panes_action_group,
#								  "ViewBottomPane");
#			gtk_action_set_sensitive (action, FALSE);
#		}

#		/* start track sensitivity after the initial state is set */
#		window->priv->bottom_panel_item_removed_handler_id =
#			g_signal_connect (window->priv->bottom_panel,
#					  "item_removed",
#					  G_CALLBACK (bottom_panel_item_removed),
#					  window);

#		g_signal_connect (window->priv->bottom_panel,
#				  "item_added",
#				  G_CALLBACK (bottom_panel_item_added),
#				  window);
#	}

	def on_delete_event(self, widget, event, data=None):
		return False

	def create_tab(self, jump_to):
		tab = Tab()
		tab.show()
		self._notebook.add_tab(tab, -1, jump_to)
		return tab

	def create_tab_from_uri(self, uri, encoding, line_pos, create, jump_to):
		if uri == None:
			return None
		
		tab = tab_new_from_uri(uri, encoding, line_pos, create)
		if tab == None:
			return None

		tab.show()

		self._notebook.add_tab(tab, -1, jump_to)
		
		return tab
	
	def close_tab(self, tab):
		if tab.get_state() == TAB_STATE_SAVING or tab.get_state() == TAB_STATE_SHOWING_PRINT_PREVIEW:
			return
		self._notebook.remove_tab(tab)

	def close_all_tabs(self):
		if self._state & WINDOW_STATE_SAVING or self._state & WINDOW_STATE_SAVING_SESSION:
			return
		self._removing_tabs = True
		self._notebook.remove_all_tabs()
		self._removing_tabs = False

	def get_active_tab(self):
		return self._active_tab

	def get_documents(self):
		documents = []
		for i in range(self._notebook.get_n_pages()):
			documents.append(self._notebook.get_nth_page(i))
		return documents
	
	def get_unsaved_documents(self):
		unsaved_docs = []
		tabs = self._notebook.get_children()
		for tab in tabs:
			if not tab._can_close():
				unsaved_docs.append(tab.get_document())
		return unsaved_docs
	
	def get_views(self):
		return None
	
	def get_group(self):
		return self._window_group
	
	def get_side_panel(self):
		return self._side_panel
	
	def get_bottom_panel(self):
		return self._bottom_panel
	
	def get_statusbar(self):
		return self._statusbar
	
	def get_ui_manager(self):
		return self._ui_manager
	
	def get_state(self):
		return self._state
	
	def get_tab_from_uri(self, uri):
		return None
		
	def on_destroy(self, widget):
		gtk.main_quit()
	
	def on_about(self, data):
		self.abt.show_all()
		self.abt.run()
		self.abt.hide_all()
	
	def on_build_activate(self, data):
		pass
		
	def on_file_open(self, data):
		filechooser = gtk.FileChooserDialog(title="Choose File", action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		filechooser.set_transient_for(self)
		response = filechooser.run()
		if response == gtk.RESPONSE_OK:
			file = filechooser.get_filename()
		else:
			file = None
		filechooser.destroy()
		
		if file != None:
			self.create_tab_from_uri(urllib.unquote(file), None, 0, False, True)

	def on_new_project(self, widget):
		self.newproject = NewProject(self)
	
	def on_open_project(self, widget):
		filechooser = gtk.FileChooserDialog(title="Choose Project File", action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		filter = gtk.FileFilter()
		filter.set_name("Taluka Project Files")
		filter.add_pattern("*.taluka")
		filechooser.add_filter(filter)
		filter = gtk.FileFilter()
		filter.set_name("All Files")
		filter.add_pattern("*")
		filechooser.add_filter(filter)

		filechooser.set_current_folder(os.environ["HOME"])

		filechooser.set_transient_for(self.window)
		
		response = filechooser.run()
		if response == gtk.RESPONSE_OK:
			file = filechooser.get_filename()
		else:
			file = None
		filechooser.destroy()
		
		if file != None:
			p = project.Project(self)
			p.filename = urllib.unquote(file)
			p.open()
	
	def on_save_project(self, widget):
		self.active_project.save()
	
	def on_save_file(self, data):
		self.get_current_file().save()

	def on_close_file(self, data):
		if self.get_current_file().can_close():
			self.get_current_file().close()
	
	def get_current_file(self):
		return self._notebook.get_nth_page(self._notebook.get_current_page())

	def get_current_scrolledwindow(self):
		return self.get_current_file()
		
	def get_bottom_notebook(self):
		return self.glade.get_widget('notebook3')
	
	def get_active_document(self):
		self._notebook.get_current_page()
	
	def get_bottom_panel(self):
		return self._bottom_panel

	def on_cut(self, widget):
		buffer = self.get_current_scrolledwindow().get_child().get_buffer()
		if buffer != None:
			buffer.cut_clipboard(gtk.Clipboard(), True)

	def on_copy(self, widget):
		buffer = self.get_current_scrolledwindow().get_child().get_buffer()
		if buffer != None:
			buffer.copy_clipboard(gtk.Clipboard())

	def on_paste(self, widget):
		buffer = self.get_current_scrolledwindow().get_child().get_buffer()
		if buffer != None:
			buffer.paste_clipboard(gtk.Clipboard(), None, True)
	
	def get_default_path(self):
		return "/home/jhasse" # FIXME: Don't use this path!
	
	def file_save(self, tab, window):
		assert tab != None
		assert window != None

		doc = tab.get_document()
		assert doc != None

		if doc.is_untitled() or doc.get_readonly():
			self.file_save_as(tab, window)
			return
		
		uri_for_display = doc.get_uri_for_display()
		
		self._statusbar.flash_message(self._generic_message_cid, "Saving file '%s'\342\200\246" % uri_for_display)
		
		tab.save()
			

# 		gtk.window_set_default_icon_from_file(os.path.join(reloc.DATADIR, 'pixmaps/taluka.png'))
# 		self.glade = gtk.glade.XML(os.path.join(reloc.DATADIR, 'taluka/main.glade'))
# 		self.glade.signal_autoconnect(self)
# 		self.window = self.glade.get_widget('window1')
# 		self._notebook = self.glade.get_widget('notebook_files')
# 		assert self._notebook != None
# 		
# 		self.abt = gtk.AboutDialog()

# 		self.abt.set_name(PROGRAM_NAME)
# 		self.abt.set_version(PROGRAM_VERSION)
# 		self.abt.set_comments("Taluka is a simple C/C++/Python IDE written in PyGTK.")
# 		self.abt.set_authors(["Jan Niklas Hasse <jhasse@gmail.com>", "Jannes Meyer <jannes.meyer@gmail.com>", "Fabian Franzen <flammenvogel@arcor.de>"])
# 		self.abt.set_copyright("Copyright © 2007 watteimdocht.de")
# 		gtk.about_dialog_set_url_hook(lambda dialog, url: url_show(url))
# 		gtk.about_dialog_set_email_hook(lambda dialog, email: url_show('mailto:'+email))
# 		self.abt.set_website("http://www.watteimdocht.de/index_Taluka.php")
# 		self.abt.set_website_label("Taluka Homepage")
# 		
# 		self.manager = project.Manager(self)
# 		
# 		self.active_project = None
# 		
# 		start_here = self.glade.get_widget("start_tab_event") # TODO: Don't use a EventBox
# 		# geht nicht: start_here.set_events(gtk.gdk.BUTTON_PRESS_MASK)
# 		start_here.connect("button-press-event", self.on_tab_click, 0)
# 		
# 		self._bottom_panel = Panel(self)
# 	
# 	def on_tab_click(self, widget, event, tab_index):
# 		if event.button == 2:
# 			self._notebook.remove_page(tab_index)
# 		elif event.button == 3:
# 			print "Kontextmenü"
	def set_title(self):
		# TODO: This function may be improved. Should display project name
		
		if self._active_tab == None:
			super(type(self), self).set_title("Taluka IDE")
			return
			
		doc = self._active_tab.get_document()
		
		name = doc.get_short_name_for_display()
		
		super(type(self), self).set_title("%s - Taluka IDE" % name)

	def get_active_view(self):
		if self._active_tab == None:
			return None
		return self._active_tab.get_view()

	def set_active_tab(self, tab):
		page_num = self._notebook.page_num(tab)
		if page_num == -1:
			return
		self._notebook.set_current_page(page_num)
	
	def update_recent_files_menu(self): # TODO
		pass

	def set_sensitivity_according_to_tab(self, tab):
		# TODO: Implement all of this
		
		debug(DEBUG_WINDOW)

		lockdown = app_get_default().get_lockdown()

#		state = gedit_tab_get_state (tab);
#		state_normal = (state == GEDIT_TAB_STATE_NORMAL);

#		view = gedit_tab_get_view (tab);
#		editable = gtk_text_view_get_editable (GTK_TEXT_VIEW (view));

#		doc = GEDIT_DOCUMENT (gtk_text_view_get_buffer (GTK_TEXT_VIEW (view)));

#		clipboard = gtk_widget_get_clipboard (GTK_WIDGET (window),
#							  GDK_SELECTION_CLIPBOARD);

#		action = gtk_action_group_get_action (self._action_group,
#							  "FileSave");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   (state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION) ||
#					   (state == GEDIT_TAB_STATE_SHOWING_PRINT_PREVIEW)) &&
#					  !gedit_document_get_readonly (doc) &&
#					  !(lockdown & GEDIT_LOCKDOWN_SAVE_TO_DISK));

#		action = gtk_action_group_get_action (self._action_group,
#							  "FileSaveAs");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   (state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION) ||
#					   (state == GEDIT_TAB_STATE_SHOWING_PRINT_PREVIEW)) &&
#					  !(lockdown & GEDIT_LOCKDOWN_SAVE_TO_DISK));

#		action = gtk_action_group_get_action (self._action_group,
#							  "FileRevert");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   (state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION)) &&
#					  !gedit_document_is_untitled (doc));

#		action = gtk_action_group_get_action (self._action_group,
#							  "FilePrintPreview");
#		gtk_action_set_sensitive (action,
#					  state_normal &&
#					  !(lockdown & GEDIT_LOCKDOWN_PRINTING));

#		action = gtk_action_group_get_action (self._action_group,
#							  "FilePrint");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					  (state == GEDIT_TAB_STATE_SHOWING_PRINT_PREVIEW)) &&
#					  !(lockdown & GEDIT_LOCKDOWN_PRINTING));
#					  
#		action = gtk_action_group_get_action (self._action_group,
#							  "FileClose");

#		gtk_action_set_sensitive (action,
#					  (state != GEDIT_TAB_STATE_CLOSING) &&
#					  (state != GEDIT_TAB_STATE_SAVING) &&
#					  (state != GEDIT_TAB_STATE_SHOWING_PRINT_PREVIEW) &&
#					  (state != GEDIT_TAB_STATE_PRINTING) &&
#					  (state != GEDIT_TAB_STATE_PRINT_PREVIEWING) &&
#					  (state != GEDIT_TAB_STATE_SAVING_ERROR));

#		action = gtk_action_group_get_action (self._action_group,
#							  "EditUndo");
#		gtk_action_set_sensitive (action, 
#					  state_normal &&
#					  gtk_source_buffer_can_undo (GTK_SOURCE_BUFFER (doc)));

#		action = gtk_action_group_get_action (self._action_group,
#							  "EditRedo");
#		gtk_action_set_sensitive (action, 
#					  state_normal &&
#					  gtk_source_buffer_can_redo (GTK_SOURCE_BUFFER (doc)));

#		action = gtk_action_group_get_action (self._action_group,
#							  "EditCut");
#		gtk_action_set_sensitive (action,
#					  state_normal &&
#					  editable &&
#					  gtk_text_buffer_get_has_selection (GTK_TEXT_BUFFER (doc)));

#		action = gtk_action_group_get_action (self._action_group,
#							  "EditCopy");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION) &&
#					  gtk_text_buffer_get_has_selection (GTK_TEXT_BUFFER (doc)));
#					  
#		action = gtk_action_group_get_action (self._action_group,
#							  "EditPaste");
#		if (state_normal && editable)
#		{
#			set_paste_sensitivity_according_to_clipboard (window,
#									  clipboard);
#		}
#		else
#		{
#			gtk_action_set_sensitive (action, FALSE);
#		}

#		action = gtk_action_group_get_action (self._action_group,
#							  "EditDelete");
#		gtk_action_set_sensitive (action,
#					  state_normal &&
#					  editable &&
#					  gtk_text_buffer_get_has_selection (GTK_TEXT_BUFFER (doc)));

#		action = gtk_action_group_get_action (self._action_group,
#							  "SearchFind");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION));

#		action = gtk_action_group_get_action (self._action_group,
#							  "SearchIncrementalSearch");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION));

#		action = gtk_action_group_get_action (self._action_group,
#							  "SearchReplace");
#		gtk_action_set_sensitive (action,
#					  state_normal &&
#					  editable);

#		b = gedit_document_get_can_search_again (doc);
#		action = gtk_action_group_get_action (self._action_group,
#							  "SearchFindNext");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION) && b);

#		action = gtk_action_group_get_action (self._action_group,
#							  "SearchFindPrevious");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION) && b);

#		action = gtk_action_group_get_action (self._action_group,
#							  "SearchClearHighlight");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION) && b);

#		action = gtk_action_group_get_action (self._action_group,
#							  "SearchGoToLine");
#		gtk_action_set_sensitive (action,
#					  (state_normal ||
#					   state == GEDIT_TAB_STATE_EXTERNALLY_MODIFIED_NOTIFICATION));
#	
#		action = gtk_action_group_get_action (self._action_group,
#							  "ViewHighlightMode");
#		gtk_action_set_sensitive (action, 
#					  (state != GEDIT_TAB_STATE_CLOSING) &&
#					  gedit_prefs_manager_get_enable_syntax_highlighting ());

#		update_next_prev_doc_sensitivity (window, tab);

#		gedit_plugins_engine_update_plugins_ui (gedit_plugins_engine_get_default (),
#							window, FALSE);
#	}

	def create_languages_menu(self): # TODO
		pass
	
	def set_toolbar_style(self, x):
		pass # TODO: Implement this
	
	def setup_toolbar_open_button(self, toolbar):
		pass # TODO: Implement this
	
	def toolbar_visibility_changed(self):
		pass # TODO: Implement this
	
	def create_statusbar(self, main_box):
		pass # TODO: Implement this
	
	def hpaned_restore_position(self):
		pass # TODO: Implement this
	
	def vpaned_restore_position(self):
		pass # TODO: Implement this

	def create_menu_bar_and_toolbar(self, main_box):
		debug(DEBUG_WINDOW)

		manager = gtk.UIManager()
		self._manager = manager

		self.add_accel_group(manager.get_accel_group())

		action_group = gtk.ActionGroup("TalukaWindowAlwaysSensitiveActions")
		action_group.set_translation_domain("") # TODO: Should it be NULL instead of ""?
		action_group.add_actions(always_sensitive_menu_entries, self)
		action_group.add_toggle_actions(always_sensitive_toggle_menu_entries, self)

		manager.insert_action_group(action_group, 0)
		#g_object_unref (action_group); FIXME: Do i need this?
		self._always_sensitive_action_group = action_group

		action_group = gtk.ActionGroup("TalukaWindowActions")
		action_group.set_translation_domain("") # TODO: Should it be NULL instead of ""?
		action_group.add_actions(menu_entries, self)
		manager.insert_action_group(action_group, 0)
		#g_object_unref (action_group); FIXME see above
		self._action_group = action_group

		# set short labels to use in the toolbar
		action = action_group.get_action("FileSave")
		action.set_property("short_label", _("Save"))
#		action = action_group.get_action("FilePrint") TODO Don't forget to uncomment these lines
#		action.set_property("short_label", _("Print"))
#		action = action_group.get_action("SearchFind")
#		action.set_property("short_label", _("Find"))
#		action = action_group.get_action("SearchReplace")
#		action.set_property("short_label", _("Replace"))

		# set which actions should have priority on the toolbar
		action = action_group.get_action("FileSave")
		action.set_property("is_important", True)
		action = action_group.get_action("EditUndo")
		action.set_property("is_important", True)

		action_group = gtk.ActionGroup("TalukaQuitWindowActions")
		action_group.set_translation_domain("") # TODO: Should it be NULL instead of ""?
		action_group.add_actions(quit_menu_entries, self)

		manager.insert_action_group(action_group, 0)
		#g_object_unref (action_group); FIXME: see above
		self._quit_action_group = action_group

		action_group = gtk.ActionGroup("TalukaCloseWindowActions")
		action_group.set_translation_domain("") # TODO: Should it be NULL instead of ""?
		action_group.add_actions(close_menu_entries, self)

		manager.insert_action_group(action_group, 0)
		#g_object_unref (action_group); FIXME
		self._close_action_group = action_group

		action_group = gtk.ActionGroup("TalukaWindowPanesActions")
		action_group.set_translation_domain("") # TODO: Should it be NULL instead of ""?
		action_group.add_toggle_actions(panes_toggle_menu_entries, self)

		manager.insert_action_group(action_group, 0)
		#g_object_unref (action_group); FIXME
		self._panes_action_group = action_group

		# now load the UI definition
		ui_file = os.path.join(reloc.DATADIR, 'taluka/taluka-ui.xml')
		manager.add_ui_from_file(ui_file)

		# show tooltips in the statusbar
		manager.connect("connect_proxy", connect_proxy_cb, self)
		manager.connect("disconnect_proxy", disconnect_proxy_cb, self)

		# recent files menu
		action_group = gtk.ActionGroup("RecentFilesActions")
		action_group.set_translation_domain("") # TODO: Should it be NULL instead of ""?
		self._recents_action_group = action_group
		manager.insert_action_group(action_group, 0)
		#g_object_unref (action_group); FIXME see above

		recent_manager = gtk.recent_manager_get_default()
		self._recents_handler_id = recent_manager.connect("changed", recent_manager_changed, self)
		self.update_recent_files_menu()

		# languages menu
		action_group = gtk.ActionGroup("LanguagesActions")
		action_group.set_translation_domain("") # TODO: Should it be NULL instead of ""?
		self._languages_action_group = action_group
		manager.insert_action_group(action_group, 0)
		self.create_languages_menu()

		# list of open documents menu
		action_group = gtk.ActionGroup("DocumentsListActions")
		action_group.set_translation_domain("") # TODO: Should it be NULL instead of ""?
		self._documents_list_action_group = action_group
		manager.insert_action_group(action_group, 0)

		self._menubar = manager.get_widget("/MenuBar")
		main_box.pack_start(self._menubar, False, False, 0)

		self._toolbar = manager.get_widget("/ToolBar")
		main_box.pack_start(self._toolbar, False, False, 0)

		self.set_toolbar_style(None)
	
		self._toolbar_recent_menu = self.setup_toolbar_open_button(self._toolbar)

		self._toolbar.foreach(set_non_homogeneus)

		self._toolbar.connect_after("show", self.toolbar_visibility_changed)
		self._toolbar.connect_after("hide", self.toolbar_visibility_changed)
	
	def create_side_panel(self):
		pass # TODO: Implement this
	
	def create_bottom_panel(self):
		pass # TODO: Implement this

	def connect_notebook_signals(self, notebook):
		notebook.connect("switch_page", notebook_switch_page, self)
		# TODO:
#		notebook.connect("tab-added", notebook_tab_added, self)
#		notebook.connect("tab-removed", notebook_tab_removed, self)
#		notebook.connect("tabs-reordered", notebook_tabs_reordered, self)
#		notebook.connect("tab-detached", notebook_tab_detached, self)
#		notebook.connect("tab-close-request", notebook_tab_close_request, self)
#		notebook.connect("button-press-event", notebook_button_press_event, self)
#		notebook.connect("popup-menu", notebook_popup_menu, self)

def recent_manager_changed(manager, window):
	# regenerate the menu when the model changes
	window.update_recent_files_menu()

def notebook_switch_page(book, pg, page_num, window):
	# CHECK: I don't know why but it seems notebook_switch_page is called
	# two times every time the user change the active tab

	tab = book.get_nth_page(page_num)
	if tab == window._active_tab:
		return
		
	window._active_tab = tab
	
	window.set_title()
	window.set_sensitivity_according_to_tab(tab)
	
	# Activate the right item in the documents menu
#	action_name = g_strdup_printf ("Tab_%d", page_num);
#	action = gtk_action_group_get_action (self._documents_list_action_group,
#					      action_name);

#	/* sometimes the action doesn't exist yet, and the proper action
#	 * is set active during the documents list menu creation
#	 * CHECK: would it be nicer if active_tab was a property and we monitored the notify signal?
#	 */
#	if (action != NULL)
#		gtk_toggle_action_set_active (GTK_TOGGLE_ACTION (action), True);

#	g_free (action_name);

#	/* update the syntax menu */
#	update_languages_menu (window);

#	view = gedit_tab_get_view (tab);

#	/* sync the statusbar */
#	update_cursor_position_statusbar (GTK_TEXT_BUFFER (gedit_tab_get_document (tab)),
#					  window);
#	gedit_statusbar_set_overwrite (GEDIT_STATUSBAR (self._statusbar),
#				       gtk_text_view_get_overwrite (GTK_TEXT_VIEW (view)));

	window.emit("active_tab_changed", window._active_tab)

def connect_proxy_cb(manager, action, proxy, window):
	#if (GTK_IS_MENU_ITEM (proxy)) FIXME: Do i need this?
#	proxy.connect("select", self.menu_item_select_cb, window) TODO
#	proxy.connect("deselect", self.menu_item_deselect_cb) TODO
	pass

def disconnect_proxy_cb(manager, action, proxy, window):
	#if (GTK_IS_MENU_ITEM (proxy)) FIXME: Do i need this?
#	proxy.disconnect_by_func(menu_item_select_cb, window) TODO
#	proxy.disconnect_by_func(menu_item_deselect_cb, window) TODO
	pass

def set_non_homogeneus(widget, data):
	widget.set_homogeneous(False)
