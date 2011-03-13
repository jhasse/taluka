#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser

class GtkEmuError(Exception):
	pass

class Options():
	def __init__(self, optionfile):
		self.parser = ConfigParser.SafeConfigParser()
		self.optionfile = optionfile
		self.read()
		self.update()

	def read(self):
		self.parser.read(self.optionfile)

	def update(self):
		self.settings = {}
		sections = self.parser.sections()
		for section in sections:
			self.settings[section] = {}
			items = self.parser.items(section)
			for item in items:
				self.settings[section][item[0]] = self.get_conversion(section, item[0], item[1])

	def save(self):
		fp = open(self.optionfile, 'w')
		self.parser.write(fp)
		fp.close()
	
	def create_section(self, section):
		self.parser.add_section(section)
		self.settings[section] = {}
	
	def get(self, section, option):
		if not self.parser.has_section(section):
			self.create_section(section)

		if not self.parser.has_option(section, option):
			try:
				self.set(section, option, self.default_values[section][option][0])
			except:
				# if no default value is available
				raise GtkEmuError('Couldn't read option '%s' from the config file.' % option)
		return self.settings[section][option]
	
	def get_conversion(self, section, option, value):
		try:
			type = self.default_values[section][option][1]
		except:
			print 'unrecognized option '%s'' % option
			type = None

		if type == 'bool':
			if value == 'true':
				value = True
			elif value == 'false':
				value = False
			else:
				value = self.default_values[section][option][0]
		elif type == 'list':
			value = value.split(self.list_seperator)
		elif type == 'int':
			value == int(value)
		return value

	def set(self, section, option, value):
		if not self.parser.has_section(section):
			self.create_section(section)

		value = self.set_conversion(section, option, value)
		self.parser.set(section, option, value)
		self.settings[section][option] = value

	def set_conversion(self, section, option, value):
		try:
			type = self.default_values[section][option][1]
		except:
			print 'update your default_values! '%s' wasn't found' % option
			type = None
		if type == 'bool':
			if value == True:
				value = 'true'
			elif value == False:
				value = 'false'
		elif type == 'list':
			value = self.list_seperator.join(value)
		elif type == 'int':
			value == str(value)
		elif type == 'str':
			pass
		return value
