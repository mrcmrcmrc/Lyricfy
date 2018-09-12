from distutils.core import setup
import py2exe
import requests.certs
 
setup(
#console=['lyricfy.py'], konsolu gizlemek icin. bunu yazarsan alttakine gerek yok.
windows=[{"script": "lyricfy.py",
"icon_resources": [(1, "lyricfy.ico")]}],
data_files=[('',[requests.certs.where()])],
name = "Lyricfy",
version = "0.1",
description = "lyrics viewer for Spotify",
options = {'build_exe': {
"include_files": ["cacert.pem"],
}},
)
