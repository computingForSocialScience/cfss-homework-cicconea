import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
	artist_names = sys.argv[1:]
	print "input artists are ", artist_names
	artistList = []

	for name in artist_names:
		artID = fetchArtistId(name)
		artistList.append(artID) # generate a list of all artist names

	artistInfoDict = []
	albumDictList = []
	for identity in artistList: # indexing through artist IDs
		artistInfoDict.append(fetchArtistInfo(identity)) # create list of artist info dictionaries
		identityAlbumList = fetchAlbumIds(identity) # generate list of albums for artist identity
		for album in identityAlbumList:
			albumDictList.append(fetchAlbumInfo(album))

	writeArtistsTable(artistInfoDict) # write artist information to CSV
	writeAlbumsTable(albumDictList) # write album information to CSV


	plotBarChart()
