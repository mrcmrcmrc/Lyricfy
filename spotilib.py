#python2
# -*- coding: utf-8 -*-
import win32gui
import win32api
import os

###Virtual-KeyCodes###
Media_Next = 0xB0
Media_Previous = 0xB1
Media_Pause = 0xB3 ##Play/Pause
Media_Mute = 0xAD



###SpotifyInfo###
def get_info_windows():
    windows = []
        
    # Older Spotify versions - simply FindWindow for "SpotifyMainWindow"
    windows.append(win32gui.GetWindowText(win32gui.FindWindow("SpotifyMainWindow", None)))

    # Newer Spotify versions - create an EnumHandler for EnumWindows and flood the list with Chrome_WidgetWin_0s
    def find_spotify_uwp(hwnd, windows):
        text = win32gui.GetWindowText(hwnd)
        if win32gui.GetClassName(hwnd) == "Chrome_WidgetWin_0" and len(text) > 0:
            windows.append(text)
    
    win32gui.EnumWindows(find_spotify_uwp, windows)

    while windows.count != 0:
        try:
            text = windows.pop()
        except:
            return "Error", "Nothing playing"
        try:
            artist, track = text.split(" - ",1)
            return artist, track
        except:
            pass

def artist_info_windows():
	try:
		artist, track = get_info_windows()
		return artist
	except:
		return "There is nothing playing at this moment"

            

def song_info_windows():
	try:
		artist, track = get_info_windows()
		return track
	except:
		return "There is nothing playing at this moment"

    

def getwindow(Title="SpotifyMainWindow"):
	window_id = win32gui.FindWindow(Title, None)
	return window_id
	
def song_info():
	try:
		song_info = win32gui.GetWindowText(getwindow())
	except:
		pass
	return song_info

def artist():
	try:
		temp = song_info()
		artist, song = temp.split("-",1)
		artist = artist.strip()
		return artist
	except:
		return "There is noting playing at this moment"
	
def song():
	try:
		temp = song_info()
		artist, song = temp.split("-",1)
		song = song.strip()
		return song
	except:
		return "There is noting playing at this moment"
	
###SpotifyBlock###
def createfolder(folder_path="C:\SpotiBlock"):
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
	else:
		pass
	
def createfile(file_path="C:\SpotiBlock\Block.txt" ):
	if not os.path.exists(file_path):
		file = open(file_path, "a")
		file.write("ThisFirstLineWillBeIgnoredButIsNecessaryForUse")

def blocklist(file_path="C:\SpotiBlock\Block.txt"):
	block_list = []
	for line in open(file_path, "r"):
		if not line == "":
			block_list.append(line.strip())
	return block_list
	
def add_to_blocklist(file_path="C:\SpotiBlock\Block.txt"):
	with open(file_path, 'a') as text_file:
		text_file.write("\n" + song_info())
		
def reset_blocklist(file_path="C:\SpotiBlock\Block.txt"):
	with open(file_path, 'w') as text_file:
		text_file.write("ThisFirstLineWillBeIgnored")
		pass
	
	

	
###Media Controls###
def hwcode(Media):
	hwcode = win32api.MapVirtualKey(Media, 0)
	return hwcode

def next():
	win32api.keybd_event(Media_Next, hwcode(Media_Next))
	
def previous():
	win32api.keybd_event(Media_Previous, hwcode(Media_Previous))
	
def pause():
	win32api.keybd_event(Media_Pause, hwcode(Media_Pause))
	
def play():
	win32api.keybd_event(Media_Pause, hwcode(Media_Pause))
	
def mute():
	win32api.keybd_event(Media_Mute, hwcode(Media_Mute))

print artist()