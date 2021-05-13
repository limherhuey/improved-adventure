
##### Change "Last Modified" time of a file #####

import os, time, datetime

# get file path
print("-- Enter path of file to be changed --")
filepath = input("")

# print current datetimes
old_atime = os.path.getatime(filepath) # store original Access Time value
print('\nLast Modified:\t', time.ctime(os.path.getmtime(filepath)))
print('Created:\t', time.ctime(os.path.getctime(filepath)))
print('Accessed:\t', time.ctime(old_atime), "\n")

# get user input on new time
print("-- Enter new datetime --")
year = int(input("Year: "))
month = int(input("Month: "))
day = int(input("Day: "))
hour = int(input("Hour: "))
minute = int(input("Minute: "))
second = int(input("Second: "))

# convert to seconds since epoch
date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
new_mtime = time.mktime(date.timetuple())

# alter Last Modified time
os.utime(filepath, (old_atime, new_mtime))

# print new datetimes
print('\nLast Modified:\t', time.ctime((os.path.getmtime(filepath))))
print('Created:\t', time.ctime((os.path.getctime(filepath))))
print('Accessed:\t', time.ctime((os.path.getatime(filepath))))
