from artistNetworks import *
from analyzeNetworks import *
import sys
import pandas as pd
import numpy as np
import requests


def getRandomAlbum(artist_id):
	url = "https://api.spotify.com/v1/artists/" + artist_id + "/albums?album_type=album&market=US"
	req = requests.get(url)
	albumData = req.json()

	AlbumList = []

	if len(albumData["items"]) == 0:
		return ("", "")

	else:	
		for item in albumData["items"]:
			AlbumList.append((item["id"], item["name"]))

	if len(AlbumList) == 0:
		return ("", "")

	else: randIndex = np.random.choice(len(AlbumList))

	return AlbumList[randIndex]

def getRandomTrack(album_id):	
	if album_id  == "":
		return ""

	url = "https://api.spotify.com/v1/albums/"+ album_id + "/tracks"
	req = requests.get(url)
	albumData = req.json()

	albumData = albumData["items"]

	trackList = []
	for track in albumData:
		trackList.append(track["name"])

	randTrack = np.random.choice(trackList)

	return randTrack

def fetchArtistInfo(artist_id):
	url = "https://api.spotify.com/v1/artists/" + artist_id
	req = requests.get(url)
	artistData = req.json()

	return artistData["name"]




#artList = sys.argv[1:]


#tempList = pd.DataFrame()
#for art in artList:
#	tempList = combineEdgeLists(tempList, getEdgeList(art, 2))

#sample = pandasToNetworkX(tempList)
#counter = 1

#randomArtistList = []
#while counter <= 30:
#	randomArtistList.append(randomCentralNode(sample))
#	counter += 1

#artOutput = []
#for artist in randomArtistList:
#	albumID, albumName = getRandomAlbum(artist)
#	artTrack = getRandomTrack(albumID)
#	artistName = fetchArtistInfo(artist)
#	artOutput.append((artistName, albumName, artTrack))


#print artOutput

#artistOutput = np.array(artOutput, dtype=[('artist_name', 'a50'),('album_name', 'a100'),('track_name', 'a100')])
#dataToCSV = pd.DataFrame(artistOutput)
#dataToCSV.to_csv("playlist.csv",index=False)









