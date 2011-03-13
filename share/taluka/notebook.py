#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Jan Niklas Hasse <jhasse@gmail.com>
#                    Jannes Meyer <jannes.meyer@gmail.com>
#                    Fabian Franzen <flammenvogel@arcor.de>
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
import tab
import gobject
from starthere import StartHere
from enums import *

class Notebook(gtk.Notebook):
	__gsignals__ = { 'tab_added' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (tab.Tab,)),
	                 'tab_removed' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (tab.Tab,)) }

	def __init__(self):
		super(type(self), self).__init__()
		
		self._always_show_tabs = False
		
		self.add_start_here_tab()
		self.show_all()
	
	def add_tab(self, tab, position, jump_to):
		label = self.build_tab_label(tab)
		self.update_tabs_visibility(True)
		
		self.insert_page(tab, label, position)
		
		sync_name(tab, None, label)
		
		tab.connect("notify::name", sync_name, label)
		tab.connect("notify::state", sync_name, label)
		
		self.emit("tab_added", tab)
		
		# The signal handler may have reordered the tabs
		position = self.page_num(tab)
		
		if jump_to:
			self.set_current_page(position)
			
			tab.set_data("jump_to", jump_to) # FIXME: I'm unsure about this
			
			view = tab.get_view()
			
			view.grab_focus()

		return tab # TODO: Should i return the tab?
	
	def add_start_here_tab(self):
		#self.add_tab(StartHere(), 0, True)
		pass
	
	def remove_tab(self, tab):
		position = self.page_num(tab)

# TODO: Can I leave this out?
#		label = gtk_notebook_get_tab_label (GTK_NOTEBOOK (nb), GTK_WIDGET (tab));
#		ebox = GTK_WIDGET (g_object_get_data (G_OBJECT (label), "label-ebox"));

#		g_signal_handlers_disconnect_by_func (tab,
#							  G_CALLBACK (sync_name), 
#							  label);

		self.remove_page(position)
		self.update_tabs_visibility(False)
		self.emit("tab_removed", tab)
	
	def remove_all_tabs(self):
		self._focused_pages = None
		self.foreach(self.remove_tab)
	
	def move_tab(self, dest, tab, dest_position):
		raise NotImplementedError

	def set_always_show_tabs(self, show_tabs):
		raise NotImplementedError
	
	def set_close_buttons_sensitive(self, sensitive):
		raise NotImplementedError
	
	def get_close_buttons_sensitive(self):
		raise NotImplementedError
	
	def set_tab_drag_and_drop_enabled(self, enable):
		raise NotImplementedError
	
	def get_tab_drag_and_drop_enabled(self):
		raise NotImplementedError
	
	def build_tab_label(self, tab):
		hbox = gtk.HBox(False, 4)
		
		label_ebox = gtk.EventBox()
		label_ebox.set_visible_window(False)
		hbox.pack_start(label_ebox, True, True, 0)
		
		label_hbox = gtk.HBox(False, 4)
		label_ebox.add(label_hbox)

		# setup label
		label = gtk.Label("")
		label.set_alignment(0.0, 0.5)
		label.set_padding(0, 0)
		label_hbox.pack_start(label, False, False, 0)
		
		dummy_label = gtk.Label("")
		label_hbox.pack_start(dummy_label, True, True, 0)
			
		#	/* Set minimal size */
		#	g_signal_connect (hbox, "style-set",
		#			  G_CALLBACK (tab_label_style_set_cb), NULL);
		
		hbox.show()
		label_ebox.show()
		label_hbox.show()
		label.show()
		dummy_label.show()
		
		hbox.set_data("label", label)
		hbox.set_data("label-ebox", label_ebox)
		
		return hbox
	
	# Hide tabs if there is only one tab and the pref is not set
	def update_tabs_visibility(nb, before_inserting):
		num = nb.get_n_pages()
		
		if before_inserting:
			num += 1

		show_tabs = (nb._always_show_tabs or num > 1)
		
		nb.set_show_tabs(show_tabs)


# update_tabs_visibility: Hide tabs if there is only one tab
# and the pref is not set.
def update_tabs_visibility(nb, before_inserting):
	num = nb.get_n_pages()

	if before_inserting:
		num += 1

	show_tabs = False
	if nb._always_show_tabs or num > 1:
		show_tabs = True

	nb.set_show_tabs(show_tabs)

def sync_name(tab, pspec, hbox):
	label = hbox.get_data("label")
	ebox = hbox.get_data("label-ebox")
	
	nb = tab.get_parent()
	
	str = tab._get_name()
	
	label.set_text(str)
	
	str = tab.get_tooltips()
	
	ebox.set_tooltip_markup(str)
	
	state = tab.get_state()
	
	if state == TAB_STATE_LOADING or \
	   state == TAB_STATE_SAVING or \
	   state == TAB_STATE_REVERTING:
		icon.hide()
		
		spinner.show()
		spinner.start()
	else:
		pixbuf = tab._get_icon()
# TODO: Fix this mess
#		icon.set_from_pixbuf(pixbuf)
		
#		if pixbuf != None:
#			pixbuf.unref()

#		icon.show()
		
#		spinner.hide()
#		spinner.stop()
