import pandas as pd
import numpy as np
import networkx as nx


def readEdgeList(filename):
	data = pd.read_csv(filename)

	if len(data.columns) > 2:
		print "more than two columns. Only first two columns returned"
		data = data[data.columns[0:2]]
	
	return data

def degree(edgeList, in_or_out):
	if in_or_out == "out":
		returnDegree = edgeList["artist"].value_counts()
	if in_or_out == "in":
		returnDegree = edgeList["relatedArtist"].value_counts()
	return returnDegree


def combineEdgeLists(edgeList1, edgeList2):
	edgeList1.columns = edgeList2.columns

	edgeListCombined = edgeList1.append(edgeList2)
	edgeListCombined = edgeListCombined.drop_duplicates()
	return edgeListCombined

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







