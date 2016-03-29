import numpy as np
import math
import matplotlib.pylab as plt

#Eerst importeren en de -9991 eruit halen.

lijst=np.delete(np.genfromtxt('/Users/jorisvanlammeren/Documents/Studie/Scriptie/JorisVLammeren/Data/Svalbard_BS_input.txt',usecols=(0,4,5)),0,0)
result = filter(lambda x: x[1]>2, lijst)
datadef = filter(lambda x: x[2]>2, result)
print len(lijst)
print len(datadef)
#Hier de lijst uit elkaar halen en ze middelen
R=6371000
lat1=[x[1] for x in datadef]
lon1=[x[2] for x in datadef]
tijd=[x[0] for x in datadef]
print np.mean(lat1)
print np.mean(lon1)
lat4=np.array([])
lon4=np.array([])
for i in range(len(lat1)):
    a=(lat1[i]*2*np.pi)/360
    b=(lon1[i]*2*np.pi)/360
    lat4=np.append(lat4,a)
    lon4=np.append(lon4,b)
lat=R*(lat4)
lon=R*(lon4)*np.cos(lat4)

# Hier maak ik de rijen even lang zodat ze gedeeld kunnen worden door de tijd, de tijd heeft 100 elementen minder, zie de loop

#lat
standd=np.std(lat)
print 'De standaarddeviatie van de lattitude is ' +  repr(standd)


#lon


standdlon=np.std(lon)
print 'De standaarddeviatie van de longitude is ' +  repr(standdlon)

