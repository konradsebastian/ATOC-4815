"""
Here we will learn how to:
    * read, write an image (two ways)
    * take image apart
    * put image together again
    * manipulate an image pixel-by-pixel (detection of features)
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = mpimg.imread('../dat/alps.png')

red = img[:,:,0]
grn = img[:,:,1]
blu = img[:,:,2]

index = np.where((red > 0.6))

grn[index]=0
blu[index]=0

newimg = np.stack([red,grn,blu],axis=2)
plt.imshow(newimg)
# Now make those pixels with clouds transparent and save to file.
#plt.savefig('../dat/alps_savefig.png')
#mpimg.imsave('../dat/alps_imsave.png',img)
