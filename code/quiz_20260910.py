def mean_and_var(l):
    s=0
    n=0
    for e in l:
        s=s+e
        n=n+1
    m=s/float(n)
    
    s=0
    for e in l:
        s=s+(e-m)**2
    v = float(1/(n-1))*s
    return(m,v)  
            
my_numbers = [1,2,3,4,5,6,7,8,9]
print(mean_and_var(my_numbers)[0])
#import numpy
#print(numpy.mean(my_numbers),numpy.std(my_numbers,ddof=1)**2)
