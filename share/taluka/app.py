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

class App:
	instance = None
	@classmethod
	def get_instance(cls):
		if cls.instance == None:
			cls.instance = App()
		return cls.instance
	
	def __init__(self):
		# TODO:
		# load_accels()

		# initial lockdown state
		#self._lockdown = prefs_manager_get_lockdown()
		self._lockdown = None
	
	def get_lockdown(self):
		return self._lockdown

def app_get_default():
	return App.get_instance()
