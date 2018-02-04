# -*- coding: utf-8 -*-

from raijin.raijin import Raijin
import time

# Create Raijin object
raijin = Raijin()

cdate = raijin.getCurDate()
ctime = raijin.getCurTime()

print("Current data an time: " + cdate + " " + ctime)
start_time = time.time()
print("Period for Tarriff 3.1: " + raijin.getTariff("3.1"))
print("--- %s seconds ---" % (time.time() - start_time))