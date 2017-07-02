#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  =================================================================================================
#  Python Version ......: 3.*
#  Version .............: 1.11 (Python)
#  Release Date ........: 2017-07-02
#  GitHub ..............: https://github.com/chao-samu/demo-file-renamer
#  Author ..............: chao-samu
# --------------------------------------------------------------------------------------------------
#  Script Name..........: demo file renamer
#  Description .........: Integrate mapname into demofile (*.dem).
#                         Support: TF2, CS 1.6, CS:S and CS:GO
#  License..............: MIT License
#                         (https://github.com/chao-samu/demo-file-renamer/blob/master/LICENSE)
#  =================================================================================================


import wx
import datetime, glob, os, os.path, re, string, sys, textwrap, threading


# ADDITIONAL EVENTS FOR THREAD "DemoFileRenamer" ===================================================
myEVT_GUIENABLE = wx.NewEventType()
EVT_GUIENABLE = wx.PyEventBinder(myEVT_GUIENABLE, 1)
class GUIEnableEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)

myEVT_GUIDISABLE = wx.NewEventType()
EVT_GUIDISABLE = wx.PyEventBinder(myEVT_GUIDISABLE, 1)
class GUIDisableEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)

myEVT_GAUGESETRANGE = wx.NewEventType()
EVT_GAUGESETRANGE = wx.PyEventBinder(myEVT_GAUGESETRANGE, 1)
class GaugeSetRangeEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, demofileCount):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._demofileCount = demofileCount

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._demofileCount

myEVT_GAUGEPROGRESS = wx.NewEventType()
EVT_GAUGEPROGRESS = wx.PyEventBinder(myEVT_GAUGEPROGRESS, 1)
class GaugeProgressEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, x):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._gaugeProgress = x

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._gaugeProgress

myEVT_FINISH = wx.NewEventType()
EVT_FINISH = wx.PyEventBinder(myEVT_FINISH, 1)
class FinishEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)

myEVT_FINISHFAILED = wx.NewEventType()
EVT_FINISHFAILED = wx.PyEventBinder(myEVT_FINISHFAILED, 1)
class FinishFailedEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, logfile_name, logfile_ext, file_failed_counter):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._logfile_name = logfile_name
        self._logfile_ext = logfile_ext
        self._file_failed_counter = file_failed_counter

    def GetValues(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return (self._logfile_name, self._logfile_ext, self._file_failed_counter)

myEVT_ONERROR = wx.NewEventType()
EVT_ONERROR = wx.PyEventBinder(myEVT_ONERROR, 1)
class OnErrorEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, errorMessage):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._errorMessage = errorMessage

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._errorMessage

# GUI ==============================================================================================
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(345,330), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # programm variables
        self.PrgName = title
        self.PrgVersion = "v1.11"
        self.PytonVersion = sys.version
        self.WxVersion = wx.__version__
        IconPath = "_ico" + os.sep + "Demofile Renamer.ico"

        # init variables
        self.ListSelection = 0
        self.CheckBoxSelection = False
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
        menuHelp = helpmenu.Append(wx.ID_HELP, '&Help', 'Show help dialog')
        menuSeperator = helpmenu.AppendSeparator()
        menuLicense = helpmenu.Append(wx.ID_VIEW_DETAILS, "&License", "Show license dialog") # should use wx.newid()
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

        self.ListBoxSelect = wx.ListBox(panel, -1, choices=["OLDNAME_MAPNAME", "MAPNAME_OLDNAME", \
        "YYYY_MAPNAME_OLDNAME", "YYYY_OLDNAME_MAPNAME", "YYYY-MM_MAPNAME_OLDNAME", \
        "YYYY-MM_OLDNAME_MAPNAME", "YYYY-MM-DD_MAPNAME_OLDNAME", "YYYY-MM-DD_OLDNAME_MAPNAME"], \
        size=(270,35),pos=(30,40))

        self.StaticTextExample = wx.StaticText(panel, -1, textExample,(30,80))
        wx.StaticText(panel, -1, "Extracting mapname",(30,150))
        self.GaugeProgress = wx.Gauge(panel, -1, range=100, pos=(30,170),size=(270,10))
        self.checkboxMode = wx.CheckBox(panel, -1, "Parsing full demofile (processing intense)",  pos=(30,190), size=(270,15))
        self.buttonCancel = wx.Button(panel, -1, "Cancel", (30,218),(90,20))
        self.buttonStart = wx.Button(panel, -1, "Start", (210,218),(90,20))

        # Preselect default settings
        self.ListBoxSelect.SetSelection(0)

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnHelp, menuHelp)
        self.Bind(wx.EVT_MENU, self.OnLicense, menuLicense)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_LISTBOX, self.OnListSelect, self.ListBoxSelect)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxSelect, self.checkboxMode)
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.buttonStart)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.buttonCancel)

        # Set events (DemoFileRenamer thread handling only)
        self.Bind(EVT_GUIENABLE, self.OnGuiEnable)
        self.Bind(EVT_GUIDISABLE, self.OnGuiDisable)
        self.Bind(EVT_GAUGESETRANGE, self.OnGaugeSetRange)
        self.Bind(EVT_GAUGEPROGRESS, self.OnGaugeProgress)
        self.Bind(EVT_FINISH, self.OnFinish)
        self.Bind(EVT_FINISHFAILED, self.OnFinishFailed)
        self.Bind(EVT_ONERROR, self.OnError)

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

        Options Info:
        Parsing full demofile: This option is recommended for old demofiles (CS 1.6 etc.),
        because it was able to record into the same file when a mapchange occur. So the hole
        file have to be read to detect all played maps in one file. This was fixed in newer
        games (CS:GO etc.), so it isn't necessary there. Use this option if you are unsure.
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

        Copyright (c) 2017 chao-samu

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
        MessageDlgText = self.PrgName + ":\n" + self.PrgVersion + "\n\nBased on Python version:\n" + \
        self.PytonVersion + "\n\nGUI made with wxPython version:\n" + self.WxVersion + "\n\nMade by chao-samu" + \
        "\nLook for updates: https://github.com/chao-samu"

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
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "2007_de_dust2_samurai-vs-ninja.dem"'
            self.StaticTextExample.SetLabel(textExample)
        elif self.ListSelection == 3:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "2007_samurai-vs-ninja_de_dust2.dem"'
            self.StaticTextExample.SetLabel(textExample)
        elif self.ListSelection == 4:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "2007-05_de_dust2_samurai-vs-ninja.dem"'
            self.StaticTextExample.SetLabel(textExample)
        elif self.ListSelection == 5:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "2007-05_samurai-vs-ninja_de_dust2.dem"'
            self.StaticTextExample.SetLabel(textExample)
        elif self.ListSelection == 6:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "2007-05-03_de_dust2_samurai-vs-ninja.dem"'
            self.StaticTextExample.SetLabel(textExample)
        else:
            textExample = 'Example:\n "samurai-vs-ninja.dem" will be renamed to\n "2007-05-03_samurai-vs-ninja_de_dust2.dem"'
            self.StaticTextExample.SetLabel(textExample)

    def OnCheckBoxSelect(self, event):
        self.CheckBoxSelection = event.IsChecked()

    def OnStart(self, event):
        saveDirDialog = wx.DirDialog(self, "Please select your folder where your demofiles are.\n" \
        "All files with the ending *.dem will be renamed.", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if saveDirDialog.ShowModal() == wx.ID_OK:
            os.chdir(saveDirDialog.GetPath())

            StartSelect = self.StartRenaming()
            if StartSelect is True:
                # start thread
                worker = DemoFileRenamer(self, self.ListSelection, self.CheckBoxSelection)
                worker.start()
        else:
            return     # the user changed idea...

    def StartRenaming(self):
        # MessageDialog creation
        MessageDlgText = "Files found: " + str(len(glob.glob('*.dem'))) + "\nDo you like to start renaming?"
        dlg = wx.MessageDialog( self, MessageDlgText, "Really start", wx.CANCEL | wx.OK)

        if dlg.ShowModal() == wx.ID_OK:
            return True
        else:
            return  # the user changed idea...

        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnCancel(self, event):
        self.Close()

    # EVENTS FOR "DemoFileRenamer" THREAD  ---------------------------------------------------------
    def OnGuiEnable(self, evt):
        self.buttonStart.Enable()
        self.buttonCancel.Enable()
        self.ListBoxSelect.Enable()
        self.GaugeProgress.SetValue(0)

    def OnGuiDisable(self, evt):
        self.buttonStart.Disable()
        self.buttonCancel.Disable()
        self.ListBoxSelect.Disable()

    def OnGaugeSetRange(self, evt):
        self.GaugeProgress.SetRange(evt.GetValue())

    def OnGaugeProgress(self, evt):
        self.GaugeProgress.SetValue(evt.GetValue())

    def OnFinish(self, evt):
        # MessageDialog creation
        MessageDlgText = "All files successfully renamed!"

        dlg = wx.MessageDialog( self, MessageDlgText, "Success", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnFinishFailed(self, evt):
        logfile_name, logfile_ext, file_failed_counter = evt.GetValues()
        # MessageDialog creation
        MessageDlgText = "Files failed to rename: " + str(file_failed_counter) + " of " + \
        str(len(glob.glob('*.dem'))) + "\nLogfile is generated, please look for further information in logfile: \"" + \
        os.getcwd() +  os.sep + logfile_name + logfile_ext + "\""

        dlg = wx.MessageDialog( self, MessageDlgText, "Partitial success", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnError(self, evt):
        # MessageDialog creation
        # MessageDlgText = "Error\n\n " + str(sys.exc_info()[0])
        MessageDlgText = ("OSError: {0}".format(evt.GetValue()))
        dlg = wx.MessageDialog( self, MessageDlgText, "Error", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

# MAIN FUNCTION (THREADED) =========================================================================
class DemoFileRenamer(threading.Thread):
    def __init__(self, parent, ListSelection, CheckBoxSelection):
        """
        @param parent: The gui object that should recieve the value
        @param value: value to 'calculate' to
        """
        threading.Thread.__init__(self)
        self._parent = parent
        self.ListSelection = ListSelection
        self.CheckBoxSelection = CheckBoxSelection

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """

        # INIT VARIABLES ---------------------------------------------------------------------------
        mapname = ""
        all_mapnames = []
        file_failed = ""

        count_index = 0 # for all_mapnames
        count_gauge_prg = 0
        count_file_failed = 0

        # LOOKING FOR DEM FILES --------------------------------------------------------------------
        demofiles = glob.glob('*' + os.extsep + 'dem')
        demofileCount = len(demofiles)

        # PREPARE GUI ------------------------------------------------------------------------------
        evt = GaugeSetRangeEvent(myEVT_GAUGESETRANGE, -1, demofileCount)
        wx.PostEvent(self._parent, evt)

        evt = GUIDisableEvent(myEVT_GUIDISABLE, -1)
        wx.PostEvent(self._parent, evt)

        print ("Files found: " + str(demofileCount) + "\nStarting renaming..." + "\nIn progress please wait...")

        # START: MAIN ------------------------------------------------------------------------------
        for file_source in demofiles:
            # START: OPEN FILE AND ITERATE IT LINE BY LINE (SEARCH MAPNAME) ------------------------
            with open(file_source, 'r', errors='ignore') as fobj:
                for line in fobj:
                    mapname = re.search(r"(?<=maps[\/\\]).+(?=\.bsp)", line)
                    if mapname is not None:
                        mapname = mapname.group()
                        if '/' or '\\' in mapname:
                            mapname = re.sub(r".+[\/\\]", '', mapname)
                            mapname = ''.join([x for x in mapname if x in string.printable])
                        if self.CheckBoxSelection is True:
                            if count_index == 0:
                                all_mapnames.append(mapname)
                                count_index += 1
                            else:
                                if mapname == all_mapnames[count_index-1]:
                                    continue
                                else:
                                   all_mapnames.append(mapname)
                                   count_index += 1
                        else:
                            break
            # END: OPEN FILE AND ITERATE IT LINE BY LINE (SEARCH MAPNAME) --------------------------

            # START: HANDLE RESULT (PREPARE VAR, RENAME FILE, EXCEPTION HANDLING) ------------------
            if self.CheckBoxSelection is True:
                mapname = '+'.join(all_mapnames)
                del all_mapnames[:]
                count_index = 0

            if mapname is not None:
                if all_mapnames is not None:
                    for n in all_mapnames:
                        mapname = mapname + n
                demoname, ext = os.path.splitext(file_source)
                if self.ListSelection == 0:
                    file_destination = demoname + "_" + mapname + ext
                elif self.ListSelection == 1:
                    file_destination = mapname + "_" + demoname + ext
                elif self.ListSelection == 2:
                    dt = os.path.getmtime(file_source)
                    dt = datetime.datetime.fromtimestamp(dt).strftime('%Y')
                    file_destination = dt + "_" + mapname + "_" + demoname + ext
                elif self.ListSelection == 3:
                    dt = os.path.getmtime(file_source)
                    dt = datetime.datetime.fromtimestamp(dt).strftime('%Y')
                    file_destination = dt + "_" + demoname + "_" + mapname + ext
                elif self.ListSelection == 4:
                    dt = os.path.getmtime(file_source)
                    dt = datetime.datetime.fromtimestamp(dt).strftime('%Y-%m')
                    file_destination = dt + "_" + mapname + "_" + demoname + ext
                elif self.ListSelection == 5:
                    dt = os.path.getmtime(file_source)
                    dt = datetime.datetime.fromtimestamp(dt).strftime('%Y-%m')
                    file_destination = dt + "_" + demoname + "_" + mapname + ext
                elif self.ListSelection == 6:
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

                    evt = OnErrorEvent(myEVT_ONERROR, -1, e)
                    wx.PostEvent(self._parent, evt)

                    print("OSError: {0}".format(e))

                    evt = GUIEnableEvent(myEVT_GUIENABLE, -1)
                    wx.PostEvent(self._parent, evt)
                    return
            else:
                file_failed = file_failed + file_source + '\n'
                file_failed_count += 1
            count_gauge_prg += 1

            evt = GaugeProgressEvent(myEVT_GAUGEPROGRESS, -1, count_gauge_prg)
            wx.PostEvent(self._parent, evt)
            # END: HANDLE RESULT (PREPARE VAR, RENAME FILE, EXCEPTION HANDLING) --------------------
        # END: MAIN --------------------------------------------------------------------------------

        # START: FINISH (RESULT MESSAGES, LOG, GUI-UNLOCK) -----------------------------------------
        if file_failed:
            logfile_name = 'logfile_demo-file-renamer'
            logfile_ext = os.extsep + 'txt'
            logfile_text = """The following files aren't renamed because the map wasn't found in the demofile: \n\n""" + file_failed + \
            """\nWhat you can do: \n- Execute the demofile in your game or \n- Open the file in an editor and search for the word "maps" \n\nBe sure the demofile is a CS 1.6, CS:S, CS:GO or TF2 demofile."""
            if os.path.isfile(logfile_name + logfile_ext):
                logfile_counter = 2
                logfile_name_check =  logfile_name + "(" + str(logfile_counter) + ")" + logfile_ext
                while os.path.isfile(logfile_name_check) is True:
                    logfile_counter += 1
                    logfile_name_check =  logfile_name + "(" + str(logfile_counter) + ")" + logfile_ext
                logfile = open(logfile_name_check, 'x').write(logfile_text)
            else:
                logfile = open(logfile_name + logfile_ext, 'x').write(logfile_text)

            evt = FinishFailedEvent(myEVT_FINISHFAILED, -1, logfile_name, logfile_ext, countfile_failed)
            wx.PostEvent(self._parent, evt)

            print("Files failed to rename: " + str(count_file_failed) + " of " + str(demofileCount) + \
            "\nLogfile is generated, please look for further information in logfile: \"" + os.getcwd() + \
            os.sep + logfile_name + logfile_ext + "\"")

        else:
            evt = FinishEvent(myEVT_FINISH, -1)
            wx.PostEvent(self._parent, evt)
            print("All files successfully renamed!")

        evt = GUIEnableEvent(myEVT_GUIENABLE, -1)
        wx.PostEvent(self._parent, evt)
        # END: FINISH (RESULT MESSAGES, LOG, GUI-UNLOCK) -----------------------------------------

# wxPython window loop
app = wx.App(False)
frame = MainWindow(None, "demo file renamer")
app.MainLoop()