D:
CD D:\app\wireshark
adb devices
adb -s d4146ac1  pull /sdcard/btsnoop_hci.log C:\Users\mengyao\Desktop\3
tshark -r "C:\Users\mengyao\Desktop\3\btsnoop_hci.log" -T fields -e frame.time >"C:\Users\mengyao\Desktop\3\time.txt"
tshark -r "C:\Users\mengyao\Desktop\3\btsnoop_hci.log" >"C:\Users\mengyao\Desktop\3\value.txt" -x
