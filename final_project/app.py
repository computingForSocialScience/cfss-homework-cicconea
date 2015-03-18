from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import tempfile
import matplotlib
matplotlib.use('Agg') # this allows PNG plotting
import matplotlib.pyplot as plt
from capital_min_model import *
from func_gen import *
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components
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



@app.route('/results/')
def make_results_resp():

	latestID = cur.lastrowid

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

	print chartLabel, FLScale, period, alpha, nh, nl

	minCost, solved, Hp, Hn, Lp, Ln = storeData(FLScale, period, alpha, nh, nl)

	print "Model Solved"
	# generate Bokeh HTML elements
	# create a `figure` object
	p = figure(title='A Bokeh plot',plot_width=500,plot_height=400)
	# add the line
	x = range(1, period+1)
	y = Hp
	p.line(x,y)
	# add axis labels
	p.xaxis.axis_label = "time"
	p.yaxis.axis_label = "size"
	# create the HTML elements
	figJS,figDiv = components(p,CDN)

	return render_template("results.html", y=y, figJS = figJS, figDiv = figDiv)



@app.route('/defineParameters/',methods=['GET','POST'])
def define_parameters():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('defineParameters.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        chartLabel = request.form['chartLabel']
        period = request.form['period']
        alpha = request.form['alpha']
        nh = request.form['nh']
        nl = request.form['nl']
        FlScale = request.form['FlScale']

        print chartLabel, period, alpha, nh, nl, FlScale


        addLatestRun(chartLabel, FlScale, period, alpha , nh, nl)

        return(render_template('defineParameters.html'))



@app.route('/fig/')
def fig(period, Hp):
    import StringIO

    fig = plt.figure(figsize=(5,4),dpi=100)
    axes = fig.add_subplot(1,1,1)
    # plot the data
    axes.plot(range(1, period+1), Hp)



    img = StringIO.StringIO()
    fig.savefig(img, format="png")
    img.seek(0)
    return send_file(img, mimetype='image/png')






if __name__ == '__main__':
    app.debug=True
    app.run()



