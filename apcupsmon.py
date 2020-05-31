#!/usr/bin/env python3
import os
import time
import sys
from datetime import datetime
from datetime import timedelta
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r",low=0,returnLine=True):
# thanks to https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    #percent = ("{0:." + str(decimals) + "f}").format(100 * ((iteration-low) / float(total)))
    filledLength = int(length * (iteration-low) // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    if(returnLine):
        print('\r%s |%s| %s%s' % (prefix, bar, iteration, suffix), end = printEnd)
    else:
        print('%s |%s| %s%s' % (prefix, bar, iteration, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
def fileToCumPower(newpath):
    #pass1 - get average
    inputFileName=newpath
    #inputFileName="apcupsmon_2652020.log.gz"
    fileName=None
    compress=False # Compress any way but can be changed to true to not preserve state...
    if(inputFileName.endswith(".gz")):
        #detected gz compression
        compress=True
        os.system("gunzip "+inputFileName)
        fileName=inputFileName[:-3]
    else:
        fileName=inputFileName
    entries=0
    averageVolt=0
    averageWatt=0
    averageLoad=0
    f=open(fileName)
    f.readline()
    while(True):
        line=f.readline()
        if(line=='\n' or line==""):
            break
        else:
            time,volt,watt,load,transfers=line.strip().split("\t")
            hrs,minutes,seconds=time.split(":")
            averageLoad+=int(load)
            averageVolt+=int(volt)
            averageWatt+=int(watt)
            entries+=1
    f.close()
    #print(averageLoad,averageVolt,averageWatt)
    averageLoad/=entries
    averageWatt/=entries
    averageVolt/=entries
    #print(averageLoad,averageVolt,averageWatt)


    #pass2 - get wattage
    cumWattsSeconds=0
    cumTime=0
    f=open(fileName)
    f.readline()
    prev=None
    run=True
    while(run):
        time,volt,watt,load,transfers=[0,0,0,0,0]
        hrs,minutes,seconds=[0,0,0]
        while True:
            line=f.readline()
            if(line==""):
                run=False
                break
            try:
                time,volt,watt,load,transfers=line.strip().split("\t")
                hrs,minutes,seconds=time.split(":")
                break
            except:
                print("Error",line)
        if(run==False):
            break
        else:
            if(prev==None):
                prev=[hrs,minutes,seconds]
            else:
                t1=timedelta(hours=int(prev[0]),minutes=int(prev[1]),seconds=int(prev[2]))
                t2=timedelta(hours=int(hrs),minutes=int(minutes),seconds=int(seconds))
                if((t2-t1).seconds>1):
                    cumWattsSeconds+=(averageWatt)*((t2-t1).seconds-1)
                    cumTime+=(t2-t1).seconds-1
                prev=[hrs,minutes,seconds]
            cumWattsSeconds+=int(watt)
            cumTime+=1
    f.close()
    if(compress):
        os.system("gzip "+fileName)
    cumTimeHrs=cumTime/60/60
    cumWattHrs=cumWattsSeconds/60/60
    print("Estimate for date",fileName.split("_")[1].replace(".log",""))
    print("Watt Hours for ",cumTimeHrs,"is ",cumWattHrs)
    cumWatt24Hrs=(cumWattHrs/cumTimeHrs)*24
    print("Watt Hours projected for 24hrs",cumWatt24Hrs)
    return(cumTimeHrs,cumWattHrs,cumWatt24Hrs)
plot=False
log=True
path="/var/log/apcupsmon"
if(len(sys.argv)>=2):
    if("--analyze" in " ".join(sys.argv) or "-a" in " ".join(sys.argv)):
        newpath=None
        try:
            try:
                newpath=sys.argv[sys.argv.index("--analyze")+1]
            except:
                newpath=sys.argv[sys.argv.index("-a")+1]
            if("--" in newpath or "-p" in newpath or "-l" in newpath or "-f" in newpath or "-a" in newpath):
                print("Invalid path!")
                exit(-1)
            path=newpath
        except Exception as e:
            print(e)
            print("Path requires an argument!")
            exit(-1)
        #to be added function
        fileToCumPower(newpath)
        exit(0)
    if("--help" in " ".join(sys.argv) or "-h" in " ".join(sys.argv)):
        print("Example use cases")
        print(sys.argv[0],"-p # to plot and log to /var/log/apcupsmon")
        print(sys.argv[0],"-p -l # to plot without logging")
        print(sys.argv[0],"-p -f <path> # to plot and log to the path")
        print(sys.argv[0],"-f <path> # dont plot, just log to the path")
        print(sys.argv[0],"-a <file> # analyzes the log and gives a summary")
        print(sys.argv[0],"-h or --help for help")
        print("-p can be replaced with --plot")
        print("-l can be replaced with --nolog")
        print("-f can be replaced with --path")
        print("-a can be replaced with --analyze")
        exit()
    if("--plot" in " ".join(sys.argv) or "-p" in " ".join(sys.argv)):
        plot=True
    if("--nolog" in " ".join(sys.argv) or "-l" in " ".join(sys.argv)):
        log=False
    if("--path" in " ".join(sys.argv) or "-f" in " ".join(sys.argv)):
        try:
            newpath=None
            try:
                newpath=sys.argv[sys.argv.index("--path")+1]
            except:
                newpath=sys.argv[sys.argv.index("-f")+1]
            if("--" in newpath or "-p" in newpath or "-l" in newpath or "-f" in newpath or "-a" in newpath):
                print("Invalid path!")
                exit(-1)
            path=newpath
        except Exception as e:
            print(e)
            print("Path requires an argument!")
            exit(-1)
else:
    print("No arguments detected, contiuing with default")
if(log==False and plot==False):
    print("Northing to do, exiting")
    print("Try -h for help")
    exit()
if(log):
    if(os.path.exists(path)==False):
        try:
            os.mkdir(path)
        except PermissionError:
            print("Permission denied creating "+path)
            exit(-1)
oldfile=None
while(True):
    try:
        #os.system("clear")
        p=os.popen("apcaccess")
        voltage=0
        load=0
        wattage=0
        low=180
        up=288
        transfers=0
        while(True):
            line=p.readline()
            if(line):
                if("LINEV" in line):
                    voltage=float(line.split(":")[1].split(" ")[1])
                elif("LOADPCT" in line):
                    load=float(line.split(":")[1].split(" ")[1])
                elif("NOMPOWER" in line):
                    wattage=load/100*float(line.split(":")[1].split(" ")[1])
                elif("LOTRANS" in line):
                    low=int(float(line.split(":")[1].split(" ")[1]))
                elif("HITRANS" in line):
                    up=int(float(line.split(":")[1].split(" ")[1]))
                elif("NUMXFERS" in line):
                    transfers=int(float(line.split(":")[1].split(" ")[1]))
            else:
                break
        #print(voltage,load,wattage)
        columns = int(os.popen('stty size', 'r').read().split()[1])
        if(log):
            now=datetime.now()
            filename="apcupsmon_"+str(now.day)+str(now.month)+str(now.year)+".log"
            if(oldfile!=filename):
                f=None
                if(path[-1]=="/"):
                    if(oldfile!=None):
                        os.system("gzip "+path+oldfile)
                    if(not os.path.exists((path+filename))):
                        f=open(path+filename,"w")
                else:
                    if(oldfile!=None):
                        os.system("gzip "+path+"/"+oldfile)
                    if(not os.path.exists((path+"/"+filename))):
                        f=open(path+"/"+filename,"w")
                if(f):
                    f.write("Time\tVolt\tWatt\tLoad(%)\tTransfers\n")
                    f.close()
                oldfile=filename
            if(path[-1]=="/"):
                f=open(path+filename,"a")
            else:
                f=open(path+"/"+filename,"a")
            f.write(str(now.hour)+":"+str(now.minute)+":"+str(now.second)+"\t")
            f.write(str(int(voltage))+"\t")
            f.write(str(int(wattage))+"\t")
            f.write(str(int(load))+"\t")
            f.write(str(int(transfers))+"\n")
            f.close()
        if(plot):
            if(columns-50>5):
                printProgressBar(load,100,"Load ","% ("+str(int(wattage))+"W)",length=int((columns-45)/2),printEnd="")
                printProgressBar(voltage,up,"\tVolt ","V",printEnd="\n",length=int((columns-45)/2),returnLine=False,low=low)
            else:
                print("Terminal Size Error")
        time.sleep(1)
    except KeyboardInterrupt:
        print("Bye...")
        break