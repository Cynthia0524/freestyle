import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import cvxopt as opt
from cvxopt import blas, solvers
import csv

def read_prices(file_path):
    port_price = list(csv.reader(open(file_path)))
    port_price = np.delete(np.asmatrix(port_price),(0),axis=1)
    port_price = np.delete(np.asmatrix(port_price),(0),axis=0)
    port_price = port_price.astype(np.float)
    return port_price

def get_return(prices):
	prices = np.array(prices)
	stock_return = prices[1:]/prices[:-1]-1
	return stock_return

def possible_portfolios(returns,n_port):
	#randomly generate n weights
	n_asset = len(returns.T)
	weights = []
	for i in range(n_port):
		w = np.random.rand(n_asset)
		weights.append(w/sum(w))
	weights = np.matrix(weights)

	#calculate the random returns and risks
	#assume: returns for each asset is a column vector
	returns = returns.T
	expect_return = np.matrix(np.mean(returns,axis = 1)) #here we get a row vector
	covariance = np.cov(returns)
	port_returns = []
	port_risks = []
	for row in weights:
		returns = float(row * expect_return.T)
		risks = float(np.sqrt(row * covariance * row.T))
		while(risks > 0.03):
			w = np.random.randn(n_asset)
			w = np.asmatrix(w/sum(w))
			returns = float(w * expect_return.T)
			risks = float(np.sqrt(w * covariance * w.T))
		port_returns.append(np.array(returns))
		port_risks.append(np.array(risks))
	return port_risks, port_returns

def	efficient_frontier(returns):
	n_asset = len(returns.T)
	returns = np.asmatrix(returns.T)
	#Assume
	#returns of each asset is a column vector
	#rq_returns only contains the smallest and biggest ones

	#this parameter should be adjusted according to characteristics of different database
	parameter = 1.8
	N = 100
	mus = [10**(5 * t/N - 1.0 + parameter) for t in range(N)]

	covariance = opt.matrix(np.cov(returns))
	expect_return = opt.matrix(np.mean(returns,axis = 1))

    #Constraint Matrices
	G = -opt.matrix(np.eye(n_asset))
	h = opt.matrix(0.0,(n_asset,1))
	A = opt.matrix(1.0,(1,n_asset))
	b = opt.matrix(1.0)

    #Optimization
	ef_frontier = [solvers.qp(mu*covariance, -expect_return, G, h, A, b)['x'] for mu in mus]
	ef_returns = [blas.dot(expect_return,x) for x in ef_frontier]
	ef_risks = [np.sqrt(blas.dot(x,covariance*x)) for x in ef_frontier]
	m1 = np.polyfit(ef_returns, ef_risks, 2)
	x1 = np.sqrt(m1[2] / m1[0])
    #ef_weights = solvers.qp(opt.matrix(x1 * covariance), -expect_return, G, h, A, b)['x']
	ef_weights = []
	for x in ef_frontier: ef_weights.append(list(x))

	return ef_risks, ef_returns, np.asarray(ef_weights)

def sharpe_ratio(ef_weights,returns,rf):
	#Assume:
	#returns: n_observs * n_asset
	#ef_weights: row as weights
	expect_return = np.asmatrix(np.mean(returns.T,axis = 1))
	covariance = np.asmatrix(np.cov(returns.T))
	ef_weights = np.asmatrix(ef_weights)
	ratios = []
	for weight in ef_weights:
		sp = (weight*expect_return.T-rf)/np.sqrt(weight*covariance*weight.T)
		ratios.append(float(sp))
	tangency_index, max_sp = max(enumerate(ratios),key = operator.itemgetter(1))

	return max_sp, tangency_index
