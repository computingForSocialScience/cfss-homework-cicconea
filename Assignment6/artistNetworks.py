import requests
import sys
import time
import pandas as pd
import numpy as np

def getRelatedArtists(artistID):
	url = "https://api.spotify.com/v1/artists/" + artistID + "/related-artists"
	req = requests.get(url)
	relatedArtists = req.json()

	relArtistList = []
	for relatedArtist in relatedArtists["artists"]:
		relArtistList.append(str(relatedArtist["id"]))

	return relArtistList



def getDepthEdges(artistID, dep):

	depth = int(dep) # ensure any data we get is integer form. Otherwise while loop will break
	if depth <= 0: return [artistID] # 0th node is just artist ID. Anything less will still get that back

	searchList = getRelatedArtists(artistID)
	edgeList = [] # list of directed tuples to return
	count = 1 # to index depth

	for artist in searchList: #initial sublist
		edgeList.append((artistID, artist))
	
	updateList = []

	while count < depth:
		for artist in searchList:
			time.sleep(0.5) #try not to overload the spotify servers
			subSearchList = getRelatedArtists(artist) # get related artists to 'artist'
			for subArt in subSearchList: # for all related artists, create edge record 
				edgeList.append((artist, subArt)) 
				updateList.append(subArt) # and add related artist to next iteration to track. 

		count +=1
		searchList = updateList # refresh the new set of artist IDs to be searched in next iteration
		updateList = []	# clear updatelist

	return set(edgeList)


def getEdgeList(artistID, depth):
	res = list(getDepthEdges(artistID, depth))
	result = np.array(res, dtype=[('artist', 'a50'),('relatedArtist', 'a50')])
	
	return pd.DataFrame(result)


def writeEdgeList(artistID, depth, filename):
	dataToCSV = getEdgeList(artistID, depth)
	dataToCSV.to_csv(filename,index=False)
	return


#getEdgeList(sys.argv[1], int(sys.argv[2]), sys.argv[3])





