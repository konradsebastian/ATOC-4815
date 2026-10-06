import matplotlib.pyplot as plt
import matplotlib.image as mpimg

png = '../dat/boulder_1km.png'
wesn=[-105.9669,-104.2169,39.5081,40.8300]
# Load image
img = mpimg.imread(png)

#Make plot of WorldVIEW background
plt.close('all')
plt.figure('GRID',figsize=[7,7])
plt.imshow(img,extent=wesn)
plt.scatter(-105.27,40,color='red')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
