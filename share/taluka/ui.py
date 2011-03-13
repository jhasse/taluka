import gtk
import commands

def N_(s): # FIXME use gettext
	return s

always_sensitive_menu_entries = (
	# Toplevel
	( "File", None, N_("_File") ),
	( "Edit", None, N_("_Edit") ),
	( "View", None, N_("_View") ),
	( "Search", None, N_("_Search") ),
	( "Tools", None, N_("_Tools") ),
	( "Documents", None, N_("_Documents") ),
	( "Help", None, N_("_Help") ),

	# File menu
	( "FileNew", gtk.STOCK_NEW, None, "<control>N",
	  N_("Create a new document"), commands._file_new ),
	( "FileOpen", gtk.STOCK_OPEN, N_("_Open..."), "<control>O",
	  N_("Open a file"), commands._file_open ),

	# Edit menu
#	( "EditPreferences", gtk.STOCK_PREFERENCES, N_("Pr_eferences"), None,
#	  N_("Configure the application"), commands._edit_preferences ),

	# Help menu
#	("HelpContents", gtk.STOCK_HELP, N_("_Contents"), "F1",
#	 N_("Open the gedit manual"), commands._help_contents ),
#	( "HelpAbout", gtk.STOCK_ABOUT, None, None,
#	 N_("About this application"), commands._help_about ),
	
	# Fullscreen toolbar
#	( "LeaveFullscreen", gtk.STOCK_LEAVE_FULLSCREEN, None,
#	  None, N_("Leave fullscreen mode"), commands._view_leave_fullscreen_mode )
)

menu_entries = (
	# File menu
	( "FileSave", gtk.STOCK_SAVE, None, "<control>S",
	  N_("Save the current file"), commands._file_save ),
	( "FileSaveAs", gtk.STOCK_SAVE_AS, N_("Save _As..."), "<shift><control>S",
	  N_("Save the current file with a different name"), commands._file_save_as ),
#	( "FileRevert", gtk.STOCK_REVERT_TO_SAVED, None, None,
#	  N_("Revert to a saved version of the file"), commands._file_revert ),
#	( "FilePrintPreview", gtk.STOCK_PRINT_PREVIEW, N_("Print Previe_w"),"<control><shift>P",
#	  N_("Print preview"), commands._file_print_preview ),
#	( "FilePrint", gtk.STOCK_PRINT, N_("_Print..."), "<control>P",
#	  N_("Print the current page"), commands._file_print ),

	# Edit menu
	( "EditUndo", gtk.STOCK_UNDO, None, "<control>Z",
	  N_("Undo the last action"), commands._edit_undo ),
	( "EditRedo", gtk.STOCK_REDO, None, "<shift><control>Z",
	  N_("Redo the last undone action"), commands._edit_redo ),
	( "EditCut", gtk.STOCK_CUT, None, "<control>X",
	  N_("Cut the selection"), commands._edit_cut ),
	( "EditCopy", gtk.STOCK_COPY, None, "<control>C",
	  N_("Copy the selection"), commands._edit_copy ),
	( "EditPaste", gtk.STOCK_PASTE, None, "<control>V",
	  N_("Paste the clipboard"), commands._edit_paste ),
	( "EditSelectAll", gtk.STOCK_SELECT_ALL, N_("Select _All"), "<control>A",
	  N_("Select the entire document"), commands._edit_select_all ),

	# View menu
	( "ViewHighlightMode", None, N_("_Highlight Mode") ),

	# Search menu
#	( "SearchFind", gtk.STOCK_FIND, N_("_Find..."), "<control>F",
#	  N_("Search for text"), commands._search_find ),
#	( "SearchFindNext", None, N_("Find Ne_xt"), "<control>G",
#	  N_("Search forwards for the same text"), commands._search_find_next ),
#	( "SearchFindPrevious", None, N_("Find Pre_vious"), "<shift><control>G",
#	  N_("Search backwards for the same text"), commands._search_find_prev ),
#	( "SearchReplace", gtk.STOCK_FIND_AND_REPLACE, N_("_Replace..."), "<control>H",
#	  N_("Search for and replace text"), commands._search_replace ),
#	( "SearchClearHighlight", None, N_("_Clear Highlight"), "<shift><control>K",
#	  N_("Clear highlighting of search matches"), commands._search_clear_highlight ),
#	( "SearchGoToLine", gtk.STOCK_JUMP_TO, N_("Go to _Line..."), "<control>I",
#	  N_("Go to a specific line"), commands._search_goto_line ),
#	( "SearchIncrementalSearch", gtk.STOCK_FIND, N_("_Incremental Search..."), "<control>K",
#	  N_("Incrementally search for text"), commands._search_incremental_search ),

	# Documents menu
#	( "FileSaveAll", gtk.STOCK_SAVE, N_("_Save All"), "<shift><control>L",
#	  N_("Save all open files"), commands._file_save_all ),
#	( "FileCloseAll", gtk.STOCK_CLOSE, N_("_Close All"), "<shift><control>W",
#	  N_("Close all open files"), commands._file_close_all ),
#	( "DocumentsPreviousDocument", None, N_("_Previous Document"), "<alt><control>Page_Up",
#	  N_("Activate previous document"), commands._documents_previous_document ),
#	( "DocumentsNextDocument", None, N_("_Next Document"), "<alt><control>Page_Down",
#	  N_("Activate next document"), commands._documents_next_document ),
#	( "DocumentsMoveToNewWindow", None, N_("_Move to New Window"), None,
#	  N_("Move the current document to a new window"), commands._documents_move_to_new_window )
)

# separate group, needs to be sensitive on OS X even when there are no tabs
close_menu_entries = (
	( "FileClose", gtk.STOCK_CLOSE, None, "<control>W",
	  N_("Close the current file"), commands._file_close ),
)

# separate group, should be sensitive even when there are no tabs
quit_menu_entries = (
	( "FileQuit", gtk.STOCK_QUIT, None, "<control>Q",
	  N_("Quit the program"), commands._file_quit ),
)

always_sensitive_toggle_menu_entries = (
#	( "ViewToolbar", None, N_("_Toolbar"), None,
#	  N_("Show or hide the toolbar in the current window"),
#	  commands._view_show_toolbar, True ),
#	( "ViewStatusbar", None, N_("_Statusbar"), None,
#	  N_("Show or hide the statusbar in the current window"),
#	  commands._view_show_statusbar, True ),
#	( "ViewFullscreen", gtk.STOCK_FULLSCREEN, None, "F11",
#	  N_("Edit text at fullscreen"),
#	  commands._view_toggle_fullscreen_mode, False )
)

# separate group, should be always sensitive except when there are no panes
panes_toggle_menu_entries = (
#	( "ViewSidePane", None, N_("Side _Pane"), "F9",
#	  N_("Show or hide the side pane in the current window"),
#	  commands._view_show_side_pane, False ),
#	( "ViewBottomPane", None, N_("_Bottom Pane"), "<control>F9",
#	  N_("Show or hide the bottom pane in the current window"),
#	  commands._view_show_bottom_pane, False )
)
