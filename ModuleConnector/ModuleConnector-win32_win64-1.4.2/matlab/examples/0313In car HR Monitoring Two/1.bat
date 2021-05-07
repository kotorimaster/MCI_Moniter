D:
CD D:\app\wireshark
adb devices
adb -s 7f63b3fc  pull /sdcard/btsnoop_hci.log C:\Users\mengyao\Desktop\1
tshark -r "C:\Users\mengyao\Desktop\1\btsnoop_hci.log" -T fields -e frame.time >"C:\Users\mengyao\Desktop\1\time.txt"
tshark -r "C:\Users\mengyao\Desktop\1\btsnoop_hci.log" >"C:\Users\mengyao\Desktop\1\value.txt" -x
