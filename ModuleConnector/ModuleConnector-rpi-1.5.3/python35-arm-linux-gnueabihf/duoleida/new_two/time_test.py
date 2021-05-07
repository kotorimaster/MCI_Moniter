import time
a= time.asctime(time.localtime(time.time()))
print(a)
aa1=a[11:13]
aa2=a[14:16]
aa3=a[17:19]


print(int(aa1)*10000+int(aa2)*100+int(aa3))
print(aa2)
print(aa3)