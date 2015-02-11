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

	f = open("albums.csv", mode="w")
	f.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')

	itList = ["artist_id", "album_id", "name", "year", "popularity"]
	for dictionary in album_info_list:
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




testDict = [{'popularity': 15, 'artist_id': u'2BTZIqw0ntH9MvilQ3ewNY', 'year': u'1983', 'name': u"She's So Unusual", 'album_id': '0sNOF9WDwhWunNAHPD3Baj'}]
writeAlbumsTable(testDict)






