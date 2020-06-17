#!/usr/bin/env python
#Commit sha eb88bb802d5c9b5cc67b0ee35b0992c866780192 old log renamer, copy this script to log directory and run it
import os 
#print(os.listdir())
arg1=[]
arg2=[]
for i in os.listdir():
    if(i[-3:]==".gz"):
        arg1.append(i)
        date=i.split("_")[1].split(".")[0]
        year=((date[::-1])[0:4])[::-1]
        month=((date[::-1])[4])[::-1]
        day=((date[::-1])[5:])[::-1]
        #print(date,end="\t")
        assemble="apcupsmon_"+day.zfill(2)+month.zfill(2)+year+".log.gz"
        arg2.append(assemble)
        os.system("mv "+i+" "+assemble)
        #print("Year=",year,"month=",month,"day=",day)
        #print(i.split("_")[1].split(".")[0])
        #l.append(i)
#print(l)
print(arg1)
print(arg2)
