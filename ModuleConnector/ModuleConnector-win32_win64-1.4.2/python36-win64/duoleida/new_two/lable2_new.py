import matplotlib.pyplot as plt
import cmath
import numpy as np
import copy
from kalman_mul import *

area = np.pi * 3.8

data1 = []
data2 = []
data3 = []
file = open('C:/Users/yyb/Desktop/brss/p2_3.txt', 'r')
list_read = file.readlines()
for line in list_read:
    line = line.strip('\n')
    data3.append(line)
file.close()

file = open('C:/Users/yyb/Desktop/brss/p2_1.txt', 'r')
list_read = file.readlines()
for line in list_read:
    line = line.strip('\n')
    data1.append(line)
file.close()

file = open('C:/Users/yyb/Desktop/brss/p2_2.txt', 'r')
list_read = file.readlines()
for line in list_read:
    line = line.strip('\n')
    data2.append(line)
file.close()

banjing = 4
xl = np.arange(-2.4, 2.4, 0.2)
yl = np.arange(0, 4.0, 0.2)


def solv_13(r1, r3):
    yuan = ((r3 * r3 - r1 * r1 + 16) / 4)
    y1_1 = cmath.sqrt(3) / 4 * yuan + cmath.sqrt(
        (r3 * r3 - yuan * yuan) / 4 + (cmath.sqrt(3) / 4 * yuan) * (cmath.sqrt(3) / 4 * yuan))
    x1_t = cmath.sqrt(r3 * r3 - y1_1 * y1_1)
    if abs((x1_t - 2) * (x1_t - 2) + (y1_1 - 2 * cmath.sqrt(3).real) * (y1_1 - 2 * cmath.sqrt(3).real) - r1 * r1) < 0.5:
        x1_1 = x1_t
    else:
        x1_1 = -x1_t
    y2_1 = cmath.sqrt(3) / 4 * yuan - (r3 * r3 - yuan * yuan) / 4 + (cmath.sqrt(3) / 4 * yuan) * (
            cmath.sqrt(3) / 4 * yuan)
    x2_t = cmath.sqrt(r3 * r3 - y2_1 * y2_1)

    if abs((x2_t - 2) * (x2_t - 2) + (y1_1 - 2 * cmath.sqrt(3).real) * (y1_1 - 2 * cmath.sqrt(3).real) - r1 * r1) < 0.5:
        x2_1 = x2_t
    else:
        x2_1 = -x2_t
    xx1_1 = x1_1.imag
    xx2_1 = x2_1.imag

    x1_1 = x1_1.real

    x2_1 = x2_1.real
    y1_1 = y1_1.real
    y2_1 = y2_1.real

    return x1_1, x2_1, y1_1, y2_1, xx1_1, xx2_1


def solv_23(r2, r3):
    yuan = ((r2 * r2 - r3 * r3 - 16) / 4)
    y1_2 = -cmath.sqrt(3) / 4 * yuan + cmath.sqrt(
        (r3 * r3 - yuan * yuan) / 4 + (cmath.sqrt(3) / 4 * yuan) * (cmath.sqrt(3) / 4 * yuan))
    x1_t = cmath.sqrt(r3 * r3 - y1_2 * y1_2)
    if abs((x1_t + 2) * (x1_t + 2) + (y1_2 - 2 * cmath.sqrt(3).real) * (y1_2 - 2 * cmath.sqrt(3).real) - r2 * r2) < 0.5:
        x1_2 = x1_t
    else:
        x1_2 = -x1_t
    y2_2 = cmath.sqrt(3) / 4 * yuan - (r3 * r3 - yuan * yuan) / 4 + (cmath.sqrt(3) / 4 * yuan) * (
            cmath.sqrt(3) / 4 * yuan)
    x2_t = cmath.sqrt(r3 * r3 - y2_2 * y2_2)

    if abs((x2_t + 2) * (x2_t + 2) + (y1_2 - 2 * cmath.sqrt(3).real) * (y1_2 - 2 * cmath.sqrt(3).real) - r2 * r2) < 0.5:
        x2_2 = x2_t
    else:
        x2_2 = -x2_t
    xx1_2 = x1_2.imag
    xx2_2 = x2_2.imag

    x1_2 = x1_2.real

    x2_2 = x2_2.real
    y1_2 = y1_2.real
    y2_2 = y2_2.real

    return x1_2, x2_2, y1_2, y2_2, xx1_2, xx2_2


def solv_12(r1, r2):
    xx_3 = (r2 * r2 - r1 * r1) / 8
    y1_3 = 2 * cmath.sqrt(3) + cmath.sqrt(r2 * r2 - (xx_3 + 2) * (xx_3 + 2))
    y2_3 = 2 * cmath.sqrt(3) - cmath.sqrt(r2 * r2 - (xx_3 + 2) * (xx_3 + 2))
    yy1_3 = y1_3.imag
    yy2_3 = y2_3.imag
    y1_3 = y1_3.real
    y2_3 = y2_3.real

    return xx_3, y1_3, y2_3, yy1_3, yy2_3


h = 0


chushi_xa = -1.6
chushi_ya = 2.38
chushi_xb = 0.4
chushi_yb = 1.14
resultx=[]
resulty=[]
# chushi_xa=-1.05
# chushi_ya=1.87
# chushi_xb=0.74
# chushi_yb=2.0

kmxa = Kalman(chushi_xa, 0)
kmya = Kalman(chushi_ya, 0)
kmxb = Kalman(chushi_xb, 0)
kmyb = Kalman(chushi_yb, 0)
font = {
    'weight': 'normal',
    'size': 20

}

for i in range(110):
    ttmmppx = []
    ttmmppy = []
    ffllaa1=0
    ffllaa2=0
    re_la = []
    re_la_str = []
    chaa = []
    chab = []

    print "#########################################################################num" + "      " + str(i)
    a = str(data1[h + i])
    a = a[1:len(a) - 1]
    aa = a.split()
    b = str(data3[h + i])
    b = b[1:len(b) - 1]
    bb = b.split()
    c = str(data2[h + i])
    c = c[1:len(c) - 1]
    cc = c.split()

    for j1 in range(len(aa)):
        tmp1 = float(aa[j1])
        for j2 in range(len(bb)):
            tmp2 = float(bb[j2])
            for j3 in range(len(cc)):
                tmp3 = float(cc[j3])
                if tmp1 + tmp2 >= banjing:

                    x1, x2, y1, y2, xx1, xx2 = solv_13(tmp1, tmp2)

                    if x1 > -2 and x1 < 2 and y1 < 2 * cmath.sqrt(3).real and y1 > 0 and xx1 == 0:
                        # if y1 < 2 * cmath.sqrt(3).real and y1 > cmath.sqrt(3).real * x1 and y1 > -cmath.sqrt(3).real * x1 and xx1==0:
                        ttmmppx.append(x1)
                        ttmmppy.append(y1)

                        plt.scatter(x1, y1, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)
                        print "$$$$$$12" + str(h + i) + "  x1 " + str(x1)
                        print "$$$$$$12" + str(h + i) + "  y1 " + str(y1)
                        tmp_la = np.zeros((1, 2))
                        tmp_la[0, 0] = x1
                        tmp_la[0, 1] = y1
                        print tmp_la
                        print re_la
                        tmp_la_str = str(tmp_la)
                        if tmp_la_str not in re_la_str:
                            re_la_str.append(tmp_la_str)
                            re_la.append(tmp_la)

                            tmp_chaa = cmath.sqrt(
                                (x1 - chushi_xa) * (x1 - chushi_xa) + (y1 - chushi_ya) * (y1 - chushi_ya)).real
                            tmp_chab = cmath.sqrt(
                                (x1 - chushi_xb) * (x1 - chushi_xb) + (y1 - chushi_yb) * (y1 - chushi_yb)).real
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xa) + " " + str(chushi_ya) + "|" + str(
                                tmp_chab)
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xb) + " " + str(chushi_yb) + "|" + str(
                                tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)

                    print 2222
                    if x2 > -2 and x2 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and xx2 == 0:
                        # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x2 and y2 > -cmath.sqrt(3).real * x2 and xx2==0:
                        ttmmppx.append(x2)
                        ttmmppy.append(y2)

                        plt.scatter(x2, y2, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)

                        print "$$$$$$12" + str(h + i) + "  x2 " + str(x2)
                        print "$$$$$$12" + str(h + i) + "  y2 " + str(y2)
                        tmp_la = np.zeros((1, 2))
                        tmp_la[0, 0] = x2
                        tmp_la[0, 1] = y2
                        tmp_la_str = str(tmp_la)
                        if tmp_la_str not in re_la_str:
                            re_la_str.append(tmp_la_str)
                            re_la.append(tmp_la)
                            tmp_chaa = cmath.sqrt(
                                (x2 - chushi_xa) * (x2 - chushi_xa) + (y2 - chushi_ya) * (y2 - chushi_ya)).real
                            tmp_chab = cmath.sqrt(
                                (x2 - chushi_xb) * (x2 - chushi_xb) + (y2 - chushi_yb) * (y2 - chushi_yb)).real
                            print str(x2) + " " + str(y2) + " |" + str(chushi_xa) + " " + str(chushi_ya) + "|" + str(
                                tmp_chaa)
                            print str(x2) + " " + str(y2) + " |" + str(chushi_xb) + " " + str(chushi_yb) + "|" + str(
                                tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)

                if tmp3 + tmp2 >= banjing:

                    x1, x2, y1, y2, xx11, xx22 = solv_23(tmp3, tmp2)
                    if x1 > -2 and x1 < 2 and y1 < 2 * cmath.sqrt(3).real and y1 > 0 and xx11 == 0:
                        # if y1 < 2 * cmath.sqrt(3).real and y1 > cmath.sqrt(3).real * x1 and y1 > -cmath.sqrt(
                        #         3).real * x1 and xx1 == 0:
                        ttmmppx.append(x1)
                        ttmmppy.append(y1)
                        plt.scatter(x1, y1, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)
                        print "$$$$$$23" + str(h + i) + "  x1 " + str(x1)
                        print "$$$$$$23" + str(h + i) + "  y1 " + str(y1)
                        tmp_la = np.zeros((1, 2))
                        tmp_la[0, 0] = x1
                        tmp_la[0, 1] = y1
                        tmp_la_str = str(tmp_la)
                        if tmp_la_str not in re_la_str:
                            re_la_str.append(tmp_la_str)
                            re_la.append(tmp_la)
                            tmp_chaa = cmath.sqrt(
                                (x1 - chushi_xa) * (x1 - chushi_xa) + (y1 - chushi_ya) * (y1 - chushi_ya)).real
                            tmp_chab = cmath.sqrt(
                                (x1 - chushi_xb) * (x1 - chushi_xb) + (y1 - chushi_yb) * (y1 - chushi_yb)).real
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xa) + " " + str(chushi_ya) + "|" + str(
                                tmp_chaa)
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xb) + " " + str(chushi_yb) + "|" + str(
                                tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)

                    if x2 > -2 and x2 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and xx22 == 0:
                        # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x2 and y2 > -cmath.sqrt(
                        #         3).real * x2 and xx2 == 0:
                        ttmmppx.append(x2)
                        ttmmppy.append(y2)
                        plt.scatter(x2, y2, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)

                        print "$$$$$$23" + str(h + i) + "  x2 " + str(x2)
                        print "$$$$$$23" + str(h + i) + "  y2 " + str(y2)
                        tmp_la = np.zeros((1, 2))
                        tmp_la[0, 0] = x2
                        tmp_la[0, 1] = y2
                        tmp_la_str = str(tmp_la)
                        if tmp_la_str not in re_la_str:
                            re_la_str.append(tmp_la_str)
                            re_la.append(tmp_la)
                            tmp_chaa = cmath.sqrt(
                                (x2 - chushi_xa) * (x2 - chushi_xa) + (y2 - chushi_ya) * (y2 - chushi_ya)).real
                            tmp_chab = cmath.sqrt(
                                (x2 - chushi_xb) * (x2 - chushi_xb) + (y2 - chushi_yb) * (y2 - chushi_yb)).real
                            print str(x2) + " " + str(y2) + " |" + str(chushi_xa) + " " + str(chushi_ya) + "|" + str(
                                tmp_chaa)
                            print str(x2) + " " + str(y2) + " |" + str(chushi_xb) + " " + str(chushi_yb) + "|" + str(
                                tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)

                if tmp1 + tmp3 >= banjing:

                    x1, y1, y2, yy11, yy22 = solv_12(tmp3, tmp1)

                    if x1 > -2 and x1 < 2 and y1 < 2 * cmath.sqrt(3).real and y1 > 0 and yy11 == 0:
                        # if y1 < 2 * cmath.sqrt(3).real and y1 > cmath.sqrt(3).real * x1 and y1 > -cmath.sqrt(
                        #         3).real * x1 and yy1 == 0:
                        ttmmppx.append(x1)
                        ttmmppy.append(y1)
                        plt.scatter(x1, y1, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)
                        print "$$$$$$13" + str(h + i) + "  x1 " + str(x1)
                        print "$$$$$$13" + str(h + i) + "  y1 " + str(y1)
                        tmp_la = np.zeros((1, 2))
                        tmp_la[0, 0] = x1
                        tmp_la[0, 1] = y1
                        tmp_la_str = str(tmp_la)
                        if tmp_la_str not in re_la_str:
                            re_la_str.append(tmp_la_str)
                            re_la.append(tmp_la)
                            tmp_chaa = cmath.sqrt(
                                (x1 - chushi_xa) * (x1 - chushi_xa) + (y1 - chushi_ya) * (y1 - chushi_ya)).real
                            tmp_chab = cmath.sqrt(
                                (x1 - chushi_xb) * (x1 - chushi_xb) + (y1 - chushi_yb) * (y1 - chushi_yb)).real
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xa) + " " + str(chushi_ya) + "|" + str(
                                tmp_chaa)
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xb) + " " + str(chushi_yb) + "|" + str(
                                tmp_chab)

                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)

                    if x1 > -2 and x1 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and yy22 == 0:
                        # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x1 and y2 > -cmath.sqrt(
                        #         3).real * x1 and yy2 == 0:
                        ttmmppx.append(x1)
                        ttmmppy.append(y2)
                        plt.scatter(x1, y2, color='r', s=area)
                        plt.xticks(xl)
                        plt.yticks(yl)
                        plt.grid(True)

                        print "$$$$$$13" + str(h + i) + "  x2 " + str(x1)
                        print "$$$$$$13" + str(h + i) + "  y2 " + str(y2)
                        tmp_la = np.zeros((1, 2))
                        tmp_la[0, 0] = x1
                        tmp_la[0, 1] = y2
                        tmp_la_str = str(tmp_la)
                        if tmp_la_str not in re_la_str:
                            re_la_str.append(tmp_la_str)
                            re_la.append(tmp_la)
                            tmp_chaa = cmath.sqrt(
                                (x1 - chushi_xa) * (x1 - chushi_xa) + (y2 - chushi_ya) * (y2 - chushi_ya)).real
                            tmp_chab = cmath.sqrt(
                                (x1 - chushi_xb) * (x1 - chushi_xb) + (y2 - chushi_yb) * (y2 - chushi_yb)).real
                            print str(x1) + " " + str(y2) + " |" + str(chushi_xa) + " " + str(chushi_ya) + "|" + str(
                                tmp_chaa)
                            print str(x1) + " " + str(y2) + " |" + str(chushi_xb) + " " + str(chushi_yb) + "|" + str(
                                tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print re_la
    print chaa
    print chab
    print len(re_la)
    print len(chaa)
    print len(chab)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    all_xa = 0
    all_ya = 0
    all_xb = 0
    all_yb = 0
    flaga = 0
    flagb = 0
    gea = 0
    geb = 0
    print"^^^^^^^^^^^^^^"
    print chushi_xa
    print chushi_ya
    print chushi_xb
    print chushi_yb
    print re_la

    copy_chaa = copy.deepcopy(chaa)
    while flaga < 0.4:
        if len(copy_chaa)==0:
            ffllaa1=1
            break
        min_chaa = chaa.index(min(copy_chaa))
        min_num = copy_chaa.index(min(copy_chaa))

        end_xa = re_la[min_chaa][0, 0]
        end_ya = re_la[min_chaa][0, 1]
        all_xa = end_xa + all_xa
        all_ya = end_ya + all_ya
        gea = gea + 1
        print copy_chaa
        copy_chaa.pop(min_num)
        print copy_chaa
        if len(copy_chaa)==0:
            ffllaa1 = 1
            break
        flaga = min(copy_chaa)
        print "AAAAAAAAAAAAAAAAAAAAAAA"
        print end_xa
        print end_ya
    if ffllaa1==1:
        end_xaa=chushi_xa
        end_yaa=chushi_ya
    else:
        print "gea" + "    " + str(gea)
        print all_xa
        print all_ya
        end_xaa = all_xa / gea
        end_yaa = all_ya / gea
    print end_xaa
    print end_yaa

    copy_chab = copy.deepcopy(chab)
    while flagb < 0.4:
        if len(copy_chab)==0:
            ffllaa2 = 1
            break
        min_chab = chab.index(min(copy_chab))
        min_num = copy_chab.index(min(copy_chab))

        end_xb = re_la[min_chab][0, 0]
        end_yb = re_la[min_chab][0, 1]
        all_xb = end_xb + all_xb
        all_yb = end_yb + all_yb
        geb = geb + 1
        print copy_chab
        copy_chab.pop(min_num)
        print copy_chab
        if len(copy_chab)==0:
            ffllaa2 = 1
            break
        flagb = min(copy_chab)
        print "BBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        print end_xb
        print end_yb
    if ffllaa2 == 1:
        end_xbb = chushi_xb
        end_ybb = chushi_yb
    else:
        print "geb" + "    " + str(geb)
        print all_xb
        print all_yb
        end_xbb = all_xb / geb
        end_ybb = all_yb / geb
    print end_xbb
    print end_ybb
    resultx.append(ttmmppx)
    resulty.append(ttmmppy)

    kmxa.z = np.array([end_xaa])
    kmxa.kf_update()
    kmya.z = np.array([end_yaa])
    kmya.kf_update()
    kmxb.z = np.array([end_xbb])
    kmxb.kf_update()
    kmyb.z = np.array([end_ybb])
    kmyb.kf_update()
    end_xaa = kmxa.x[0, 0]
    end_yaa = kmya.x[0, 0]
    end_xbb = kmxb.x[0, 0]
    end_ybb = kmyb.x[0, 0]

    print"***************************************"
    print end_xaa
    print end_yaa
    print end_xbb
    print end_ybb
    # plt.scatter(end_xaa, end_yaa, color='b', s=area)
    # plt.xticks(xl)
    # plt.yticks(yl)
    # plt.scatter(end_xbb, end_ybb, color='b', s=area)
    # plt.xticks(xl)
    # plt.yticks(yl)
    chushi_xa = end_xaa
    chushi_ya = end_yaa
    chushi_xb = end_xbb
    chushi_yb = end_ybb
# file=open('C:/Users/yyb/Desktop/brss/x_11.txt','w')
# for fp in resultx:
# 	file.write(str(fp))
# 	file.write('\n')
# file.close()
#
# file=open('C:/Users/yyb/Desktop/brss/y_11.txt','w')
# for fp in resulty:
# 	file.write(str(fp))
# 	file.write('\n')
plt.xticks(xl)
plt.yticks(yl)
plt.show()



