# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:46:06 2015

@author: PAVILION
"""
import io
import base64

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import LogLocator

from bottle import Bottle, run, response, static_file, request, route, template

r_value = 0
app = Bottle()
output1 = io.BytesIO()
output2 = io.BytesIO()
# Generate ticks
def weibull_CDF(y, pos):
    return "%G %%" % (100*(1-np.exp(-np.exp(y))))
y_formatter = FuncFormatter(weibull_CDF)
x_formatter = FuncFormatter(lambda x, pos: np.exp(x))
x_locator = LogLocator(2)

import scipy.stats as stats # scipy is a statistical package for Python
# Use Scipy's stats package to perform least-squares fit
def plot_linreg1(x,y):
    global output1
    # y = slope * x + intercept
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    #line = slope*x+intercept
    yt_F = np.array([ 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5,
           0.6, 0.7, 0.8, 0.9, 0.95, 0.99])
    yt_lnF = np.log(-np.log(1-yt_F))
    xt_F = np.power(10, np.arange(8))
    xt_lnF = np.log(xt_F)
    fig = plt.figure()    
    fig,ax = plt.subplots()
    plt.yticks(yt_lnF)
    plt.xticks(xt_lnF)
    ax.yaxis.set_major_formatter(y_formatter)
    ax.xaxis.set_major_formatter(x_formatter)
    #ax.xaxis.set_major_locator(x_locator)
    plt.xlim(1)
    plt.scatter(x,y)
    #plt.plot(x,line)
    plt.title("Weibull Cumulative Distribution Function", weight='bold')
    plt.grid()
    fig.savefig(output1,format="jpeg");
    output1.seek(0)
    print("R^2: {}".format(r_value**2))
    print("Shape:{} Scale:{}".format(slope, np.exp(-intercept/slope)))
    return slope, np.exp(-intercept/slope)

def plot_linreg2(x,y):
    global output2
    global r_value
    # y = slope * x + intercept
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    line = slope*x+intercept
    yt_F = np.array([ 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5,
           0.6, 0.7, 0.8, 0.9, 0.95, 0.99])
    yt_lnF = np.log(-np.log(1-yt_F))
    xt_F = np.power(10, np.arange(8))
    xt_lnF = np.log(xt_F)
    fig = plt.figure()    
    fig,ax = plt.subplots()
    plt.yticks(yt_lnF)
    plt.xticks(xt_lnF)
    ax.yaxis.set_major_formatter(y_formatter)
    ax.xaxis.set_major_formatter(x_formatter)
    #ax.xaxis.set_major_locator(x_locator)
    plt.xlim(1)
    plt.scatter(x,y)
    plt.plot(x,line)
    plt.title("Weibull Cumulative Distribution Function\nLinear Regression - Least Squares Method", weight='bold')
    #plt.title("Linear Regression - Least Squares Method", weight='bold')
    plt.grid()
    fig.savefig(output2,format="jpeg");
    output2.seek(0)
    print("R^2: {}".format(r_value**2))
    print("Shape:{} Scale:{}".format(slope, np.exp(-intercept/slope)))
    return slope, np.exp(-intercept/slope)
    
def reliability(t, loc, scale, shape):
    return (np.exp(-((t - loc)/scale)**shape))
    
def reliable_life(r, loc, scale, shape):
    return (loc + (scale*((-np.log(r))**(1/shape))))
    
def median_rank(n):
    return (np.arange(1, n+1)-0.3)/(n+0.4)
    
#calculate location (t0_hat) by way of Zanakis [1992]
def p(n):
    return (0.8829*n**(-0.3437))
    
def t0_hat(x):
    n = len(x) - 1
    j = np.ceil(n * p(n)) - 1
    t1 = x[0]
    tn = x[n]
    tj = x[j]
   
    return (t1*tn-tj**2)/(t1 + tn - 2*tj)
    
def weibull_scale_transform(data):
    x = np.log(data)    
    y = np.log(-np.log(1 - median_rank(len(data))))
    return x, y

@route("/process", method='POST')    
def process():
    #tfail = np.array ([101, 172, 184, 274, 378, 704, 1423, 2213, 2965, 5208, 5879, 6336, 6428, 6630, 7563, 10435, 30138, 30580, 38265, 47413, 81607, 158007, 182958])
    data = request.files.upload
    dataString = data.file.read().decode("utf-8")
    dataArray = dataString.split("\n")
    tfail = np.array([float(i) for i in dataArray])
    #tfail = np.loadtxt("Fail_data.csv")
    x1, y1 = weibull_scale_transform(tfail)
    t0 = t0_hat(tfail)
    x2, y2 = weibull_scale_transform(tfail - t0)
    shape1, scale1 = plot_linreg1(x1,y1)
    print ("Reliability: {}".format (reliability(tfail, 0, scale1, shape1)))
    shape2, scale2 = plot_linreg2(x2,y2)
    r = reliability(tfail, t0, scale2, shape2)
    print ("Location:{}".format(t0))  
    print ("Reliability: {}".format (reliability(tfail, t0, scale2, shape2)))
    print ("Reliable Life: {}".format (reliable_life(r,t0, scale2, shape2)))
    html = """<html><body> 
    <img src="data:image/png;base64,{0}"/> 
    <img src="data:image/png;base64,{1}"/>
    <br>
    R^2 = {2} <br>
    Shape Parameter = {3} <br>
    Scale Parameter = {4} <br>
    Location Parameter = {5} <br>
    <div style='float:left;border-style:solid'>
        Reliability <br> {6} 
    </div>    
    <div style='float:left;border-style:solid'>
        Reliable Life <br> {7} 
    </div>
    </body></html>""".format(base64.encodebytes(output1.getvalue()).decode(), base64.encodebytes(output2.getvalue()).decode(), (r_value**2), scale2, shape2, t0, "<br>".join(map(str, reliability(tfail, t0, scale2, shape2))), "<br>".join(map(str, reliable_life(r,t0, scale2, shape2))))
    plt.close()
    return html
    
@route("/")
def index():
    return template('template')
    
@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/views/'))
  
'''  
#test_calc()
run(host ='localhost', port=8080, debug=True)
'''

    