import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = mpimg.imread('../dat/tatra.png')

plt.close('all') # close all previous figures in case some are open
plt.figure('Picture') # instead of 'Picture', we could have used a window number
plt.imshow(img)
plt.plot([573,573],[0,1000],'w--')

plt.figure('Line')
plt.plot(img[:,573,0]/np.mean(img[:,573,0:3],axis=1),label='red/total')
plt.ylim(0,3)
plt.legend()

rflt = np.where(img[:,:,0]/np.mean(img[:,:,0:3],axis=2)>1.25)

red=img[:,:,0]
grn=img[:,:,1]
blu=img[:,:,2]
opc=np.zeros_like(blu) # opacity (1=opaque, 2=transparent)
opc[rflt]=1
blu[rflt]=1
red[rflt]=0
grn[rflt]=0

new_img=np.stack([red,grn,blu,opc],axis=2)
plt.figure('new')
plt.imshow(new_img)
plt.imsave('../dat/tatra_red.png',new_img)










