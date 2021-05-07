import matplotlib.pyplot as plt
import cmath
import numpy as np

area = np.pi * 3.8

data3=[]
file=open('C:/Users/yyb/Desktop/brs/radar_3.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data3.append(line)
file.close()






banjing=4
xl = np.arange(-2.4, 2.4, 0.2)
yl = np.arange(0, 4.8, 0.2)



h=0
ttmmppx=[]
ttmmppy=[]
for i in range(250):

    b = str(data3[h+i])
    b = b[1:len(b) - 1]
    bb = b.split()


    plt.scatter(i,float(bb[0]))
    plt.scatter(i, float(bb[1]))




plt.show()



