D:
CD D:\app\wireshark
adb devices
adb -s 129bb17d  pull /sdcard/btsnoop_hci.log C:\Users\mengyao\Desktop\2
tshark -r "C:\Users\mengyao\Desktop\2\btsnoop_hci.log" -T fields -e frame.time >"C:\Users\mengyao\Desktop\2\time.txt"
tshark -r "C:\Users\mengyao\Desktop\2\btsnoop_hci.log" >"C:\Users\mengyao\Desktop\2\value.txt" -x
