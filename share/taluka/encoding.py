#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007-2009 Jan Niklas Hasse <jhasse@gmail.com>
#                     Jannes Meyer <jannes.meyer@gmail.com>
#
# As this code is based on gedit: Copyright 2003-2006 Paolo Maggi
# Also check out gedit's AUTHORS file.
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

import gobject

class Encoding(gobject.GObject):
	def __init__(self, index, charset, name):
		super(type(self), self).__init__()
		self.index = index
		self.charset = charset
		
		self.name = name
	
	def	to_string(self):
		encoding_lazy_init()
		
		if self.charset == None:
			return
		
		if self.name != None:
			return "%s (%s)" % (self.name, self.charset)
		else:
			if self.charset == "ANSI_X3.4-1968":
				return "US-ASCII (%s)" % self.charset
			else:
				return self.charset

# The original versions of the following tables are taken from profterm 
# Copyright (C) 2002 Red Hat, Inc.

ENCODING_ISO_8859_1=1
ENCODING_ISO_8859_2=2
ENCODING_ISO_8859_3=3
ENCODING_ISO_8859_4=4
ENCODING_ISO_8859_5=5
ENCODING_ISO_8859_6=6
ENCODING_ISO_8859_7=7
ENCODING_ISO_8859_8=8
ENCODING_ISO_8859_8_I=9
ENCODING_ISO_8859_9=10
ENCODING_ISO_8859_10=11
ENCODING_ISO_8859_13=12
ENCODING_ISO_8859_14=13
ENCODING_ISO_8859_15=14
ENCODING_ISO_8859_16=15
ENCODING_UTF_7=16
ENCODING_UTF_16=17
ENCODING_UTF_16_BE=18
ENCODING_UTF_16_LE=19
ENCODING_UTF_32=20
ENCODING_UCS_2=21
ENCODING_UCS_4=22
ENCODING_ARMSCII_8=23
ENCODING_BIG5=24
ENCODING_BIG5_HKSCS=25
ENCODING_CP_866=26
ENCODING_EUC_JP=27
ENCODING_EUC_JP_MS=28
ENCODING_CP932=29
ENCODING_EUC_KR=30
ENCODING_EUC_TW=31
ENCODING_GB18030=32
ENCODING_GB2312=33
ENCODING_GBK=34
ENCODING_GEOSTD8=35
ENCODING_HZ=36

ENCODING_IBM_850=37
ENCODING_IBM_852=38
ENCODING_IBM_855=39
ENCODING_IBM_857=40
ENCODING_IBM_862=41
ENCODING_IBM_864=42
ENCODING_ISO_2022_JP=43
ENCODING_ISO_2022_KR=44
ENCODING_ISO_IR_111=45
ENCODING_JOHAB=46
ENCODING_KOI8_R=47
ENCODING_KOI8__R=48
ENCODING_KOI8_U=49
  
ENCODING_SHIFT_JIS=50
ENCODING_TCVN=51
ENCODING_TIS_620=52
ENCODING_UHC=53
ENCODING_VISCII=54

ENCODING_WINDOWS_1250=55
ENCODING_WINDOWS_1251=56
ENCODING_WINDOWS_1252=57
ENCODING_WINDOWS_1253=58
ENCODING_WINDOWS_1254=59
ENCODING_WINDOWS_1255=60
ENCODING_WINDOWS_1256=61
ENCODING_WINDOWS_1257=62
ENCODING_WINDOWS_1258=63

ENCODING_LAST=64

ENCODING_UTF_8=65
ENCODING_UNKNOWN=66

utf8_encoding = Encoding(ENCODING_UTF_8, "UTF-8",	"Unicode");

# initialized in encoding_lazy_init() FIXME: It isn't
unknown_encoding = Encoding(ENCODING_UNKNOWN, None, None)

encodings = (
  Encoding( ENCODING_ISO_8859_1,
    "ISO-8859-1", "Western") ,
  Encoding( ENCODING_ISO_8859_2,
   "ISO-8859-2", "Central European") ,
  Encoding( ENCODING_ISO_8859_3,
    "ISO-8859-3", "South European") ,
  Encoding( ENCODING_ISO_8859_4,
    "ISO-8859-4", "Baltic") ,
  Encoding( ENCODING_ISO_8859_5,
    "ISO-8859-5", "Cyrillic") ,
  Encoding( ENCODING_ISO_8859_6,
    "ISO-8859-6", "Arabic") ,
  Encoding( ENCODING_ISO_8859_7,
    "ISO-8859-7", "Greek") ,
  Encoding( ENCODING_ISO_8859_8,
    "ISO-8859-8", "Hebrew Visual") ,
  Encoding( ENCODING_ISO_8859_8_I,
    "ISO-8859-8-I", "Hebrew") ,
  Encoding( ENCODING_ISO_8859_9,
    "ISO-8859-9", "Turkish") ,
  Encoding( ENCODING_ISO_8859_10,
    "ISO-8859-10", "Nordic") ,
  Encoding( ENCODING_ISO_8859_13,
    "ISO-8859-13", "Baltic") ,
  Encoding( ENCODING_ISO_8859_14,
    "ISO-8859-14", "Celtic") ,
  Encoding( ENCODING_ISO_8859_15,
    "ISO-8859-15", "Western") ,
  Encoding( ENCODING_ISO_8859_16,
    "ISO-8859-16", "Romanian") ,

  Encoding( ENCODING_UTF_7,
    "UTF-7", "Unicode") ,
  Encoding( ENCODING_UTF_16,
    "UTF-16", "Unicode") ,
  Encoding( ENCODING_UTF_16_BE,
    "UTF-16BE", "Unicode") ,
  Encoding( ENCODING_UTF_16_LE,
    "UTF-16LE", "Unicode") ,
  Encoding( ENCODING_UTF_32,
    "UTF-32", "Unicode") ,
  Encoding( ENCODING_UCS_2,
    "UCS-2", "Unicode") ,
  Encoding( ENCODING_UCS_4,
    "UCS-4", "Unicode") ,

  Encoding( ENCODING_ARMSCII_8,
    "ARMSCII-8", "Armenian") ,
  Encoding( ENCODING_BIG5,
    "BIG5", "Chinese Traditional") ,
  Encoding( ENCODING_BIG5_HKSCS,
    "BIG5-HKSCS", "Chinese Traditional") ,
  Encoding( ENCODING_CP_866,
    "CP866", "Cyrillic/Russian") ,

  Encoding( ENCODING_EUC_JP,
    "EUC-JP", "Japanese") ,
  Encoding( ENCODING_EUC_JP_MS,
    "EUC-JP-MS", "Japanese") ,
  Encoding( ENCODING_CP932,
    "CP932", "Japanese") ,

  Encoding( ENCODING_EUC_KR,
    "EUC-KR", "Korean") ,
  Encoding( ENCODING_EUC_TW,
    "EUC-TW", "Chinese Traditional") ,

  Encoding( ENCODING_GB18030,
    "GB18030", "Chinese Simplified") ,
  Encoding( ENCODING_GB2312,
    "GB2312", "Chinese Simplified") ,
  Encoding( ENCODING_GBK,
    "GBK", "Chinese Simplified") ,
  Encoding( ENCODING_GEOSTD8,
    "GEORGIAN-ACADEMY", "Georgian") , # FIXME GEOSTD8 ?
  Encoding( ENCODING_HZ,
    "HZ", "Chinese Simplified") ,

  Encoding( ENCODING_IBM_850,
    "IBM850", "Western") ,
  Encoding( ENCODING_IBM_852,
    "IBM852", "Central European") ,
  Encoding( ENCODING_IBM_855,
    "IBM855", "Cyrillic") ,
  Encoding( ENCODING_IBM_857,
    "IBM857", "Turkish") ,
  Encoding( ENCODING_IBM_862,
    "IBM862", "Hebrew"),
  Encoding( ENCODING_IBM_864,
    "IBM864", "Arabic") ,

  Encoding( ENCODING_ISO_2022_JP,
    "ISO-2022-JP", "Japanese") ,
  Encoding( ENCODING_ISO_2022_KR,
    "ISO-2022-KR", "Korean") ,
  Encoding( ENCODING_ISO_IR_111,
    "ISO-IR-111", "Cyrillic") ,
  Encoding( ENCODING_JOHAB,
    "JOHAB", "Korean") ,
  Encoding( ENCODING_KOI8_R,
    "KOI8R", "Cyrillic") ,
  Encoding( ENCODING_KOI8__R,
    "KOI8-R", "Cyrillic") ,
  Encoding( ENCODING_KOI8_U,
    "KOI8U", "Cyrillic/Ukrainian") ,
  
  Encoding( ENCODING_SHIFT_JIS,
    "SHIFT_JIS", "Japanese") ,
  Encoding( ENCODING_TCVN,
    "TCVN", "Vietnamese") ,
  Encoding( ENCODING_TIS_620,
    "TIS-620", "Thai") ,
  Encoding( ENCODING_UHC,
    "UHC", "Korean") ,
  Encoding( ENCODING_VISCII,
    "VISCII", "Vietnamese") ,

  Encoding( ENCODING_WINDOWS_1250,
    "WINDOWS-1250", "Central European") ,
  Encoding( ENCODING_WINDOWS_1251,
    "WINDOWS-1251", "Cyrillic") ,
  Encoding( ENCODING_WINDOWS_1252,
    "WINDOWS-1252", "Western"),
  Encoding( ENCODING_WINDOWS_1253,
    "WINDOWS-1253", "Greek") ,
  Encoding( ENCODING_WINDOWS_1254,
    "WINDOWS-1254", "Turkish") ,
  Encoding( ENCODING_WINDOWS_1255,
    "WINDOWS-1255", "Hebrew") ,
  Encoding( ENCODING_WINDOWS_1256,
    "WINDOWS-1256", "Arabic") ,
  Encoding( ENCODING_WINDOWS_1257,
    "WINDOWS-1257", "Baltic") ,
  Encoding( ENCODING_WINDOWS_1258,
    "WINDOWS-1258", "Vietnamese")
)

def encoding_lazy_init():
	initialized = False
	
	if (initialized):
		return

# FIXME:	
#	if (g_get_charset (&locale_charset) == FALSE)
#	{
#		unknown_encoding.charset = g_strdup (locale_charset);
#	}
#	unkown_encoding.charset = locale_charset

	initialized = True

#const GeditEncoding *
#gedit_encoding_get_from_charset (const gchar *charset)
#{
#	gint i;

#	g_return_val_if_fail (charset != NULL, NULL);

#	gedit_encoding_lazy_init ();

#	if (charset == NULL)
#		return NULL;

#	if (g_ascii_strcasecmp (charset, "UTF-8") == 0)
#		return gedit_encoding_get_utf8 ();

#	i = 0; 
#	while (i < ENCODING_LAST)
#	{
#		if (g_ascii_strcasecmp (charset, encodings[i].charset) == 0)
#			return &encodings[i];
#      
#		++i;
#	}

#	if (unknown_encoding.charset != NULL)
#	{
#		if (g_ascii_strcasecmp (charset, unknown_encoding.charset) == 0)
#			return &unknown_encoding;
#	}

#	return NULL;
#}

#const GeditEncoding *
#gedit_encoding_get_from_index (gint index)
#{
#	g_return_val_if_fail (index >= 0, NULL);

#	if (index >= ENCODING_LAST)
#		return NULL;

#	gedit_encoding_lazy_init ();

#	return &encodings [index];
#}

def encoding_get_utf8():
	encoding_lazy_init()
	return utf8_encoding

#const GeditEncoding *
#gedit_encoding_get_current (void)
#{
#	static gboolean initialized = FALSE;
#	static const GeditEncoding *locale_encoding = NULL;

#	const gchar *locale_charset;

#	gedit_encoding_lazy_init ();

#	if (initialized != FALSE)
#		return locale_encoding;

#	if (g_get_charset (&locale_charset) == FALSE) 
#	{
#		g_return_val_if_fail (locale_charset != NULL, &utf8_encoding);
#		
#		locale_encoding = gedit_encoding_get_from_charset (locale_charset);
#	}
#	else
#	{
#		locale_encoding = &utf8_encoding;
#	}
#	
#	if (locale_encoding == NULL)
#	{
#		locale_encoding = &unknown_encoding;
#	}

#	g_return_val_if_fail (locale_encoding != NULL, NULL);

#	initialized = TRUE;

#	return locale_encoding;
#}

#gchar *
#gedit_encoding_to_string (const GeditEncoding* enc)
#{
#	g_return_val_if_fail (enc != NULL, NULL);
#	
#	gedit_encoding_lazy_init ();

#	g_return_val_if_fail (enc->charset != NULL, NULL);

#	if (enc->name != NULL)
#	{
#	    	return g_strdup_printf ("%s (%s)", _(enc->name), enc->charset);
#	}
#	else
#	{
#		if (g_ascii_strcasecmp (enc->charset, "ANSI_X3.4-1968") == 0)
#			return g_strdup_printf ("US-ASCII (%s)", enc->charset);
#		else
#			return g_strdup (enc->charset);
#	}
#}

#const gchar *
#gedit_encoding_get_charset (const GeditEncoding* enc)
#{
#	g_return_val_if_fail (enc != NULL, NULL);

#	gedit_encoding_lazy_init ();

#	g_return_val_if_fail (enc->charset != NULL, NULL);

#	return enc->charset;
#}

#const gchar *
#gedit_encoding_get_name (const GeditEncoding* enc)
#{
#	g_return_val_if_fail (enc != NULL, NULL);

#	gedit_encoding_lazy_init ();

#	return (enc->name == NULL) ? _("Unknown") : _(enc->name);
#}

#/* These are to make language bindings happy. Since Encodings are
# * const, copy() just returns the same pointer and fres() doesn't
# * do nothing */

#GeditEncoding *
#gedit_encoding_copy (const GeditEncoding *enc)
#{
#	g_return_val_if_fail (enc != NULL, NULL);

#	return (GeditEncoding *) enc;
#}

#void 
#gedit_encoding_free (GeditEncoding *enc)
#{
#	g_return_if_fail (enc != NULL);
#}

#/**
# * gedit_encoding_get_type:
# * 
# * Retrieves the GType object which is associated with the
# * #GeditEncoding class.
# * 
# * Return value: the GType associated with #GeditEncoding.
# **/
#GType 
#gedit_encoding_get_type (void)
#{
#	static GType our_type = 0;

#	if (!our_type)
#		our_type = g_boxed_type_register_static (
#			"GeditEncoding",
#			(GBoxedCopyFunc) gedit_encoding_copy,
#			(GBoxedFreeFunc) gedit_encoding_free);

#	return our_type;
#} 

