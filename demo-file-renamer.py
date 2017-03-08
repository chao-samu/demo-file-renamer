#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  ===================================================================================
#  Python Version ......: 3.*
#  Version .............: 1.06 (Python)
#  Release Date ........: 2017-03-08
#  GitHub ..............: https://github.com/chao-samu/demo-file-renamer
#  Author ..............: chao-samu
# ------------------------------------------------------------------------------------
#  Script Name..........: demo file renamer
#  Description .........: Integrate mapname into demofile (*.dem).
#                         Support: TF2, CS 1.6, CS:S and CS:GO
#  License..............: MIT License (https://github.com/chao-samu/demo-file-renamer/blob/master/LICENSE)
#  ===================================================================================

from concurrent import futures
import datetime, glob, os, os.path, re, string, sys, textwrap, wx

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(345,320), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        
        # Variables
        self.ListSelection = 0
        textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "samurai-vs-ninja_de_dust2.dem"'
        
        # Center frame
        self.Center()
        
        # Icon set
        # ico = wx.Icon(IconPath, wx.BITMAP_TYPE_ICO)
        # self.SetIcon(ico)
        
        # StatusBar creation in the bottom of the window
        self.CreateStatusBar() 
        
        # MenuBar in the top of the window
        helpmenu = wx.Menu()

        # MenuBar colums
        menuHelp = helpmenu.Append(wx.ID_HELP)
        menuSeperator = helpmenu.AppendSeparator()
        menuLicense = helpmenu.Append(wx.ID_VIEW_DETAILS, "License") # should use wx.newid()
        menuAbout = helpmenu.Append(wx.ID_ABOUT)
        menuSeperator = helpmenu.AppendSeparator()
        menuExit = helpmenu.Append(wx.ID_EXIT)

        # MenuBar creation
        menuBar = wx.MenuBar()
        menuBar.Append(helpmenu,"&Help") # Adding the "helpmenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # FramePanel creation        
        panel = wx.Panel(self, -1)
        wx.StaticText(panel, -1, "Choose renaming mask:",(30,15))
        self.ListBoxSelect = wx.ListBox(panel, -1, choices=["OLDNAME_MAPNAME", "MAPNAME_OLDNAME", "YYYY-MM-DD_MAPNAME_OLDNAME", "YYYY-MM-DD_OLDNAME_MAPNAME"],size=(270,35),pos=(30,40))
        self.StaticTextExample = wx.StaticText(panel, -1, textExample,(30,80))
        wx.StaticText(panel, -1, "Extracting mapname",(30,150))
        self.GaugeProgress = wx.Gauge(panel, -1, range=100, pos=(30,170),size=(270,10))
        self.buttonCancel = wx.Button(panel, -1, "Cancel", (30,200),(90,20))
        self.buttonStart = wx.Button(panel, -1, "Start", (210,200),(90,20))
        
        # Preselect default settings
        self.ListBoxSelect.SetSelection(0)
        
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnHelp, menuHelp)
        self.Bind(wx.EVT_MENU, self.OnLicense, menuLicense)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)     
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_LISTBOX, self.OnListSelect, self.ListBoxSelect)
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.buttonStart)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.buttonCancel)
        
        # Create/Show MainWindow
        self.Show(True)
        
    def OnHelp(self, event):
        # MessageDialog creation
        MessageDlgText = """\
        What can do this Tool?
        This tool was manly made to extract out the mapname of
        GoldSrc- and Source Engine demofiles and place it in the name of the demofile itself.

        Which kind of demofiles this tool can handle?
        Currently this tool support Counter-Strike 1.6, Counter-Strike Source,
        Counter-Strike Global Offensive and Team Fortress 2 demofiles.

        How to use?
        1. Select your renaming mask you want
        2. Press start and select in the following window your folder with the supported demofiles
            (please note, all demofiles with the ending "dem" in this folder will be renamed, subfolder
            are not included).
            In a protected folder (like "ProgramFiles") you have to start this program in admin mode!
        3. Press OK and wait until you will hopefully be happy :)
        """
        MessageDlgText = textwrap.dedent(MessageDlgText)
        
        dlg = wx.MessageDialog( self, MessageDlgText, "Help", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
        
    def OnLicense(self, event):
        # MessageDialog creation
        MessageDlgText = """\
        :::::::::::::::This software is provided under the following License:::::::::::::::::::::

        The MIT License (MIT)

        Copyright (c) 2015 chao-samu

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        """
        MessageDlgText = textwrap.dedent(MessageDlgText)
        
        dlg = wx.MessageDialog( self, MessageDlgText, "About", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnAbout(self, event):
        # MessageDialog creation
        MessageDlgText = PrgName + ":\n" + PrgVersion + "\n\nBased on Python version:\n" + PytonVersion + "\n\nGUI made with wxPython version:\n" + WxVersion + "\n\nMade by chao-samu" + "\nLook for updates: https://github.com/chao-samu"
        
        dlg = wx.MessageDialog( self, MessageDlgText, "License", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
        
    def OnExit(self, event):
        self.Close(True)  # Close the frame.
        
    def OnListSelect(self, event):
        self.ListSelection = event.GetSelection()      
        if self.ListSelection == 0:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "samurai-vs-ninja_de_dust2.dem"'
            self.StaticTextExample.SetLabel(textExample)
        elif self.ListSelection == 1:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "de_dust2_samurai-vs-ninja.dem"'
            self.StaticTextExample.SetLabel(textExample)
        elif self.ListSelection == 2:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "2007-05-03_de_dust2_samurai-vs-ninja.dem"'
            self.StaticTextExample.SetLabel(textExample)
        else:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "2007-05-03_samurai-vs-ninja_de_dust2.dem"'
            self.StaticTextExample.SetLabel(textExample)
            
    def OnStart(self, event):
        saveDirDialog = wx.DirDialog(self, "Please select your folder where your demofiles are.\n All files with the ending *.dem will be renamed.", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)       

        if saveDirDialog.ShowModal() == wx.ID_OK:
            os.chdir(saveDirDialog.GetPath())
            MTT = futures.ThreadPoolExecutor(max_workers=1) # check if correct implementated
            MTT.submit(RenamingDemoFiles, self.ListSelection) # check if correct implementated
            MTT.shutdown(False) # check if correct implementated
            return
        else:
            return     # the user changed idea...
            
    def OnCancel(self, event):
        self.Close()
        
    def OnFinish(self):
        # MessageDialog creation
        MessageDlgText = "All files successfully renamed!"
        
        dlg = wx.MessageDialog( self, MessageDlgText, "Success", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
        
    def OnFinishFailed(self, logfile_name, logfile_ext, file_failed_counter):
        # MessageDialog creation
        MessageDlgText = "Files failed to rename: " + str(file_failed_counter) + " of " + str(len(glob.glob('*.dem'))) + "\nLogfile is generated, please look for further information in logfile: \"" + os.getcwd() +  os.sep + logfile_name + logfile_ext + "\""
        
        dlg = wx.MessageDialog( self, MessageDlgText, "Partitial success", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
        
    def OnStartRenaming(self, demofileCount):
        # MessageDialog creation
        MessageDlgText = "Files found: " + str(demofileCount) + "\nDo you like to start renaming?"
        
        dlg = wx.MessageDialog( self, MessageDlgText, "Really start", wx.CANCEL | wx.OK)
        
        if dlg.ShowModal() == wx.ID_OK:
            return True
        else:
            return  # the user changed idea...
        
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
        
    def OnError(self, e):
        # MessageDialog creation
        #MessageDlgText = "Error\n\n " + str(sys.exc_info()[0])
        MessageDlgText = ("OSError: {0}".format(e))
        dlg = wx.MessageDialog( self, MessageDlgText, "Error", wx.OK)       
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
        
def RenamingDemoFiles(ListSelection):
    file_failed = ""
    x = 0
    file_failed_counter = 0
    demofiles = glob.glob('*' + os.extsep + 'dem')
    demofileCount = len(demofiles)
    frame.GaugeProgress.SetRange(demofileCount)
    StartSelect = frame.OnStartRenaming(demofileCount)
    if StartSelect is not True:
        return
    frame.buttonStart.Disable()
    frame.buttonCancel.Disable()
    frame.ListBoxSelect.Disable()
    print ("Files found: " + str(demofileCount) + "\nStarting renaming..." + "\nIn progress please wait...")
    for file_source in demofiles:
        with open(file_source, 'r', errors='ignore') as fobj:
            for line in fobj:
                mapname = re.search(r"(?<=maps[\/\\]).+(?=\.bsp)", line)
                if mapname is not None:
                    break
        if mapname is not None:
            mapname = mapname.group()
            if '/' or '\\' in mapname:
                mapname = re.sub(r".+[\/\\]", '', mapname)
            mapname = ''.join([x for x in mapname if x in string.printable])
            demoname, ext = os.path.splitext(file_source)
            if ListSelection == 0:
                file_destination = demoname + "_" + mapname + ext
            elif ListSelection == 1:
                file_destination = mapname + "_" + demoname + ext
            elif ListSelection == 2:
                dt = os.path.getmtime(file_source)
                dt = datetime.datetime.fromtimestamp(dt).strftime('%Y-%m-%d')
                file_destination = dt + "_" + mapname + "_" + demoname + ext
            else:
                dt = os.path.getmtime(file_source)
                dt = datetime.datetime.fromtimestamp(dt).strftime('%Y-%m-%d')
                file_destination = dt + "_" + demoname + "_" + mapname + ext
            try:
                os.rename(file_source, file_destination)
            except OSError as e:
                frame.OnError(e)               
                print("OSError: {0}".format(e))
                frame.buttonStart.Enable()
                frame.buttonCancel.Enable()
                frame.ListBoxSelect.Enable()
                frame.GaugeProgress.SetValue(0)
                return
        else:           
            file_failed = file_failed + file_source + '\n'
            file_failed_counter += 1
        x += 1
        frame.GaugeProgress.SetValue(x)

    if file_failed:
        logfile_name = 'logfile_demo-file-renamer'
        logfile_ext = os.extsep + 'txt'
        logfile_text = """The following files aren't renamed because the map wasn't found in the demofile: \n\n""" + file_failed +  """\nWhat you can do: \n- Execute the demofile in your game or \n- Open the file in an editor and search for the word "maps" \n\nBe sure the demofile is a CS 1.6, CS:S, CS:GO or TF2 demofile."""
        if os.path.isfile(logfile_name + logfile_ext):
            logfile_counter = 2
            logfile_name_check =  logfile_name + "(" + str(logfile_counter) + ")" + logfile_ext
            while os.path.isfile(logfile_name_check) is True:
                logfile_counter += 1
                logfile_name_check =  logfile_name + "(" + str(logfile_counter) + ")" + logfile_ext
            logfile = open(logfile_name_check, 'x').write(logfile_text)
        else:
            logfile = open(logfile_name + logfile_ext, 'x').write(logfile_text)
        frame.OnFinishFailed(logfile_name, logfile_ext, file_failed_counter)
        print("Files failed to rename: " + str(file_failed_counter) + " of " + str(demofileCount) + "\nLogfile is generated, please look for further information in logfile: \"" + os.getcwd() +  os.sep + logfile_name + logfile_ext + "\"")
    else:
        frame.OnFinish()
        print("All files successfully renamed!")    
    frame.buttonStart.Enable()
    frame.buttonCancel.Enable()
    frame.ListBoxSelect.Enable()
    frame.GaugeProgress.SetValue(0)
    

PrgName = "Demo file renamer"
PrgVersion = "v1.05"
PytonVersion = sys.version
WxVersion = wx.__version__
IconPath = r"_ico\Demofile Renamer.ico"
app = wx.App(False)
frame = MainWindow(None, PrgName)
app.MainLoop()