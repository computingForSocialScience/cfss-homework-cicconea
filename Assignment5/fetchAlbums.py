import requests
from datetime import datetime
import sys

def fetchAlbumIds(artist_id):
	"""Using the Spotify API, take an artist ID and 
	returns a list of album IDs in a list
	"""

	url = "https://api.spotify.com/v1/artists/" + artist_id + "/albums?album_type=album&market=US"
	req = requests.get(url)
	albumData = req.json()

	AlbumList = []
	for item in albumData["items"]:
		AlbumList.append(item["id"])

	return AlbumList

def fetchAlbumInfo(album_id):
	"""Using the Spotify API, take an album ID 
	and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
	"""
	
	url = "https://api.spotify.com/v1/albums/" + album_id
	req = requests.get(url)
	albumData = req.json()

	AlbumDict = {}

	AlbumDict["artist_id"] = albumData["artists"][0]["id"]
	AlbumDict["album_id"] = album_id
	AlbumDict["name"] = albumData["name"]
	AlbumDict["year"] = albumData["release_date"][0:4]
	AlbumDict["popularity"] = albumData["popularity"]

	return AlbumDict

info = fetchAlbumIds(sys.argv[1])
for album in info:
	print fetchAlbumInfo(album)
