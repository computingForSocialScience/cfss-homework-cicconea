from io import open

def writeArtistsTable(artist_info_list):
	"""Given a list of dictionaries, each as returned from 
	fetchArtistInfo(), write a csv file 'artists.csv'.

	The csv file should have a header line that looks like this:
	ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
	"""
	f = open("artists.csv", mode="w")
	f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')

	itList = ["id", "name", "followers", "popularity"]
	for dictionary in artist_info_list:
		writeString = unicode("")
		for key in itList:
			if key == "popularity":
				writeString = writeString + unicode(dictionary[key]) + unicode("\n")
			elif key == "name":
				writeString = writeString + '"' + unicode(dictionary[key]) + '"'
			else:
				writeString = writeString + unicode(dictionary[key]) + unicode(",")

		print writeString
		f.write(writeString)

	f.close()


	pass 
      
def writeAlbumsTable(album_info_list):
	"""
	Given list of dictionaries, each as returned
	from the function fetchAlbumInfo(), write a csv file
	'albums.csv'.

	The csv file should have a header line that looks like this:
	ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
	"""
	pass

testDict = [{'genres': [u'garage rock'], 'popularity': 82, 'followers': 1319841, 'id': u'7mnBLXK823vNxN3UWB7Gfz', 'name': u'The Black Keys'}]

writeArtistsTable(testDict)