import matplotlib.pyplot as plt
import numpy as np

xx=np.linspace(-10,10,100)

yy=np.sin(xx)

# Make figure
f = plt.figure(0)
plt.plot(xx,yy,'b--')
plt.xlabel('x')
plt.ylabel('y')
plt.title('I am a sine function.')


# select and plot three points on curve

