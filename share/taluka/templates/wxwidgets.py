import wx

class MyApp(wx.App):
	def OnInit(self):
		frame = wx.Frame(None, -1, "Hello World")
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

app = MyApp(0)
app.MainLoop()
