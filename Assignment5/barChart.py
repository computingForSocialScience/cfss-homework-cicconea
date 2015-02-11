import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    f_artists = open('artists.csv') # read in artists data
    f_albums = open('albums.csv') # read in album data

    # convert to csv object
    artists_rows = csv.reader(f_artists)
    albums_rows = csv.reader(f_albums) 

    # identify csv file headers
    artists_header = artists_rows.next() 
    albums_header = albums_rows.next()

    artist_names = []
    
    # we allow decades in range from 1990 to 2020 in increments of 10
    decades = range(1900,2020, 10)
    decade_dict = {} # create a dictionary of decades & initialize values = 0
    for decade in decades:
        decade_dict[decade] = 0
    
    for artist_row in artists_rows:
        if not artist_row: # ignoring header row
            continue
        artist_id,name,followers, popularity = artist_row # split out values from csv row
        artist_names.append(name) # call out the artist names specifically for use later

    for album_row  in albums_rows:
        if not album_row: # ignoring header row
            continue
        artist_id, album_id, album_name, year, popularity = album_row # split out values from csv row
        for decade in decades: # index through all decades in the range defined above
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)): # if the year of the album is within that decade
                decade_dict[decade] += 1 # increment the dictionary count of that decade by 1 to represent an album in that decade
                break

    x_values = decades # define the range of x axis labels - just the range of decades
    y_values = [decade_dict[d] for d in decades] # define the range of y axis labels - the frequency counts of each decade
    return x_values, y_values, artist_names # function returns future chart labels and artist names

def plotBarChart():
    x_vals, y_vals, artist_names = getBarChartData() # separating out the data from the 'getBarChartData' return
    
    fig , ax = plt.subplots(1,1) # generate a single plot with attributes fig and ax
    ax.bar(x_vals, y_vals, width=10) # set axes according to the correct decades/freqencies from the prior function
    ax.set_xlabel('decades') # set x axis label
    ax.set_ylabel('number of albums') # set y axis label
    ax.set_title('Totals for ' + ', '.join(artist_names)) # set title including all the artist names from artist csv file
    plt.show() # display plot
