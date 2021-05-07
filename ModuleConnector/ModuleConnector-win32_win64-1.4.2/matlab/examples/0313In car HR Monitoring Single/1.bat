E:
CD E:\wireshark
adb devices
adb -s 129bb17d  pull /sdcard/btsnoop_hci.log C:\Users\93435\Desktop\1
tshark -r "C:\Users\93435\Desktop\1\btsnoop_hci.log" -T fields -e frame.time >"C:\Users\93435\Desktop\1\time.txt"
tshark -r "C:\Users\93435\Desktop\1\btsnoop_hci.log" >"C:\Users\93435\Desktop\1\value.txt" -x
