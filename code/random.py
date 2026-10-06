import random
import numpy as np
    
def hidden(x,a=2,b=0.5,c=0.0):
    return(a+b*x+c*x*x)    

n     = 1000 # number of samples of the process
noise = 0.5 # noise (e.g., of an instrument)
xx = np.linspace(0,3,n)
yy = []
for i in range(n):
    r2=hidden(xx[i])+random.gauss(0,noise) # random.gauss(mean,std) or random.uniform(r-,r+)
    yy.append(r2)


import matplotlib.pyplot as plt
plt.plot(xx,yy,'o')

a,b=np.polyfit(xx,yy,1)
print(a,b)