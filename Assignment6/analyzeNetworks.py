import pandas as pd
import numpy as np
import networkx as nx


def readEdgeList(filename):
	data = pd.read_csv(filename)

	if len(data.columns) > 2:
		print "more than two columns. Only first two columns returned"
		data = data[data.columns[0:2]]
	
	return data



readEdgeList("testEdges.csv")

def degree(edgeList, in_or_out):
	if in_or_out == "in":
		returnDegree = edgeList['relatedArtist'].value_counts()
	elif in_or_out == "out":
		returnDegreee = edgeList['artist'].value_counts()
	else: returnDegree = 0

	return returnDegree

def combineEdgelists(edgeList1, edgeList2):
	edgeList1 = edgeList1.append(edgeList2)
	edgeList1.drop_duplicates()
	return edgeList1

def pandasToNetworkX(edgeList):
	g = nx.DiGraph()
	for artist,relatedArtist in edgeList.to_records(index=False):
 		g.add_edge(artist,relatedArtist)
	return g

def randomCentralNode(inputDiGraph):
	eigenDict = nx.eigenvector_centrality(inputDiGraph)
	norm = sum(eigenDict.values())
	for key in eigenDict:
		eigenDict[key] = eigenDict[key]/float(norm)

	randomNode = np.random.choice(eigenDict.keys(), p = eigenDict.values())

	return randomNode


#edges = readEdgeList("testEdges.csv")
#graph = pandasToNetworkX(edges)


#print randomCentralNode(graph)















