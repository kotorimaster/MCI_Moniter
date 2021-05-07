def multi(a3_list,lcs1,lcs2,rang1,rang2, mmii1, mmii2,mmii1_na,mmii2_na,wg1,wg2):
    if (len(a3_list) == 1):
        print(a3_list[0][0])
        print("111111111111111111111111111111111111111111111111111")
        wc1 = abs(a3_list[0][0] - lcs1)
        wc2 = abs(a3_list[0][0] - lcs2)
        if (wc1 >= wc2):
            if (wc2 < 0.4):
                rang2 = a3_list[0][0]
                rang1 = lcs1
        else:
            rang2 = lcs2
            rang1 = a3_list[0][0]
        lcs1 = rang1
        lcs2 = rang2
        print("////////////////////////////////////////")
        print(rang1)
        print(rang2)
    if (len(a3_list) == 2):
        print("2222222222222222222222222222222222222222")
        wc1 = abs(a3_list[0][0] - lcs1)
        wc2 = abs(a3_list[0][0] - lcs2)
        wc11 = abs(a3_list[1][0] - lcs1)
        wc22 = abs(a3_list[1][0] - lcs2)
        print(lcs1)
        print(lcs2)
        print(a3_list[0][0])
        minmin = min(wc1, wc2, wc11, wc22)
        if (wc1 == minmin):
            if (minmin < 0.4):
                rang1 = a3_list[0][0]
                if (wc22 < 0.4):
                    rang2 = a3_list[1][0]
                else:
                    rang2 = lcs2
            else:
                rang1 = lcs1
                rang2 = lcs2
        elif (wc2 == minmin):
            if (minmin < 0.4):
                rang2 = a3_list[0][0]
                if (wc11 < 0.4):
                    rang1 = a3_list[1][0]
                else:
                    rang1 = lcs1
            else:
                rang1 = lcs1
                rang2 = lcs2
        elif (wc11 == minmin):
            if (minmin < 0.4):
                rang1 = a3_list[1][0]
                if (wc2 < 0.4):
                    rang2 = a3_list[0][0]
                else:
                    rang2 = lcs2
            else:
                rang1 = lcs1
                rang2 = lcs2
        else:

            if (minmin < 0.4):
                rang2 = a3_list[1][0]
                if (wc1 < 0.4):
                    rang1 = a3_list[0][0]
                else:
                    rang1 = lcs1
            else:
                rang1 = lcs1
                rang2 = lcs2

        # if (wc1 <=wc11):
        #     if(wc11<0.4):
        #         rang1 = a3_list[1][0]
        # elif(wc1< wc2):
        #     if (wc1 < 0.4):
        #         rang1 = a3_list[0][0]
        # else:
        #     rang1 = lcs1
        # if (wc2 >= wc22):
        #     if(wc22<0.4):
        #         rang2 = a3_list[1][0]
        # elif(wc2< wc22):
        #     if (wc2 < 0.4):
        #         rang1 = a3_list[0][0]
        # else:
        #     rang2 = lcs2
        lcs1 = rang1
        lcs2 = rang2
        print("////////////////////////////////////////")
        print(lcs1)
        print(lcs2)

    if (len(a3_list) > 2):
        print("333333333333333333333333333333333333333")
        print(lcs1)
        print(lcs2)

        for iii in range(len(a3_list)):
            mmii1.append(abs(a3_list[iii][0] - lcs1))
            mmii2.append(abs(a3_list[iii][0] - lcs2))
            mmii1_na.append(a3_list[iii][0] - lcs1)
            mmii2_na.append(a3_list[iii][0] - lcs2)
        th = min(mmii1)
        TT = mmii1.index(th)
        print("------------------------")
        print(TT)

        th2 = min(mmii2)
        print(th)
        print(th2)
        for itt in range(1 + int((len(a3_list) - 2) // 1.5)):
            print(mmii1_na)
            print(mmii2_na)
            index1 = mmii1.index(min(mmii1))
            index2 = mmii2.index(min(mmii2))

            if (min(mmii1) <= th * 3):
                wg1.append(mmii1_na[index1] + lcs1)

            if (min(mmii2) <= th2 * 3):
                wg2.append(mmii2_na[index2] + lcs2)
            mmii1.remove(min(mmii1))
            mmii2.remove(min(mmii2))
            mmii1_na.pop(index1)
            mmii2_na.pop(index2)
        junzhi1 = 0
        junzhi2 = 0
        if (len(wg1) != 0 and len(wg2) != 0):
            print(len(wg2))
            for iiii in range(len(wg1)):
                junzhi1 = junzhi1 + wg1[iiii]
            for iiiii in range(len(wg2)):
                junzhi2 = junzhi2 + wg2[iiiii]
            if (abs(junzhi1 / len(wg1) - lcs1) < 0.4):
                rang1 = junzhi1 / len(wg1)
            else:
                rang1 = lcs1
            if (abs(junzhi2 / len(wg2) - lcs2) < 0.4):
                rang2 = junzhi2 / len(wg2)
            else:
                rang2 = lcs2
            lcs1 = rang1
            lcs2 = rang2
        else:
            rang1 = lcs1
            rang2 = lcs2
            lcs1 = rang1
            lcs2 = rang2
    print("00000000000000000000000")
    print(rang1)
    print(rang2)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print(lcs1)
    print(lcs2)


    return rang1,rang2,lcs1,lcs2
