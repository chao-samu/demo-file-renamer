#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  ===================================================================================
#  Python Version ......: 3+
#  Version .............: 1.00-beta (Python)
#  Release Date ........: 2015-08-27
#  GitHub ..............: https://github.com/chao-samu/demo-file-renamer
#  Author ..............: chao-samu
# ------------------------------------------------------------------------------------
#  Script Name..........: demo file renamer
#  Description .........: Integrate mapname into demofile (*.dem).
#                         Support: TF2, CS 1.6, CS:S and CS:GO
#  License..............: MIT License (https://github.com/chao-samu/demo-file-renamer/blob/master/LICENSE)
#  ===================================================================================

from tkinter import *
from tkinter import filedialog
import re, os, os.path, glob, string



PrgName = "Demo file rename tool"
PrgVersion = "1.00-beta (Python)"
print(PrgName + " - Version " + PrgVersion + " - made by chao-samu\nRenaming Mask: OLDNAME_MAPNAME\nExample: 'samu-vs-ninja.dem' will be renamed to 'samu-vs-ninja_de_dust2.dem'")



root = Tk()
root.withdraw()
working_dir = filedialog.askdirectory()
os.chdir(working_dir)



file_failed = ''
demofiles = glob.glob('*.dem')
print ("Files found: " + str(len(glob.glob('*.dem'))) + "\nStarting renaming..." + "\nIn progress please wait...")
for file_source in demofiles:
	with open(file_source, 'r', errors='ignore') as fobj:
		for line in fobj:
			mapname = re.search(r"(?<=maps[\/\\]).+(?=\.bsp)",line)
			if mapname is not None:
				break
	if mapname is not None:
		mapname = mapname.group()
		mapname = ''.join(filter(lambda x: x in string.printable, mapname))	
		demoname, ext = os.path.splitext(file_source)		
		file_destination = demoname + "_" + mapname + ext
		os.rename(file_source, file_destination)
	else:
		file_failed = file_failed + file_source + '\n'
		

		
if file_failed:
	logfile_name = 'demofile_renamer'
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
	print("Some files failed to rename, logfile is generated, please look for further information in logfile " + os.getcwd() +  os.sep + logfile_name + logfile_ext)	
else:
	print("All files successfully renamed!")
input("Press any key to exit")
