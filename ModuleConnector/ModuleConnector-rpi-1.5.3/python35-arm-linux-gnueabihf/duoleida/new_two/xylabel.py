import matplotlib.pyplot as plt
import cmath
import numpy as np

area = np.pi * 3.8

data1=[]
data2=[]
data3=[]
file=open('C:/Users/yyb/Desktop/brs/radar_3.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data3.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brs/radar_1.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data1.append(line)
file.close()

file=open('C:/Users/yyb/Desktop/brs/radar_2.txt','r')
list_read=file.readlines()
for line in list_read:
    line=line.strip('\n')
    data2.append(line)
file.close()


banjing=4
xl = np.arange(-2.4, 2.4, 0.2)
yl = np.arange(0, 4.8, 0.2)
def solv_13(r1,r3):
    yuan=((r3*r3-r1*r1+16)/4)
    y1=cmath.sqrt(3)/4*yuan+cmath.sqrt((r3*r3-yuan*yuan)/4+(cmath.sqrt(3)/4*yuan)*(cmath.sqrt(3)/4*yuan))
    x1_t=cmath.sqrt(r3*r3-y1*y1)
    if abs((x1_t-2)*(x1_t-2)+(y1-2*cmath.sqrt(3).real)*(y1-2*cmath.sqrt(3).real)-r1*r1)<0.3:
        x1=x1_t
    else:
        x1=-x1_t
    y2 = cmath.sqrt(3) / 4 * yuan - (r3 * r3 - yuan * yuan) / 4 + (cmath.sqrt(3) / 4 * yuan) * (
            cmath.sqrt(3) / 4 * yuan)
    x2_t = cmath.sqrt(r3 * r3 - y2 * y2)

    if abs((x2_t-2)*(x2_t-2)+(y1-2*cmath.sqrt(3).real)*(y1-2*cmath.sqrt(3).real)-r1*r1)<0.3:
        x2=x2_t
    else:
        x2=-x2_t
    xx1=x1.imag
    xx2=x2.imag

    x1 = x1.real

    x2 = x2.real
    y1 = y1.real
    y2 = y2.real

    return x1,x2 ,y1,y2,xx1,xx2


def solv_23(r2,r3):
    yuan=((r2*r2-r3*r3-16)/4)
    y1 = -cmath.sqrt(3) / 4 * yuan + cmath.sqrt((r3 * r3 - yuan * yuan) / 4 + (cmath.sqrt(3) / 4 * yuan) * (cmath.sqrt(3) / 4 * yuan))
    x1_t=cmath.sqrt(r3*r3-y1*y1)
    if abs((x1_t+2)*(x1_t+2)+(y1-2*cmath.sqrt(3).real)*(y1-2*cmath.sqrt(3).real)-r2*r2)<0.3:
        x1=x1_t
    else:
        x1=-x1_t
    y2 = cmath.sqrt(3) / 4 * yuan - (r3 * r3 - yuan * yuan) / 4 + (cmath.sqrt(3) / 4 * yuan) * (
            cmath.sqrt(3) / 4 * yuan)
    x2_t = cmath.sqrt(r3 * r3 - y2 * y2)

    if abs((x2_t+2)*(x2_t+2)+(y1-2*cmath.sqrt(3).real)*(y1-2*cmath.sqrt(3).real)-r2*r2)<0.3:
        x2=x2_t
    else:
        x2=-x2_t
    xx1=x1.imag
    xx2=x2.imag

    x1 = x1.real

    x2 = x2.real
    y1 = y1.real
    y2 = y2.real

    return x1,x2 ,y1,y2,xx1,xx2


def solv_12(r1,r2):
    x=(r2*r2-r1*r1)/8
    y1=2*cmath.sqrt(3)+cmath.sqrt(r2*r2-(x+2)*(x+2))
    y2 = 2 * cmath.sqrt(3) - cmath.sqrt(r2 * r2 - (x + 2) * (x + 2))
    yy1 = y1.imag
    yy2 = y2.imag
    y1=y1.real
    y2=y2.real


    return x1,y1,y2,yy1,yy2



h=0
ttmmppx=[]
ttmmppy=[]
for i in range(150):
    a = str(data1[h+i])
    a = a[1:len(a) - 1]
    aa = a.split()
    b = str(data3[h+i])
    b = b[1:len(b) - 1]
    bb = b.split()
    c = str(data2[h + i])
    c = c[1:len(c) - 1]
    cc = c.split()

    for j1 in range(len(aa)):
        tmp1=float(aa[j1])
        for j2 in range(len(bb)):
            tmp2=float(bb[j2])
            for j3 in range(len(cc)):
                tmp3 = float(cc[j2])
                if tmp1+tmp2>=banjing:

                    x1, x2, y1, y2,xx1,xx2 =solv_13(tmp1, tmp2)


                    if x1>-2 and x1<2 and y1<2 * cmath.sqrt(3).real and y1>0 and xx1==0:
                    # if y1 < 2 * cmath.sqrt(3).real and y1 > cmath.sqrt(3).real * x1 and y1 > -cmath.sqrt(3).real * x1 and xx1==0:
                        ttmmppx.append(x1)
                        ttmmppy.append(y1)

                        plt.scatter(x1, y1, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)
                        print "$$$$$$"+str(h+i)+"  x1 "+str(x1)
                        print "$$$$$$" + str(h + i) + "  y1 " + str(y1)
                    if x2 > -2 and x2 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and xx2==0:
                    # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x2 and y2 > -cmath.sqrt(3).real * x2 and xx2==0:
                        ttmmppx.append(x2)
                        ttmmppy.append(y2)

                        plt.scatter(x2, y2, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)

                        print "$$$$$$" + str(h + i) + "  x2 " + str(x2)
                        print "$$$$$$" + str(h + i) + "  y2 " + str(y2)

                if tmp3 + tmp2 >= banjing:

                    x1, x2, y1, y2, xx1, xx2 = solv_23(tmp3, tmp2)
                    if x1 > -2 and x1 < 2 and y1 < 2 * cmath.sqrt(3).real and y1 > 0  and xx1 == 0:
                    # if y1 < 2 * cmath.sqrt(3).real and y1 > cmath.sqrt(3).real * x1 and y1 > -cmath.sqrt(
                    #         3).real * x1 and xx1 == 0:
                        ttmmppx.append(x1)
                        ttmmppy.append(y1)
                        plt.scatter(x1, y1, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)
                        print "$$$$$$" + str(h + i) + "  x1 " + str(x1)
                        print "$$$$$$" + str(h + i) + "  y1 " + str(y1)
                    if x2 > -2 and x2 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and xx2==0:
                    # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x2 and y2 > -cmath.sqrt(
                    #         3).real * x2 and xx2 == 0:
                        ttmmppx.append(x2)
                        ttmmppy.append(y2)
                        plt.scatter(x2, y2, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)

                        print "$$$$$$" + str(h + i) + "  x2 " + str(x2)
                        print "$$$$$$" + str(h + i) + "  y2 " + str(y2)

                if tmp1 + tmp3 >= banjing:

                    x1,y1, y2,yy1,yy2 = solv_12(tmp3, tmp1)


                    if x1 > -2 and x1 < 2 and y1 < 2 * cmath.sqrt(3).real and y1 > 0 and yy1 == 0:
                    # if y1 < 2 * cmath.sqrt(3).real and y1 > cmath.sqrt(3).real * x1 and y1 > -cmath.sqrt(
                    #         3).real * x1 and yy1 == 0:
                        ttmmppx.append(x1)
                        ttmmppy.append(y1)
                        plt.scatter(x1, y1, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)
                        print "$$$$$$" + str(h + i) + "  x1 " + str(x1)
                        print "$$$$$$" + str(h + i) + "  y1 " + str(y1)
                    if x1 > -2 and x1 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and yy2 == 0:
                    # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x1 and y2 > -cmath.sqrt(
                    #         3).real * x1 and yy2 == 0:
                        ttmmppx.append(x1)
                        ttmmppy.append(y2)
                        plt.scatter(x1, y2, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)

                        print "$$$$$$" + str(h + i) + "  x2 " + str(x1)
                        print "$$$$$$" + str(h + i) + "  y2 " + str(y2)





plt.xticks(xl)
plt.yticks(yl)
plt.show()



