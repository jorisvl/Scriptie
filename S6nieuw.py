import numpy as np
import math
import matplotlib.pylab as plt



#Hier wordt de data ingeladen en worden S6 en BS op dezelfde startdatum gezet.
lijst=np.delete(np.genfromtxt('/Users/jorisvanlammeren/Documents/Studie/Scriptie/JorisVLammeren/Data/Svalbard_BS_input.txt',usecols=(0,4,5)),0,0)
result = filter(lambda x: x[1]>2, lijst)
datadef = filter(lambda x: x[2]>2, result)
lat1=[x[1] for x in datadef]
lon1=[x[2] for x in datadef]
tijd=[x[0] for x in datadef]
BSgemlat=np.mean(lat1)
BSgemlon=np.mean(lon1)

data=np.delete(np.genfromtxt('/Users/jorisvanlammeren/Documents/Studie/Scriptie/JorisVLammeren/Data/Svalbard_S6_input.txt',usecols=(0,4,5)),0,0)
dataBS=np.delete(np.genfromtxt('/Users/jorisvanlammeren/Documents/Studie/Scriptie/JorisVLammeren/Data/Svalbard_BS_input.txt',usecols=(0,4,5)),0,0)
data=np.delete(data,[range(69)],0)
dataBS=np.delete(dataBS,range(79132,79226),0)


#Hier haal ik de lat en lon uit de data en uit BS
lat=[x[1] for x in data]
lon=[x[2] for x in data]
tijd=[x[0] for x in data]
latBS=[x[1] for x in dataBS]
lonBS=[x[2] for x in dataBS]
tijdBS=[x[0] for x in dataBS]
latbss=latBS-BSgemlat
lonbss=lonBS-BSgemlon
lat5=np.array([])
lon5=np.array([])
for i in range(len(lat)):
    ab=lat[i]-latbss[i]
    cd=lon[i]-lonbss[i]
    lat5=np.append(lat5, ab)
    lon5=np.append(lon5, cd)
    
print lat5[0:10]
print len(lat5)
print len(lon5)
print len(tijd)
lat6=np.array([])
lon6=np.array([])
tijd1=np.array([])
for i in range(len(lat5)):
    if lat5[i]>2 and lon5[i]>2 and lat5[i]<100 and lon5[i]<100:
        lat6=np.append(lat6,lat5[i])
        lon6=np.append(lon6,lon5[i])
        tijd1=np.append(tijd1,tijd[i])
#result = filter(lambda x: x>2, lat5)
#datadef = filter(lambda x: x>2, lon5)
#lat = filter(lambda x: x<100, result)
#lon = filter(lambda x: x<100, datadef)
print len(lat6)
print len(lon6)
print len(tijd1)
R=6371000
#print lat[0]
#print len(lat)
#print lon[0]
#print len(lon)

#Hier schaal ik de lattitude en de longitude ten opzichte van hun vorige punt
lat4=np.array([])
lon4=np.array([])
for i in range(len(lat6)):
    a=(lat6[i]*2*np.pi)/360
    b=(lon6[i]*2*np.pi)/360
    lat4=np.append(lat4,a)
    lon4=np.append(lon4,b)
print lat4[0:5]
lat2=np.delete(np.insert(lat4,0,lat4[0]),-1)
print lat2
lon2=np.delete(np.insert(lon4,0,lon4[0]),-1)
latcor=R*(lat4-lat2)
loncor=R*(lon4-lon2)*np.cos(lat4)
latcor2=latcor**2
loncor2=loncor**2
tijdsverschil=np.delete(np.insert(tijd1,0,tijd1[0]),-1)
print latcor[0:9]
#Hier bereken ik het lopende gemiddelde eb filter ik de date ten opzichte van de standaarddeviatie van BS
n=100
stdbslat=3.5160
stdbslon=2.2207
print len(latcor)
print len(tijd1)
for i in range(len(latcor)):
    if np.std(latcor[i:i+n]) >3*stdbslat and i+n-1<len(latcor):
        latcor=np.delete(latcor,i+n-1)
        loncor=np.delete(loncor,i+n-1)
        tijd1=np.delete(tijd1,i+n-1)

print len(latcor)

for i in range(len(loncor)):
    if np.std(loncor[i:i+n]) >3*stdbslon and i+n-1<len(latcor):
        latcor=np.delete(latcor,i+n-1)
        loncor=np.delete(loncor,i+n-1)
        tijd1=np.delete(tijd1,i+n-1)

print len(latcor)

for i in range(len(latcor)):
    if np.std(latcor[-i-n:-i]) >3*stdbslat:
        latcor=np.delete(latcor,-i-n)
        loncor=np.delete(loncor,-i-n)
        tijd1=np.delete(tijd1,-i-n)
        

print len(latcor)

for i in range(len(loncor)):
    if np.std(latcor[-i-n:-i]) >3*stdbslon:
        latcor=np.delete(latcor,-i-n+1)
        loncor=np.delete(loncor,-i-n+1)
        tijd1=np.delete(tijd1,-i-n+1)
# Hier reken ik de snelheid uit
print len(latcor)
print len(tijd1)
tijdsverschil=tijd1-np.delete(np.insert(tijd1,0,0),-1)
u=(latcor/tijdsverschil)
v=(loncor/tijdsverschil)
d=2*R*np.arcsin(np.sqrt(np.power(np.sin(lat4-lat2/2),2)+np.cos(lat2)*np.cos(lat4)*np.power(np.sin(lon4-lon2/2),2)))
snelheid=np.power((np.power(u,2)+np.power(v,2)),0.5)*24*365
print d[0:9]
print snelheid[0:9]
#Hier vind ik de tijdwaardes zonder snelheid
tijdnul=np.array([])
for element in range(79201):
    if element not in tijd1:
        tijdnul=np.append(tijdnul,element)
tijdnul=np.delete(tijdnul,0)


#Hier koppel ik de tijdstippen aan een snelheid en koppel ik de tijdstippen zonder snelheid aan 0
c=np.array([])
for i in range(len(snelheid)):
    d=[tijd1[i],snelheid[i]]
    c=np.append(c,d)
lijst=np.split(c,len(c)/2)

p=np.array([])
for i in range(len(tijdnul)):
    l=[tijdnul[i],0]
    p=np.append(p,l)
lijst2=np.split(p,len(p)/2)

m=lijst+lijst2
def getKey(item):
    return item[0]
lijstdef=sorted(m, key=getKey)
snel=[x[1] for x in lijstdef]
tijd=[x[0] for x in lijstdef]
snelheidgemweek=np.array_split(snel,108)
result=np.array([])
for i in range(len(snelheidgemweek)):
    a=snelheidgemweek[i].tolist()
    a = [x for x in a if x != 0]
    if len(a)>0:
        pp=sum(a)/len(a)
    else:
        pp=0
    result=np.append(result,pp)
plaatje=plt.plot(result)
#plt.axis([5*12, 6*12, 0, 0.0005])
plt.show()
#result=np.array([])
#for i in range(len(lat)):
#    b=sum(latcor[i:i+n])
#    result=np.append(result, b)
#result2=np.array([])
#for i in range(len(lat2)):
#    d=sum(latcor2[i:i+n])
#    result2=np.append(result2, d)
#result3=np.array([])
#for i in range(len(lon)):
#    e=sum(loncor[i:i+n])
#    result3=np.append(result3, e)
#result4=np.array([])
#for i in range(len(lon2)):
#    f=sum(loncor2[i:i+n])
#    result4=np.append(result4, f)
#resultt=np.array([])
#for i in range(len(tijd)-n):
#    c=tijd[i+n]-tijd[i]
#    resultt=np.append(resultt, c)
#n is the window size

# Hier maak ik de rijen even lang zodat ze gedeeld kunnen worden door de tijd, de tijd heeft 100 elementen minder, zie de loop
#Hier bepaal ik de standaarddeviatie
#lat
#snel=(result/n)/tijdsverschil
#snel2=(result2/n)/tijdsverschil
#standd=(snel2-np.power(snel,2))**0.5
#gemstandlat=sum(standd)/len(standd)
#print 'De gemiddelde standaarddeviatie van de lattitude is ' +  repr(gemstandlat)


#lon

#snel3=(result3/n)/tijdsverschil
#snel4=(result4/n)/tijdsverschil
#standdlon=(snel4-np.power(snel3,2))**0.5
#gemstandlon=sum(standdlon)/len(standdlon)
#print 'De gemiddelde standaarddeviatie van de longitude is ' +  repr(gemstandlon)

#resultv=np.array([])
#for i in range(abs(len(snel3)/720)):
#    g=sum(snel3[720*i:720*(i+1)])
#    resultv=np.append(resultv, g)
#print len(resultv)

#plotjes van de data

#pla=plt.plot(latcor,'r')
#pla2=plt.plot(tijd,devlon)
#pla3=plt.plot(tijd, snel3)
#plt.show(pla)
#plt.show(pla)
