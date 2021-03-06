# ----------------------------------------------------------------------
# A very simple wxPython example.  Just a wx.Frame, wx.Panel,
# wx.StaticText, wx.Button, and a wx.BoxSizer, but it shows the basic
# structure of any wxPython application.
# ----------------------------------------------------------------------

import os
import wx
import traceback
import myTools
import DSSE_gen
import DSSE_index
import DSSE_enc
import DSSE_zip
import DSSE_srchtoken
import DSSE_addtoken
import DSSE_deltoken
import DSSE_srchdec

wx.ID_SET_USER = 2358
wx.EVT_FRESH = 358


class GenPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        sizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)

        self.last_gen_time_text = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        sizer.Add(wx.StaticText(self, -1, 'Last Time:'))
        sizer.Add(self.last_gen_time_text)
        sizer.Add((-1, -1))
        self.LoadLastGenTime()

        self.dir_path = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
        self.select_dir_button = wx.Button(self, label='Choose Dir')
        self.Bind(wx.EVT_BUTTON, self.OpenDir, self.select_dir_button)
        sizer.Add(wx.StaticText(self, -1, 'Key Dir:'))
        sizer.Add(self.dir_path)
        sizer.Add(self.select_dir_button)
        self.LoadLastGenTime()

        self.regen_button = wx.Button(self, label='Regenerate Key')
        self.Bind(wx.EVT_BUTTON, self.ReGen, self.regen_button)
        sizer.Add(self.regen_button)
        sizer.Add((-1, -1))
        sizer.Add((-1, -1))

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        self.SetSizer(border)

    def LoadLastGenTime(self):
        last_get_time = myTools.GetLastGenTime()
        self.last_gen_time_text.SetValue(str(last_get_time))

    def OpenDir(self, event):
        dlg = wx.DirDialog(self, 'Choose a directory:', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.dir_path.SetValue(str(path))
        dlg.Destroy()

    def ReGen(self, event):
        path = self.dir_path.GetValue()
        print 'Dir: ', path
        if DSSE_gen.gen(path):
            now = myTools.GetNowString()
            myTools.SetLastGenTime(now)
            self.last_gen_time_text.SetValue(str(now))


class ZipPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        sizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)

        self.usernameText = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
        sizer.Add(wx.StaticText(self, -1, 'Username:'))
        sizer.Add(self.usernameText)
        self.LoadUsername()
        self.freshButton = wx.Button(self, label='Fresh')
        self.Bind(wx.EVT_BUTTON, self.OnFresh, self.freshButton)
        sizer.Add(self.freshButton)

        self.dir_path = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
        self.select_dir_button = wx.Button(self, label='Choose Dir')
        self.Bind(wx.EVT_BUTTON, self.OpenDir, self.select_dir_button)
        sizer.Add(wx.StaticText(self, -1, 'File Dir:'))
        sizer.Add(self.dir_path)
        sizer.Add(self.select_dir_button)

        self.zip_button = wx.Button(self, label='Zip')
        self.Bind(wx.EVT_BUTTON, self.Zip, self.zip_button)
        sizer.Add(self.zip_button)
        sizer.Add((-1, -1))
        sizer.Add((-1, -1))

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        self.SetSizer(border)

    def LoadUsername(self):
        username = myTools.GetUserName()
        self.usernameText.SetValue(str(username))

    def OnFresh(self, event):
        self.LoadUsername()

    def OpenDir(self, event):
        dlg = wx.DirDialog(self, 'Choose a directory:', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.dir_path.SetValue(str(path))
        dlg.Destroy()

    def Zip(self, event):
        rootdir = self.dir_path.GetValue()
        user = self.usernameText.GetValue()
        DSSE_index.index(rootdir)
        DSSE_enc.enc(rootdir)
        DSSE_zip.zip(user, rootdir)


class SearchPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        sizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)

        self.usernameText = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
        sizer.Add(wx.StaticText(self, -1, 'Username:'))
        sizer.Add(self.usernameText)
        self.LoadUsername()
        self.freshButton = wx.Button(self, label='Fresh')
        self.Bind(wx.EVT_BUTTON, self.OnFresh, self.freshButton)
        sizer.Add(self.freshButton)

        self.search_word = wx.TextCtrl(self, -1, '')
        sizer.Add(wx.StaticText(self, -1, 'Search Word:'))
        sizer.Add(self.search_word)
        sizer.Add((-1, -1))

        self.srchtoken_button = wx.Button(self, label='Srchtoken')
        self.Bind(wx.EVT_BUTTON, self.Srchtoken, self.srchtoken_button)
        sizer.Add(self.srchtoken_button)
        sizer.Add((-1, -1))
        sizer.Add((-1, -1))

        self.srchdec_button = wx.Button(self, label='Srchdec')
        self.Bind(wx.EVT_BUTTON, self.Srchdec, self.srchdec_button)
        tmp_str = 'Put the zip file at .../tmp/%s/' % self.usernameText.GetValue()
        sizer.Add(wx.StaticText(self, -1, tmp_str))
        sizer.Add(self.srchdec_button)
        sizer.Add((-1, -1))

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        self.SetSizer(border)

    def LoadUsername(self):
        username = myTools.GetUserName()
        self.usernameText.SetValue(str(username))

    def OnFresh(self, event):
        self.LoadUsername()

    def Srchtoken(self, event):
        username = self.usernameText.GetValue()
        word = self.search_word.GetValue()
        DSSE_srchtoken.srchtoken(username, word)

    def Srchdec(self, event):
        username = self.usernameText.GetValue()
        word = self.search_word.GetValue()
        DSSE_srchdec.srchdec(username, word)


class AddPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        sizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)

        self.usernameText = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
        sizer.Add(wx.StaticText(self, -1, 'Username:'))
        sizer.Add(self.usernameText)
        self.LoadUsername()
        self.freshButton = wx.Button(self, label='Fresh')
        self.Bind(wx.EVT_BUTTON, self.OnFresh, self.freshButton)
        sizer.Add(self.freshButton)

        self.file_path = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
        self.select_file_button = wx.Button(self, label='Choose File')
        self.Bind(wx.EVT_BUTTON, self.ChooseFile, self.select_file_button)
        sizer.Add(wx.StaticText(self, -1, 'File Dir:'))
        sizer.Add(self.file_path)
        sizer.Add(self.select_file_button)

        self.addtoken_button = wx.Button(self, label='AddToken')
        self.Bind(wx.EVT_BUTTON, self.AddToken, self.addtoken_button)
        sizer.Add(self.addtoken_button)
        sizer.Add((-1, -1))
        sizer.Add((-1, -1))

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        self.SetSizer(border)

    def LoadUsername(self):
        username = myTools.GetUserName()
        self.usernameText.SetValue(str(username))

    def OnFresh(self, event):
        self.LoadUsername()

    def ChooseFile(self, event):
        dlg = wx.FileDialog(self, 'Choose a file:', os.getcwd(), style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.file_path.SetValue(str(path))
        dlg.Destroy()

    def AddToken(self, event):
        username = self.usernameText.GetValue()
        file_path = self.file_path.GetValue()
        DSSE_addtoken.addtoken(username, file_path)
        DSSE_enc.DSSE_enc(file_path)


class DeletePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        sizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)

        self.usernameText = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
        sizer.Add(wx.StaticText(self, -1, 'Username:'))
        sizer.Add(self.usernameText)
        self.LoadUsername()
        self.freshButton = wx.Button(self, label='Fresh')
        self.Bind(wx.EVT_BUTTON, self.OnFresh, self.freshButton)
        sizer.Add(self.freshButton)

        self.filename = wx.TextCtrl(self, -1, '')
        sizer.Add(wx.StaticText(self, -1, 'File Name:'))
        sizer.Add(self.filename)
        sizer.Add((-1, -1))

        self.deltoken_button = wx.Button(self, label='Deltoken')
        self.Bind(wx.EVT_BUTTON, self.Deltoken, self.deltoken_button)
        sizer.Add(self.deltoken_button)
        sizer.Add((-1, -1))
        sizer.Add((-1, -1))

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 20)
        self.SetSizer(border)

    def LoadUsername(self):
        username = myTools.GetUserName()
        self.usernameText.SetValue(str(username))

    def OnFresh(self, event):
        self.LoadUsername()

    def Deltoken(self, event):
        username = self.usernameText.GetValue()
        filename = self.filename.GetValue()
        DSSE_deltoken.deltoken(username, filename)


class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(450, 500))

        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(wx.ID_SET_USER, "&Set User", "Set User Info")
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnSetUserInfo, id=wx.ID_SET_USER)
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&DSSE")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()

        self.notebook = wx.Notebook(self, -1, name='notebook')

        self.notebook.AddPage(GenPanel(self.notebook), 'Gen')
        self.notebook.AddPage(ZipPanel(self.notebook), 'Zip')
        self.notebook.AddPage(SearchPanel(self.notebook), 'Search')
        self.notebook.AddPage(AddPanel(self.notebook), 'Add')
        self.notebook.AddPage(DeletePanel(self.notebook), 'Delete')

    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        print "See ya later!"
        self.Close()

    def OnSetUserInfo(self, evt):
        ''' Set User Info '''
        dlg = wx.TextEntryDialog(self, 'Enter Your Username', 'User Info Entry')
        dlg.SetValue('Default')
        if dlg.ShowModal() == wx.ID_OK:
            username = dlg.GetValue()
            myTools.SetUserName(username)
            self.SetStatusText('You entered: %s\n' % username)
        dlg.Destroy()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "DSSE Client")
        # self.SetTopWindow(frame)
        print "Print statements go to this stdout window by default."

        frame.Show(True)
        return True

try:
    app = MyApp(redirect=True)
    app.MainLoop()
except:
    print traceback.print_exc()
    a = raw_input('input a: ')
    print a
