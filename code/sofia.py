"""
Sofia experiment with PI
"""

import matplotlib.pyplot as plt
import numpy as np

pi=3.141592653

i = ['pot','ladybug', 'lid']
d = [ 6,29,10]  # measured diameter
c = [17,92,30]   # measured circumference

d=np.array(d)
c=np.array(c)

#plt.plot(d,c,'go',label='measured')
#plt.plot([0,30],[0,pi*30],'k--',label='pi*diameter')
#plt.legend()

plt.plot(i,c/d,'ko')
plt.plot(i,[pi,pi,pi],'k--')
