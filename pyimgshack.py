#!/usr/bin/python

# This is an image uploader that watches a directory for new files
# and uploades them directly to imageshack and displays a pop-up
# notification that contains the url for the image

# REQUIRED
# pyinotify
# zenity (linux package)

import sys, os, pyinotify, re
from pyinotify import WatchManager, Notifier, EventsCodes, ProcessEvent

#Define globals.
imageDir = '/home/moranjk/Pictures' # directory for images
   
#Define functions.
def uploadImage(img):
	tmp = "temp.data" #Temporary file filename.
	if re.search('png$', img):
		img = img+';type=image/png'

	os.system("curl -H Expect: -F fileupload=\"@" + img + "\" -F xml=yes -# \"http://www.imageshack.us/index.php\" > " + tmp)
	
	file = open(tmp, "r")
	content = file.read()
	os.system("rm " + tmp) #Remove temporary file.
	
	#Get the image link.
	start = content.find("<image_link>")
	end = content.find("</image_link>")
	link = content[start + 12 : end]			      
	os.system('zenity --info --text "' + link + '"')


class WatcherEvent(ProcessEvent):
	def process_IN_CREATE(self, event):
		uploadImage(os.path.join(event.path, event.name))


wm = WatchManager()

notifier = Notifier(wm, WatcherEvent())

wdd = wm.add_watch(imageDir, pyinotify.IN_CREATE, auto_add=True)

while True:
	try:
		notifier.process_events()
		if notifier.check_events():
			notifier.read_events()
	except KeyboardInterrupt:
		notifier.stop()
		break

