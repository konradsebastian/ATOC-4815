import numpy as np
# file name, relative path
name='../dat/spn_17_08_21.dat'

# open text file to read
handle = open(name,'r')

# read all lines into list of strings "lines"
lines  = handle.readlines() # () tells python it's a function not an attribute --> execute
handle.close()

n = len(lines)
print("There are "+str(n)+" lines in file "+name+".")


# Loop over the lines in the file and read content
utc=[] # initialize list for times
tti=[] # initialize list for total irradiance
for line in lines:
    entries = line.split(",")
    # ";" is used as a comment in the data file
    if entries[0][0] != ';':
        utc.append(float(entries[0][0:2]) + \
                   float(entries[0][3:5])/60. + \
                   float(entries[0][6:8])/3600.)
        tti.append(float(entries[1]))  

utc = np.array(utc)
tti = np.array(tti)
index = np.where(utc < 5)
utc[index] = utc[index]+24.0

# Now do the plotting
import matplotlib.pyplot as plt
fig=plt.figure(figsize=[6,6]) 
plt.plot(utc,tti,'o',markersize=1) 
plt.xlabel('UTC [h]')
plt.xticks(np.linspace(12,24,7))
plt.ylabel('Irradiance [W m$^{-2}$ nm$^{-1}$]') 
plt.title('Solar Eclipse')
plt.show()




