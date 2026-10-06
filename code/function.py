import urllib.request
import numpy as np

def download(url):
    # open URL to read
    urlhandle = urllib.request.urlopen(url)
    
    # read all lines into list of strings "lines"
    lines = urlhandle.readlines()
    
    # close the handle
    urlhandle.close()
    
    # lines came back as bytes, so convert each one to a string
    lines = [line.decode("utf-8") for line in lines]
    
    # Loop over the lines in the file
    utc=[] # initialize list for times
    tti=[] # initialize list for radiation
    for line in lines:
        entries = line.split(',')
        #print(entries);quit()
        if entries[0][0] != ';':
            utc.append(float(entries[0][0:2]) + \
                       float(entries[0][3:5])/60. + \
                       float(entries[0][6:8])/3600.)
            tti.append(float(entries[1]))      
    
    # Append +24 hours if data was measured on next day
    utc=np.array(utc)
    next_day=np.where(utc < 7) # This is not quite clean, cut off at locat midnight
    utc[next_day]=utc[next_day]+24.
    
    return utc,tti