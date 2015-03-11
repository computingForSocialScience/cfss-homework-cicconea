from flask import Flask, render_template, request, redirect, url_for
import pymysql
from artistNetworks import *
from analyzeNetworks import *
from makePlaylist import *
from fetchArtist import *

dbname="playlists"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

cur = db.cursor()

app = Flask(__name__)


def createNewPlaylist(artist):
    artistID = fetchArtistId(artist)
    tempList = getEdgeList(artistID, 2)
    sample = pandasToNetworkX(tempList)
    counter = 1

    randomArtistList = []
    while counter <= 30:
        randomArtist = randomCentralNode(sample)
        if getRandomAlbum(randomArtist) == "":
            continue
        randomArtistList.append(randomArtist)
        counter += 1

 
    playlistsTableCreate = '''CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(100));'''
    songsTableCreate = '''CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER, songOrder INTEGER, artistName VARCHAR(255), albumName VARCHAR(255), trackName VARCHAR(255));'''

    cur.execute(playlistsTableCreate)
    cur.execute(songsTableCreate)

    insertArtistQuery = '''INSERT INTO playlists (rootArtist) VALUES (%s);'''
    cur.execute(insertArtistQuery, artist)

    latestID = cur.lastrowid

    songOrder = 1
    playList = []
    for songArtist in randomArtistList:
        albumID, albumName = getRandomAlbum(songArtist)
        artTrack = getRandomTrack(albumID)
        artistName = fetchArtistInfo(songArtist)

        lineTuple = (latestID, songOrder, artistName, albumName, artTrack)
        
        songOrder += 1
        playList.append(lineTuple)


    insertSongQuery = '''INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES (%s, %s, %s, %s, %s)'''
    cur.executemany(insertSongQuery, playList)
    db.commit()




@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():

    cur.execute("SELECT * FROM playlists;")
    playlists = cur.fetchall()

    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):

    query = '''SELECT songOrder, artistName, albumName, trackName 
        FROM songs WHERE playlistId = %s ORDER BY songOrder'''
    cur.execute(query, playlistId)
    songs = cur.fetchall()

    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']

        createNewPlaylist(artistName)

        return(redirect("/playlists/"))



if __name__ == '__main__':
    app.debug=True
    app.run()



