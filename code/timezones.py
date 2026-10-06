import datetime,pytz

# naive datetime
daylight=False
if daylight:
    d = datetime.datetime(2016,  6, 5, 1, 43, 45) # MDT
else:
    d = datetime.datetime(2016, 12, 5, 1, 43, 45) # MST

utc = pytz.UTC # UTC timezone
print('Naive        :',d)

# Convert to UTC timezone aware datetime
du = utc.localize(d) 
print('Aware        :',du,' tz',utc)

# show as in MT time zone (not converting here)
mt = pytz.timezone('America/Denver') # MT timezone
dc = du.astimezone(mt)
print('Disply as MT :',dc,' tz',mt) 

# show time difference between UTC and MT
tu=utc.localize(d) #10 utc
tm=mt.localize(d)  #10 mt  --> 16 utc (17 utc)
diff = (tm-tu).total_seconds()/3600. #16-10 (17-10) = 6(7)
print('MT-UTC       :',diff)

# Plotting against time
import matplotlib.pyplot as plt
d0 = datetime.datetime(2016,  6, 5, 1, 43, 45)
d1 = datetime.datetime(2016,  6, 6, 23, 43, 45)
plt.plot([d0,d1],[1,1],'ko--')
#plt.xticks([datetime.datetime(2016,  6, 5),datetime.datetime(2016,  6, 6),datetime.datetime(2016,  6, 7)])
plt.tight_layout()




