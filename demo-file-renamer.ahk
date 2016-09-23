; ===================================================================================
; AHK Version .........: 1.1.24.01
; Version .............: 1.04 (AHK)
; Release Date ........: 2016-09-23
; GitHub ..............: https://github.com/chao-samu/demo-file-renamer
; Author ..............: chao-samu
;------------------------------------------------------------------------------------
; Script Name..........: demo file renamer
; Description .........: Integrate mapname into demofile (*.dem).
;                        Support: TF2, CS 1.6, CS:S and CS:GO
; License..............: MIT License (https://github.com/chao-samu/demo-file-renamer/blob/master/LICENSE)
; ===================================================================================

#NoEnv
#NoTrayIcon
SendMode Input
SetWorkingDir %A_ScriptDir%

;############################### Programm Info ###############################
PrgName := "demo file renamer"
PrgVersion := "1.04 (AHK)"

;############################### OS Detections ###############################
If (A_PtrSize = 4)
{
	BitVersion := "x86"
}
else
{
	BitVersion := "x64"
}

;############################### Functions ###############################
ParsingDemofiles(RenamingMaskNumber, counter_files_quotient)
{
	Loop, Files, *.dem
	{
		counter_prog := counter_files_quotient * A_Index
		GuiControl,, ProgressBar, %counter_prog%
		mapstring := ""
		File := FileOpen(A_LoopFileName, "r")
		while !File.AtEOF
		{
			demofile := File.ReadLine()		
			RegExMatch(demofile, "maps[\/\\].+\.bsp", mapstring)
		If mapstring
		{
			File.Close()
			mapstring_formated := Format("{1:s}", mapstring)			
			continue
		}
		}
		If (InStr(mapstring_formated, "maps") and InStr(mapstring_formated, "bsp"))
		{
		RegExMatch(mapstring_formated, "(?<=maps[\/\\]).+(?=\.bsp)", Mapname)
		Mapname := Format("{1:s}", Mapname)
			If (InStr(Mapname, "/") or InStr(Mapname, "\"))
			{
				Mapname := RegExReplace(Mapname, ".+[\/\\]", "")
			}
			SplitPath, A_LoopFileName,,,, FileNameNoExt
			If (RenamingMaskNumber = 3) or (RenamingMaskNumber = 4)
			{
				FormatTime, mod_date, %A_LoopFileTimeModified%, yyyy-MM-dd
			}
			RenamingMask := []
			RenamingMask[1] := filelist . A_LoopFileName . "`t" . FileNameNoExt . "_" . Mapname . "." . A_LoopFileExt . "`n"
			RenamingMask[2] := filelist . A_LoopFileName . "`t" . Mapname . "_" . FileNameNoExt . "." . A_LoopFileExt . "`n"
			RenamingMask[3] := filelist . A_LoopFileName . "`t" . mod_date . "_" . Mapname . "_" . FileNameNoExt . "." . A_LoopFileExt . "`n"
			RenamingMask[4] := filelist . A_LoopFileName . "`t" . mod_date . "_" . FileNameNoExt . "_" . Mapname . "." . A_LoopFileExt . "`n"
			filelist := RenamingMask[RenamingMaskNumber]
		}
		else
		{
			filelist_failed := filelist_failed . A_LoopFileName . "`n"
			counter_failed += 1
		}
	}
	return [filelist, filelist_failed, counter_failed]
}

;############################### GUI ###############################
Menu, helpmenu, Add, Help , MenuHelp
Menu, helpmenu, Add
Menu, helpmenu, Add, About, MenuAbout
Menu, topmenu, Add, &Help, :helpmenu
Gui, Menu, topmenu

Gui, Add, Button, x12 y180 w90 h20 , Cancel
Gui, Add, Button, x212 y180 w90 h20 , Start
Gui, Add, Text, x12 y120 w290 h20 vtext_prog, Extracting mapname
Gui, Add, ListBox, x12 y30 w290 h30 vRenamingMaskNumber AltSubmit gpressListBox, OLDNAME_MAPNAME||MAPNAME_OLDNAME|YYYY-MM-DD_MAPNAME_OLDNAME|YYYY-MM-DD_OLDNAME_MAPNAME
Gui, Add, Text, x12 y10 w290 h20 , Choose renaming mask
Gui, Add, Text, x12 y70 w290 h40 vtext_example, Example: `n"samurai-vs-ninja.dem" will be renamed to "samurai-vs-ninja_de_dust2.dem"

Gui, Add, Progress, x12 y140 w290 h10 Backgroundsilver vProgressBar
; Generated using SmartGUI Creator for SciTE
Gui, Show, w323 h221, %PrgName%
return

MenuHelp:
Gui, Help:+owner1
Gui +Disabled
Gui, Help:Add, Text,,
((
What can do this Tool?
This tool was manly made to extract out the mapname of
GoldSrc- and Source Engine demofiles and place it in the name of the demofile itself.

Which kind of demofiles this tool can handle?
Currently this tool support Counter-Strike 1.6, Counter-Strike Source,
Counter-Strike Global Office and Team Fortress 2 demofiles.

How to use?
1. Select your renaming mask you want
2. Press start and select in the following window your folder with the supported demofiles
    (please note, all demofiles with the ending "dem" in this folder will be renamed, subfolder
    are not included).
    In a protected folder (like "ProgramFiles") you have to start this program in admin mode!
3. Press OK and wait until you will hopefully be happy :)
)
Gui, Help:Add, Button, Default, OK
Gui, Help:Show, w450 h240, Help
return

MenuAbout:
Gui, About:+owner1
Gui +Disabled
Gui, About:Add, Link,, %PrgName% - Version %PrgVersion% `n`nTool compiled with: AHK %A_AhkVersion% %BitVersion% `n`nLook for updates:`n<a href="https://github.com/chao-samu">https://github.com/chao-samu</a>`n`nMade by chao-samu
Gui, About:Add, Text, r9 vMeinEdit, 
(

:::::::::::::::::::::::::::::::::::::::::This software is provided under the following License:::::::::::::::::::::::::::::::::::::::::
---------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
)
Gui, About:Add, Button, Default, OK
Gui, About:Show, w540 h490, About
return

HelpButtonOK:
HelpGuiClose:
HelpGuiEscape:
AboutButtonOK:
AboutGuiClose:
AboutGuiEscape:
Gui, 1:-Disabled
Gui Destroy
return

pressListBox:
	Gui, Submit, NoHide
	if (RenamingMaskNumber = 1)
	GuiControl,, text_example, Example: `n"samurai-vs-ninja.dem" will be renamed to "samurai-vs-ninja_de_dust2.dem"
	else if (RenamingMaskNumber = 2)
	GuiControl,, text_example, Example: `n"samurai-vs-ninja.dem" will be renamed to "de_dust2_samurai-vs-ninja.dem"
	else if (RenamingMaskNumber = 3)
	GuiControl,, text_example, Example: `n"samurai-vs-ninja.dem" will be renamed to "2007-05-03_de_dust2_samurai-vs-ninja.dem"
	else
	GuiControl,, text_example, Example: `n"samurai-vs-ninja.dem" will be renamed to "2007-05-03_samurai-vs-ninja_de_dust2.dem"
return

;############################### MAIN Programm ###############################
ButtonStart:
FormatTime, current_time
ParsingDemofiles.Delete(1, 3)
folder_demofiles := ""
filelist := ""
filelist_failed := ""
counter_files := ""
counter_failed := ""
counter_successfully := ""
logfile_counter := 1
GuiControl, Disable, Start
GuiControl, Disable, RenamingMaskNumber
GuiControlGet, RenamingMaskNumber
FileSelectFolder, folder_demofiles,, 0, Please select your folder where your demofiles are. `nAll files with the ending *.dem will be renamed.
if ErrorLevel=0
{
	SetWorkingDir %folder_demofiles%
	Loop, Files, *.dem
	{
		counter_files += 1
	}
	If counter_files
	{
		counter_files_quotient := 100 / counter_files
		ParsingInfo := ParsingDemofiles(RenamingMaskNumber, counter_files_quotient)
		filelist := ParsingInfo[1]
		filelist_failed := ParsingInfo[2]
		counter_failed := ParsingInfo[3]
		GuiControl, Disable, Cancel
		GuiControl,, text_prog, Renaming Files
		Loop, Parse, filelist, `n
		{
			 filelist_array := StrSplit(A_LoopField, A_Tab)
			 Source := filelist_array[1]
			 Destination := filelist_array[2]
			 FileMove, %Source%, %Destination%
		}
		If filelist_failed
		{
			logfile_name := "demo-file-renamer_logfile.txt"
			logfile := "Renaming from " current_time " in " A_WorkingDir " `n`nThe following files aren't renamed because the map wasn't found in the demofile: `n`n" . filelist_failed . "`n`nWhat you can do: `n- Execute the demofile in your game or `n- Open the file in an editor and search for the word ""maps"" `n`nBe sure the demofile is a CS 1.6, CS:S, CS:GO or TF2 demofile."
			IfExist, %A_ScriptDir%\%logfile_name%
			{
			filetrue := "A"
				while filetrue
				{
				logfile_counter +=1
				logfile_name := "demo-file-renamer_logfile(" . logfile_counter . ").txt"
				filetrue := FileExist(A_ScriptDir . "\" . logfile_name)
				}
				FileAppend, %logfile%, %A_ScriptDir%\%logfile_name%
			}
			else
			{
				FileAppend, %logfile%, %A_ScriptDir%\%logfile_name%
			}

			counter_successfully := counter_files - counter_failed
			logfile_path := A_ScriptDir . "\" . logfile_name
			msgbox % counter_successfully " out of " counter_files " files were successfully renamed. `n" "There are " counter_failed " that aren't renamed. `n`nLogfile is generated, please look for further information in logfile: `n" logfile_path
		}
		else
		{
			MsgBox, 0, , All demofiles successfully renamed!
		}
		GuiControl,, ProgressBar, 0
		GuiControl,, text_prog, Extracting mapname
		GuiControl, Enable, RenamingMaskNumber
		GuiControl, Enable, Cancel
		GuiControl, Enable, Start
		return
	}
	else
	{
		MsgBox % "No files found!"
		GuiControl,, ProgressBar, 0
		GuiControl, Enable, RenamingMaskNumber
		GuiControl, Enable, Cancel
		GuiControl, Enable, Start
		return
	}
}
else
{
	GuiControl,, ProgressBar, 0
	GuiControl, Enable, RenamingMaskNumber
	GuiControl, Enable, Start
	return
}

ButtonCancel:
GuiClose:
ExitApp