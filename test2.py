minute, prev_minute = 460, 432
a = (1000000000 - prev_minute) % (minute - prev_minute)
print(a)