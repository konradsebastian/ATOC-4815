import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

png = '../dat/test.png'
wesn=[-105.7756,-105.7006,46.0743,46.1252]
# Load image
img = mpimg.imread(png)

# Make plot of WorldVIEW background
plt.imshow(img,extent=wesn)
plt.xlim(wesn[0]-0.01,wesn[1]+0.01)
plt.ylim(wesn[2]-0.01,wesn[3]+0.01)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
#
## Assign lat/lon grid to WordVIEW image
nx=img.shape[1]
ny=img.shape[0]

## for nx pixels, we have nx+1 boundaries
x=np.linspace(wesn[0],wesn[1],nx+1) # nx+1 boundaries from W to E
y=np.linspace(wesn[2],wesn[3],ny+1) # ny+1 boundaries from S to N
#
xm = (x[1:]+x[:-1])*0.5 # x mid-points (nx)
ym = (y[1:]+y[:-1])*0.5 # y mid-points (ny)

# overplot one row of mid-points
plt.scatter(np.repeat(xm[0],ny),ym,color='green')

# assignment 1: plot boundaries between columns
for i,x0 in enumerate(x):
    plt.plot(np.repeat(x0,ny+1),y,'r-')

# assignment 2: 'grid' new data
# selected lon/lat point (to be gridded)
xs=-105.7368
ys=  46.093

#xind = int((xs-wesn[0])/(x[1]-x[0]))
#yind = int((ys-wesn[2])/(y[1]-y[0]))

# Hint (from mid term)
xind = np.argmin(np.abs(x-xs))
yind = np.argmin(np.abs(y-ys))

print(xind,yind)
plt.scatter(xs,ys,color='blue')
plt.scatter(x[xind],y[yind],color='red')
plt.scatter(xm[xind],ym[yind],color='green')
green_at_grid_cell = img[ny-1-yind,xind,2]
print(green_at_grid_cell)
