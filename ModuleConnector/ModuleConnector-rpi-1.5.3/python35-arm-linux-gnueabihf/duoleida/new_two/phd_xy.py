import matplotlib.pyplot as plt
import cmath
import numpy as np
import copy
from kalman_mul import *
area = np.pi * 3.8

data1=[]
data2=[]
data3=[]
data4=[]
data5=[]
data6=[]
data7=[]
data8=[]

file=open('C:/Users/yyb/Desktop/brre/phd1_xr.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data1.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brre/phd1_yr.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data2.append(line)
file.close()
file=open('C:/Users/yyb/Desktop/brre/phd1_xl.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data3.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brre/phd1_yl.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data4.append(line)
file.close()
file=open('C:/Users/yyb/Desktop/brre/knn1_xr.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data5.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brre/knn1_yr.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data6.append(line)
file.close()
file=open('C:/Users/yyb/Desktop/brre/knn1_xl.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data7.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brre/knn1_yl.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data8.append(line)
file.close()

xl = np.arange(-2.4, 2.4, 0.2)
yl = np.arange(0, 4.0, 0.2)
area = np.pi * 3.8

chushi_xa=-0.8
chushi_ya=0.8
chushi_xb=0.7
chushi_yb=2.9



kmxa = Kalman(chushi_xb, 0)
kmya = Kalman(chushi_yb, 0)
kmxaa = Kalman(chushi_xa, 0)
kmyaa = Kalman(chushi_ya, 0)

kmxb = Kalman(chushi_xb, 0)
kmyb = Kalman(chushi_yb, 0)
kmxbb = Kalman(chushi_xa, 0)
kmybb = Kalman(chushi_ya, 0)

for i in range(90):
    h=0
    tmpx=[]
    tmpy=[]
    tmpx2 = []
    tmpy2 = []

    a = str(data1[i])
    a = a[1:len(a) - 1]
    aa = a.split()
    b = str(data2[h + i])
    b = b[1:len(b) - 1]
    bb = b.split()

    c = str(data3[h + i])
    c = c[1:len(c) - 1]
    cc = c.split()
    d = str(data4[h + i])
    d = d[1:len(d) - 1]
    dd = d.split()



    kmxa.z = np.array([float(aa[0])])
    kmxa.kf_update()
    kmya.z = np.array([float(bb[0])])
    kmya.kf_update()

    kmxaa.z = np.array([float(cc[0])])
    kmxaa.kf_update()
    kmyaa.z = np.array([float(dd[0])])
    kmyaa.kf_update()



    end_xaa = kmxa.x[0, 0]
    end_yaa = kmya.x[0, 0]

    end_xaaa = kmxaa.x[0, 0]
    end_yaaa = kmyaa.x[0, 0]




    tmpx.append(end_xaa)
    tmpy.append(end_yaa)

    tmpx2.append(end_xaaa)
    tmpy2.append(end_yaaa)

    plt.scatter(end_xaa,end_yaa,color='g',s=area)
    plt.xticks(xl)
    plt.yticks(yl)
    plt.grid(True)
    plt.scatter(end_xaaa, end_yaaa, color='g', s=area)
    plt.xticks(xl)
    plt.yticks(yl)
    plt.grid(True)



for i in range(80):
    h=0
    tmpx=[]
    tmpy=[]
    tmpx2 = []
    tmpy2 = []




    e = str(data5[h + i])
    e = e[1:len(e) - 1]
    ee = e.split()
    f = str(data6[h + i])
    f = f[1:len(f) - 1]
    ff = f.split()

    g = str(data7[h + i])
    g = g[1:len(g) - 1]
    gg = g.split()
    h = str(data8[h + i])
    h = h[1:len(h) - 1]
    hh = h.split()



    kmxb.z = np.array([float(ee[0])])
    kmxb.kf_update()
    kmyb.z = np.array([float(ff[0])])
    kmyb.kf_update()

    kmxbb.z = np.array([float(gg[0])])
    kmxbb.kf_update()
    kmybb.z = np.array([float(hh[0])])
    kmybb.kf_update()

    end_xbb = kmxb.x[0, 0]
    end_ybb = kmyb.x[0, 0]

    end_xbbb = kmxbb.x[0, 0]
    end_ybbb = kmybb.x[0, 0]







    plt.scatter(end_xbb, end_ybb, color='b', s=area)
    plt.xticks(xl)
    plt.yticks(yl)
    plt.grid(True)
    plt.scatter(end_xbbb, end_ybbb, color='b', s=area)
    plt.xticks(xl)
    plt.yticks(yl)
    plt.grid(True)
# file=open('C:/Users/yyb/Desktop/brre/phd2_xshu.txt','w')
# for fp in resultx:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()
#
# file=open('C:/Users/yyb/Desktop/brre/phd2_yshu.txt','w')
# for fp in resulty:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()

plt.show()

