from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import tempfile
import matplotlib
matplotlib.use('Agg') # this allows PNG plotting
import matplotlib.pyplot as plt
from capital_min_model import *
from func_gen import *
from mc import *
import pymysql

dbname="optimization"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8',unix_socket="/tmp/mysql.sock", port=3306)
cur = db.cursor()


app = Flask(__name__)


def addLatestRun(chartLabel, FLScale, period, alpha , nh, nl):
        lineTuple = (chartLabel, FLScale, period, alpha , nh, nl)
        paramsTableCreate = '''CREATE TABLE IF NOT EXISTS params (id INTEGER PRIMARY KEY AUTO_INCREMENT,chartLabel VARCHAR(100), FLScale INTEGER, period INTEGER, alpha INTEGER, nh INTEGER, nl INTEGER);'''
        cur.execute(paramsTableCreate)

        insertparamsQuery = '''INSERT INTO params (chartLabel, FLScale, period, alpha, nh, nl) VALUES (%s, %s,%s,%s,%s,%s);'''
        cur.execute(insertparamsQuery, lineTuple)
        db.commit()
        return



@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/

    return render_template('index.html')

@app.route('/documentation/')
def make_doc_resp():
    # this function just renders templates/documentation.html when
    # someone goes to http://127.0.0.1:5000/

    return render_template('documentation.html')





@app.route('/results/')
def make_results_resp():

	# get latest submission from sql database
	latestID = cur.lastrowid

	# get actual values vs tuples
	query = '''SELECT chartLabel FROM params WHERE id = %s'''
	cur.execute(query, latestID)
	val = cur.fetchall()
	chartLabel = val[0][0]

	query = '''SELECT FLScale FROM params WHERE id = %s'''
	cur.execute(query, latestID)
	val = cur.fetchall()
	FLScale = val[0][0]/100.0

	query = '''SELECT period FROM params WHERE id = %s'''
	cur.execute(query, latestID)
	val = cur.fetchall()
	period = val[0][0]

	query = '''SELECT alpha FROM params WHERE id = %s'''
	cur.execute(query, latestID)
	val = cur.fetchall()
	alpha = val[0][0]/100.0

	query = '''SELECT nh FROM params WHERE id = %s'''
	cur.execute(query, latestID)
	val = cur.fetchall()
	nh = val[0][0]

	query = '''SELECT nl FROM params WHERE id = %s'''
	cur.execute(query, latestID)
	val = cur.fetchall()
	nl = val[0][0]


	# call the solver via mc (MC sets up efficiency/cost trajectories, then calls the solver itself)
	H0, L0, minCost, solved, Hp, Hn, Lp, Ln = storeData(FLScale, period, alpha, nh, nl)

	# solved = 1 means that the solver was able to find an optimal solution. 
	# otherwise we should not trust the results
	if solved == 1:
		SolverStatus = "Model Solved Successfully "
	else: SolverStatus = "Model Not Solved Successfully "

	# adding the positive/negative values of investment. All investments initially set 
	# up to be positive, so this subtraction gives us the actual values of the solver 
	# as per the documentation page
	Hinvest = np.subtract(Hp, Hn)
	Linvest = np.subtract(Lp, Ln)

	# dates of investment - for investPlotPng only!
	dateRange = range(1, period+1)


	# what is total capital in each period?
	# follow capital accumulation formulas from documenation
	HKap = [H0]
	LKap = [L0]
	for i in range(1, period+1):
		HKap.append(HKap[i-1]* float(1 - 1/nh) + Hinvest[i-1])
		LKap.append(LKap[i-1]* float(1 - 1/nl) + Linvest[i-1])

	# generate matplotlib plot for investment
	fig = plt.figure(figsize=(8,6),dpi=100)
	axes = fig.add_subplot(1,1,1)
	# plot the data
	axes.plot(dateRange,Hinvest, label= "Dirty Capital Invesment")
	axes.plot(dateRange,Linvest, label= "Clean Capital Investment")

	# labels
	axes.set_xlabel('Years of Simulation')
	axes.set_ylabel('Investment ($)')
	axes.set_title(chartLabel + " Investment")
	plt.legend(loc = 0)

	# make the temporary file
	f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
	# save the figure to the temporary file
	plt.savefig(f)
	f.close() # close the file
	# get the file's name (rather than the whole path) (the template will need that)
	investPlotPng = f.name.split('/')[-1]



	kdateRange = range(period+1)



	# generate matplotlib plot for capital
	fig = plt.figure(figsize=(8,6),dpi=100)
	axes = fig.add_subplot(1,1,1)
	# plot the data
	axes.plot(kdateRange,HKap, label= "Dirty Capital Stock")
	axes.plot(kdateRange,LKap, label= "Clean Capital Stock")

	# labels
	axes.set_xlabel('Years of Simulation')
	axes.set_ylabel('Capital Stock ($)')
	axes.set_title(chartLabel + " Capital Stock")
	plt.legend(loc = 0)

	# make the temporary file
	f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
	# save the figure to the temporary file
	plt.savefig(f)
	f.close() # close the file
	# get the file's name (rather than the whole path) (the template will need that)
	capitalPlotPng = f.name.split('/')[-1]


	# get old queries so we can see what has been repeated
	query = '''SELECT chartLabel, FLScale, period, alpha, nh, nl FROM params ORDER BY id DESC'''
	cur.execute(query)
	oldParams = cur.fetchall()


	return render_template("results.html", investPlotPng=investPlotPng, minCost = minCost, SolverStatus = SolverStatus, oldParams = oldParams, capitalPlotPng=capitalPlotPng)



@app.route('/defineParameters/',methods=['GET','POST'])
def define_parameters():
    if request.method == 'GET':
        # This code executes when someone visits the page.
		# get old queries so we can see what has been repeated
		query = '''SELECT chartLabel, FLScale, period, alpha, nh, nl FROM params ORDER BY id DESC'''
		cur.execute(query)
		oldParams = cur.fetchall()

		return(render_template('defineParameters.html', oldParams=oldParams))
    
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        chartLabel = request.form['chartLabel']
        period = request.form['period']
        alpha = request.form['alpha']
        nh = request.form['nh']
        nl = request.form['nl']
        FlScale = request.form['FlScale']

        # add to SQL database
        addLatestRun(chartLabel, FlScale, period, alpha , nh, nl)

        return(redirect('/results/'))






if __name__ == '__main__':
    app.debug=True
    app.run()



