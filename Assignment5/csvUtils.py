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
				writeString = writeString + '"' + unicode(dictionary[key]) + '"' + unicode(",")
			else:
				writeString = writeString + unicode(dictionary[key]) + unicode(",")

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
				writeString = writeString + '"' + unicode(dictionary[key]) + '"' + unicode(",")
			else:
				writeString = writeString + unicode(dictionary[key]) + unicode(",")

		f.write(writeString)

	f.close()



	pass

#artDict = [{'genres': [u'garage rock'], 'popularity': 82, 'followers': 1319880, 'id': u'7mnBLXK823vNxN3UWB7Gfz', 'name': u'The Black Keys'}]

#testDict = [{'popularity': 73, 'artist_id': u'7mnBLXK823vNxN3UWB7Gfz', 'year': u'2010', 'name': u'Brothers', 'album_id': u'7qE6RXYyz5kj5Tll7mJU0v'}, {'popularity': 62, 'artist_id': u'7mnBLXK823vNxN3UWB7Gfz', 'year': u'2008', 'name': u'Attack & Release', 'album_id': u'1YHS3Fw8THvsKVVQ1znAqi'},{'popularity': 58, 'artist_id': u'7mnBLXK823vNxN3UWB7Gfz', 'year': u'2006', 'name': u'Magic Potion', 'album_id': u'4jFfuHyKmhGeipjRmKIh8O'},{'popularity': 60, 'artist_id': u'7mnBLXK823vNxN3UWB7Gfz', 'year': u'2004', 'name': u'Rubber Factory', 'album_id': u'6OphQUjIBIZHXzugkjMjxz'},{'popularity': 58, 'artist_id': u'7mnBLXK823vNxN3UWB7Gfz', 'year': u'2003', 'name': u'Thickfreakness', 'album_id': u'1BicwqogYc0pnMIH3tr0cM'},{'popularity': 59, 'artist_id': u'7mnBLXK823vNxN3UWB7Gfz', 'year': u'2002', 'name': u'The Big Come Up', 'album_id': u'7DDMtj3GwKJ8HHBm18OdKT'}]

#writeAlbumsTable(testDict)
#writeArtistsTable(artDict)





