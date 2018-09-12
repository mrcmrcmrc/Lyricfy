#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import requests
import os.path
import sys
import spotilib
from bs4 import BeautifulSoup
import Tkinter as tk
import tkMessageBox
from PIL import ImageTk, Image
import webbrowser

def resource_path(relative):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")),
                    relative)

cert_path = resource_path('cacert.pem')
os.environ["REQUESTS_CA_BUNDLE"] = cert_path

API_KEY = 'YOUR LAST.FM API KEY'

window = tk.Tk()
window.iconbitmap("icon\lyricfy.ico")
window.title("Lyricfy")
window.geometry("510x600")
window.configure(background='grey')
window.resizable(False, False)

canvas = tk.Canvas(window, width=500, height=160, bg="black")
canvas.grid(row=0, column=0, rowspan=2)

img = ImageTk.PhotoImage(Image.open("default.png").resize((200, 160), Image.ANTIALIAS))
label_img = tk.Label(window)
label_img.config(image = img, width = 200, height = 160)
label_img.grid(row=0, column=0, sticky = tk.W+tk.N, padx=1, pady=1, rowspan=2)

label_artist = tk.Label(window)
label_artist.config(width = 21, height=1, text="{0}".format("-"), font=("Times", 18, "italic"), padx=2)
label_artist.grid(row=0, column=0, sticky=tk.E)

label_song = tk.Label(window)
label_song.config(width=21, height=1, text="{0}".format("-"), font=("Times", 18, "italic"), padx=2)
label_song.grid(row=1, column=0, sticky=tk.E)

text_lyrics = tk.Text(window)
text_lyrics.tag_configure("center", justify='center')
scrollb = tk.Scrollbar(window)
text_lyrics.insert(tk.INSERT, "Lyricfy")
text_lyrics.tag_add("center", "1.0", "end")
text_lyrics.configure(state='disabled')
text_lyrics.config(font=("Times", 19),width=40, height=14, bg="darkgray", fg="black", selectbackground="lightgray", padx=2, pady=1, wrap=tk.WORD, spacing1=1)
text_lyrics.grid(row=5,column=0,rowspan=5,sticky=tk.W+tk.E)
scrollb.grid(row=5,column=0, rowspan=5, sticky=tk.W+tk.E+tk.N+tk.S)

scrollb.config(command=text_lyrics.yview)
text_lyrics.config(yscrollcommand=scrollb.set)



def removeSpecialCharacters(s):
	r=""
	for c in s:
		if c.isalnum():
			r = r + c
	return r



def getLyrics (artist, song):

	filters = ['(', '-']

	for f in filters:
		if f in song:
			song = song.split(f)[0]

	artist = removeSpecialCharacters(artist).lower()
	song = removeSpecialCharacters(song).lower()

	if artist.find('the') == 0:
		artist = artist.split('the',1)[-1]
	
	base_URL = "http://www.azlyrics.com/lyrics"
	url = "{0}/{1}/{2}.html".format(base_URL, artist, song)

	try:
		response = urllib2.urlopen(url, timeout=5);
	except:
		return False

	html = response.read()
	soup = BeautifulSoup(html,'html.parser')
	div = soup.find('div', {'class' : 'col-xs-12 col-lg-8 text-center'})
	divs = div.find_all('div')
	lyrics = divs[6].get_text()
	
	return lyrics



def getArtistImage (artist):
    params = {'method' : 'artist.getinfo', 'artist' : artist, 'api_key': API_KEY, 'format' : 'json'} 

    try:
        response = requests.post("https://ws.audioscrobbler.com/2.0/", data=params, timeout=5).json()
        
    except requests.exceptions.RequestException as e:
    	print e
    	return False

    if 'error' in response:
        print response['message']
        return False
    else:
    	img_url = response['artist']['image'][2]['#text']
    	img_data = requests.get(img_url).content
    	with open('images\{0}.png'.format(artist), 'wb') as handler:
    		handler.write(img_data)
    	return True



def execute():
	#artist = spotilib.artist()
	#song = spotilib.song()
	artist, song = spotilib.get_info_windows()
	
	label_artist.config(text="{0}".format(artist))
	label_song.config(text="{0}".format(song))
	
	lyrics = getLyrics(artist, song)
	
	if lyrics is False:
		lyrics = "NOTHING FOUND :("

	if not os.path.exists("images\{0}.png".format(artist)):
		if getArtistImage(artist):
			img_path = "images\{0}.png".format(artist)
		else:
			img_path = "default.png"
	
	else:
		img_path = "images\{0}.png".format(artist)

	with Image.open(img_path).resize((200, 160), Image.ANTIALIAS) as image_:
		img = ImageTk.PhotoImage(image_)
		label_img.configure(image = img)
		label_img.image = img
	
	text_lyrics.configure(state='normal')
	text_lyrics.delete("1.0", tk.END)
	text_lyrics.insert(tk.INSERT, lyrics)
	text_lyrics.tag_add("center", "1.0", "end")
	text_lyrics.config(font=("Times", 19), width=40, height=14, bg="darkgray", fg="black", selectbackground="lightgray", padx=4, pady=1, spacing1=1, wrap=tk.WORD)
	text_lyrics.configure(state='disabled')


button = tk.Button(window, text="SEARCH", command=execute, relief=tk.FLAT)
button.grid(row=2, column=0)

def translate():
	pass

def saveLyrics():
	try:
		with open("lyrics\{0}_{1}.txt".format(removeSpecialCharacters(spotilib.artist_info_windows().lower()), removeSpecialCharacters(spotilib.song_info_windows()).lower()), "w") as text_file:
			text_file.write("{0}".format(text_lyrics.get("1.0", tk.END)))

			tkMessageBox.showinfo("Saved", "Lyrics has been saved successfully...")
	except Exception as error:
		print error
		tkMessageBox.showinfo("Error", "Lyrics couldnt saved...")


def copy():
	window.clipboard_clear()
	window.clipboard_append(text_lyrics.selection_get())


def viewSourceCode():
	webbrowser.open_new(r"https://www.github.com/mrcmrcmrc/Lyricfy")


menu = tk.Menu(window, tearoff=0)
menu.config(bg="darkgray", activebackground="lightgray", relief=tk.GROOVE, title="Menu")
menu.add_command(label="Translate", state=tk.DISABLED, command=translate)
menu.add_command(label="Save Lyrics", command=saveLyrics)
menu.add_command(label="Copy", command=copy)
menu.add_separator()
menu.add_command(label="View Source Code", command=viewSourceCode)
menu.add_separator()
menu.add_command(label="Exit", command = window.quit)

def popup(event):
    menu.post(event.x_root, event.y_root)

# attach popup to frame
text_lyrics.bind("<Button-3>", popup)


window.mainloop()




