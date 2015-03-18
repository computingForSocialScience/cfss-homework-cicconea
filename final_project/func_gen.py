import math
from scipy.stats import norm, truncnorm
import matplotlib.pyplot as plt

# generates a k-length log growth list w/ initial base and decay mod (mod must be negative)
# add minimum to allow a theoretical limit to efficiency/carbon intensity



def logGen(k, base, mod, maximum):
	returnList = [base]
	for i in range(1, k):
		number = base * math.log(mod*i) + base
		if number > maximum:
			number = maximum
		returnList.append(number)
	return returnList

# generates a k-length exponential decay list w/ initial base and decay mod (mod must be negative)
# add minimum to allow a theoretical limit to efficiency/carbon intensity

def expGen(k, base, mod, minimum):
	returnList = []
	for i in range(k):
		number = base * math.exp(mod*i)
		if number < minimum:
			number = minimum
		returnList.append(number)
	return returnList			

# generates a k-length list w/ intercept base and slope mod
# add minimum to allow a theoretical limit to efficiency/carbon intensity
def linGen(k, base, mod, minimum=0, maximum=1):
	returnList = []
	for i in range(k):
		number = base + mod*i
		if number < minimum:
			number = minimum
		if number > maximum:
			number = maximum
		returnList.append(number)
	return returnList			

# generates a k-length list of constant values = base
def consGen(k, base):
	returnList = []
	for i in range(k):
		random = truncGaussian(base, 0, 1)
		returnList.append(base)
	return returnList


def truncGaussian(var, a, b):
	x = truncnorm.rvs(a,b)
	#print x
	return (1+x)*var


def Gaussian(var):
	return norm.rvs()*var


# mean, scale are positive, increasing is boolean and minVal/maxVal are limits of
# logistic curve. randomAllowed is boolean for adding random noise to simulation
def logistic(k, initial, increasing, randomAllowed, scale = 0.5, minVal= 0, maxVal=1):
	returnList = [initial]	

	if randomAllowed == True:
		scale = truncGaussian(scale, 0, 5)
	
	if increasing == True:
		priorY = initial - minVal
		diff = maxVal - minVal
		for i in range(1, k):
			dpdt = scale*priorY*(1-(priorY/diff))
			appendY = dpdt + priorY
			returnList.append(appendY + minVal)
			priorY = appendY        

	if increasing == False:
		priorY = maxVal - initial
		diff = maxVal - minVal
		for i in range(1, k):
			dpdt = scale*priorY*(1-(priorY/diff))
			appendY = priorY + dpdt
			returnList.append(maxVal - appendY)
			priorY = appendY


    
	return returnList





