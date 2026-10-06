import numpy as np
import matplotlib.pyplot as plt

def gaussian(x, mu, sigma):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sigma, 2.)))

x  = np.random.normal(loc=3.14, scale=1, size=100)

sd = np.std(x)
mu = np.mean(x)
print('loc,scale',mu,sd)

plt.close('all')
h,b,p=plt.hist(x,100,label='Histogram')
mx=np.max(h)

xx=np.arange(0,10,0.01)

plt.plot(xx,gaussian(xx,mu,sd)*mx,label='Gaussian')
plt.plot([mu,mu],[0,mx],'--',label='$\mu$ (best estimate)')
plt.plot([mu-sd,mu+sd],[mx/2,mx/2],'--',label='$\pm \sigma$')
plt.xlim(mu-5*sd,mu+5*sd)
plt.xlabel("Measurement",fontsize=18)
plt.ylabel("Counts",fontsize=18)
plt.legend()

plt.show()
