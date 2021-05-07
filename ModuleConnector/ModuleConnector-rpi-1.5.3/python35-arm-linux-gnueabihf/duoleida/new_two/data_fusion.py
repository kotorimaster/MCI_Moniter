import matplotlib.pyplot as plt
import cmath
import numpy as np
import copy
from kalman_mul import *



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
    xx=(r2*r2-r1*r1)/8
    y1=2*cmath.sqrt(3)+cmath.sqrt(r2*r2-(xx+2)*(xx+2))
    y2 = 2 * cmath.sqrt(3) - cmath.sqrt(r2 * r2 - (xx + 2) * (xx + 2))
    yy1 = y1.imag
    yy2 = y2.imag
    y1=y1.real
    y2=y2.real


    return xx,y1,y2,yy1,yy2







def fu(aa,bb,cc,chushi_xa,chushi_ya,chushi_xb,chushi_yb,re_la,re_la_str,chaa,chab,banjing):
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

                        tmp_la=np.zeros((1,2))
                        tmp_la[0,0]=x1
                        tmp_la[0, 1] = y1
                        print tmp_la
                        print re_la
                        tmp_la_str=str(tmp_la)
                        if tmp_la_str not in re_la_str:
                            re_la_str.append(tmp_la_str)
                            re_la.append(tmp_la)

                            tmp_chaa=cmath.sqrt((x1-chushi_xa)*(x1-chushi_xa)+(y1-chushi_ya)*(y1-chushi_ya)).real
                            tmp_chab=cmath.sqrt((x1-chushi_xb)*(x1-chushi_xb)+(y1-chushi_yb)*(y1-chushi_yb)).real
                            print str(x1)+" "+str(y1)+" |"+str(chushi_xa)+" "+str(chushi_ya)+"|"+str(tmp_chab)
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xb) + " " + str(chushi_yb)+"|"+str(tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)



                    print 2222
                    if x2 > -2 and x2 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and xx2==0:
                    # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x2 and y2 > -cmath.sqrt(3).real * x2 and xx2==0:

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
                                (x2 - chushi_xb) * (x2 - chushi_xb) + (y2- chushi_yb) * (y2 - chushi_yb)).real
                            print str(x2) + " " + str(y2) + " |" + str(chushi_xa) + " " + str(chushi_ya)+"|"+str(tmp_chaa)
                            print str(x2) + " " + str(y2) + " |" + str(chushi_xb) + " " + str(chushi_yb)+"|"+str(tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)


                if tmp3 + tmp2 >= banjing:

                    x1, x2, y1, y2, xx1, xx2 = solv_23(tmp3, tmp2)
                    if x1 > -2 and x1 < 2 and y1 < 2 * cmath.sqrt(3).real and y1 > 0  and xx1 == 0:
                    # if y1 < 2 * cmath.sqrt(3).real and y1 > cmath.sqrt(3).real * x1 and y1 > -cmath.sqrt(
                    #         3).real * x1 and xx1 == 0:

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
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xa) + " " + str(chushi_ya)+"|"+str(tmp_chaa)
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xb) + " " + str(chushi_yb)+"|"+str(tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)

                    if x2 > -2 and x2 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and xx2==0:
                    # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x2 and y2 > -cmath.sqrt(
                    #         3).real * x2 and xx2 == 0:

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
                            print str(x2) + " " + str(y2) + " |" + str(chushi_xa) + " " + str(chushi_ya)+"|"+str(tmp_chaa)
                            print str(x2) + " " + str(y2) + " |" + str(chushi_xb) + " " + str(chushi_yb)+"|"+str(tmp_chab)
                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)


                if tmp1 + tmp3 >= banjing:

                    x1,y1, y2,yy1,yy2 = solv_12(tmp3, tmp1)


                    if x1 > -2 and x1 < 2 and y1 < 2 * cmath.sqrt(3).real and y1 > 0 and yy1 == 0:
                    # if y1 < 2 * cmath.sqrt(3).real and y1 > cmath.sqrt(3).real * x1 and y1 > -cmath.sqrt(
                    #         3).real * x1 and yy1 == 0:

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
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xa) + " " + str(chushi_ya)+"|"+str(tmp_chaa)
                            print str(x1) + " " + str(y1) + " |" + str(chushi_xb) + " " + str(chushi_yb)+"|"+str(tmp_chab)

                            chaa.append(tmp_chaa)
                            chab.append(tmp_chab)


                    if x1 > -2 and x1 < 2 and y2 < 2 * cmath.sqrt(3).real and y2 > 0 and yy2 == 0:
                    # if y2 < 2 * cmath.sqrt(3).real and y2 > cmath.sqrt(3).real * x1 and y2 > -cmath.sqrt(
                    #         3).real * x1 and yy2 == 0:

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
                            print str(x1) + " " + str(y2) + " |" + str(chushi_xa) + " " + str(chushi_ya)+"|"+str(tmp_chaa)
                            print str(x1) + " " + str(y2) + " |" + str(chushi_xb) + " " + str(chushi_yb)+"|"+str(tmp_chab)
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
    all_xa=0
    all_ya = 0
    all_xb = 0
    all_yb = 0
    flaga=0
    flagb=0
    gea=0
    geb=0
    print"^^^^^^^^^^^^^^"
    print chushi_xa
    print chushi_ya
    print chushi_xb
    print chushi_yb
    print re_la

    copy_chaa = copy.deepcopy(chaa)
    while flaga<0.6:

        min_chaa=chaa.index(min(copy_chaa))
        min_num = copy_chaa.index(min(copy_chaa))

        end_xa = re_la[min_chaa][0, 0]
        end_ya = re_la[min_chaa][0, 1]
        all_xa=end_xa+all_xa
        all_ya=end_ya+all_ya
        gea=gea+1
        print copy_chaa
        copy_chaa.pop(min_num)
        print copy_chaa
        flaga = min(copy_chaa)
        print "AAAAAAAAAAAAAAAAAAAAAAA"
        print end_xa
        print end_ya
    print "gea"+"    "+str(gea)
    print all_xa
    print all_ya
    end_xaa=all_xa/gea
    end_yaa=all_ya/gea
    print end_xaa
    print end_yaa

    copy_chab = copy.deepcopy(chab)
    while flagb < 0.6:

        min_chab = chab.index(min(copy_chab))
        min_num = copy_chab.index(min(copy_chab))

        end_xb = re_la[min_chab][0, 0]
        end_yb = re_la[min_chab][0, 1]
        all_xb=end_xb+all_xb
        all_yb=end_yb+all_yb
        geb=geb+1
        print copy_chab
        copy_chab.pop(min_num)
        print copy_chab
        flagb = min(copy_chab)
        print "BBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        print end_xb
        print end_yb
    print "geb" + "    " + str(geb)
    print all_xb
    print all_yb
    end_xbb = all_xb / geb
    end_ybb = all_yb / geb
    print end_xbb
    print end_ybb

    return end_xaa, end_yaa, end_xbb, end_ybb














