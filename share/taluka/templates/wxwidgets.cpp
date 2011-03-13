#include "wx/wx.h"

class MyApp: public wxApp
{
	virtual bool OnInit();
};

class MyFrame: public wxFrame
{
public:
	MyFrame(const wxString& title, const wxPoint& pos, const wxSize& size)
		: wxFrame((wxFrame*)NULL, -1, title, pos, size)
	{
	}
};

IMPLEMENT_APP(MyApp)

bool MyApp::OnInit()
{
	MyFrame* frame = new MyFrame(_T("Hello World"), wxPoint(50,50), wxSize(450,340));
	frame->Show(true);
	SetTopWindow(frame);
	return true;
}
