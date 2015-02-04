import csv
import sys
import matplotlib.pyplot as plt



def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


# Write a Python function get_avg_latlng() that computes the average latitude and longitude of 
# construction permits in Hyde Park and prints it to the console.

def get_avg_latlng():
	lines = readCSV("permits_hydepark.csv") # reading only HP locations
	count = 0.0
	HPlong = 0.0
	HPlat = 0.0
	for line in lines:
		HPlong += float(line[-2]) 
		HPlat += float(line[-3])
		count += 1.0
	return HPlat/count, HPlong/count


# Write another Python function zip_code_barchart() that plots and saves as a .jpg a bar chart of 
# contractor zip codes.

def zip_code_barchart():
	lines = readCSV("permits_hydepark.csv")
	contractorZip = {}
	for line in lines: # only the lines below are zip code lines
		zips = [line[28], line[35], line[42], line[49], line[56], line[63], line[70], line[77], line[84], line[91], line[98], line[105], line[112], line[119], line[126]]
		for zipcode in zips:
			if zipcode == "": continue	# if that particular line is empty (not all items use all 15 contractors)
			zipcode = zipcode.split("-") #get rid of sub-zip information. We want top-level zips only
			zipcode = zipcode[0] # second part of above
			if zipcode not in contractorZip: # add zip to dictionary
				contractorZip[zipcode] = 1
			else: contractorZip[zipcode] += 1

	plt.bar(range(len(contractorZip)), contractorZip.values(), align='center')
	plt.xticks(range(len(contractorZip)), contractorZip.keys(), rotation=25)

	#plt.show()
	plt.savefig('zipcodesHist.jpg')



# Using the contents of the value sys.argv[1], write a combined script that either (1) prints the mean 
# latitude and longitude to the console if given the command-line argument latlong (i.e., python parse.py 
# latlong) or (2) creates the histogram if given the command-line argument hist (i.e., python parse.py 
# hist).

if sys.argv[1] == "latlong":
	print get_avg_latlng()
elif sys.argv[1] == "hist":
	zip_code_barchart()
else: print "Command not understood; 'latlong' or 'hist' are only valid commands "
























