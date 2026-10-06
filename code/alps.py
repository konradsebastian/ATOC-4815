import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('../dat/tatra.png')

#plt.close('all') # close all previous figures in case some are open
plt.figure('Picture') # instead of 'Picture', we could have used a window number
plt.imshow(img)

f2=plt.figure('Statistics',figsize=[10,5])
plt.hist(img[:,:,0].flatten(),bins=30) #,label='green channel',color='green')
#plt.hist(img[:,:,0].flatten(),label='red channel',color='red',histtype='step')
#plt.hist([img[:,:,2].flatten(),img[:,:,0].flatten()],color=['blue','red'],label=['blue ch.','red ch.'])
#plt.legend()

plt.figure('Line')
plt.plot(img[:,1340,2],color='blue')
plt.plot(img[:,1340,1],color='green')
plt.plot(img[:,1340,0],color='red')

