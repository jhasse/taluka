#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

if __name__ == "__main__":
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	window.connect("destroy", lambda widget: gtk.main_quit())
	window.show()
	gtk.main()
