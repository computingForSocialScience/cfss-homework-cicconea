import sys
import requests
import csv
import json


"""Using the Spotify API search method, take a string that is the artist's name, 
and return a Spotify artist ID.
"""
def fetchArtistId(name):
	fullname = name.replace(" ", "%20")
	header = "https://api.spotify.com/v1/search?q="
	url = header + fullname + "&type=artist"
	req = requests.get(url)
	artistData = req.json()

	artistList = artistData["artists"]["items"]

	nameLength = len(name)
	diff = 1000000
	match = "No artist matches your search query"
	for artist in artistList:
		checkLength = len(artist["name"])
		if abs(checkLength - nameLength)<diff:
			diff = checkLength - nameLength
			match = artist["id"]

	return match

def fetchArtistInfo(artist_id):
	"""Using the Spotify API, takes a string representing the id and
	returns a dictionary including the keys 'followers', 'genres', 
	'id', 'name', and 'popularity'.
	"""
	infoDict = {}

	url = "https://api.spotify.com/v1/artists/" + artist_id
	req = requests.get(url)
	artistData = req.json()

	infoDict["followers"] = artistData["followers"]["total"]
	infoDict["genres"] = artistData["genres"]
	infoDict["id"] = artist_id
	infoDict["name"] = artistData["name"]
	infoDict["popularity"] = artistData["popularity"]

	return [infoDict]

identification = fetchArtistId(sys.argv[1])
print fetchArtistInfo(identification)










