import matplotlib.pyplot as plt
import random 
def henon(a,b,n):
    x=[]
    y=[]
    x.append(0)
    y.append(0)
    for i in range(0,n):
        newX= 1+ y[i]-a*x[i]*x[i]+ (random.randrange(-1,1)/200.0)
        newY= b*x[i]
        x.append(newX)
        y.append(newY)
    return x,y  

x,y = henon(1.4,0.3,100000)

plt.scatter(x,y)
#plt.xlim(-2,2)
#plt.ylim(-2,2)
plt.show()

