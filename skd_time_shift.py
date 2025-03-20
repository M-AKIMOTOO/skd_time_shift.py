#!/usr/bin/env python3 
# AKIMOTO
# 2025-03-20

import datetime, os, sys, argparse

# arguments
class MyHelpFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass
parser = argparse.ArgumentParser(formatter_class=MyHelpFormatter)  

help_skd         = "skd file"
help_dayshift    = "Delay or advance day (e.g. -d/--day-shift -1/1. it represents previous/subsequent days of obserbation days in the skd-file)"
help_hourshift   = "Delay or advance hour (e.g. -H/--hour-shift -1/1)"
help_minuteshift = "Delay or advance minute (e.g. -m/--minute-shift -1/1). An observation time turn back 4 minutes every day. In addition its time proceed 1 minute every 15 days. However, this program does not consider them."
help_secondshift = "Delay or advance second (e.g. -s/--second-shift -1/1)"


parser.add_argument("-i", "--ifile"       , default=0, type=str               , help=help_skd)
parser.add_argument("-d", "--day-shift"   , default=0, type=int, dest="day"   , help=help_dayshift )
parser.add_argument("-H", "--hour-shift"  , default=0, type=int, dest="hour"  , help=help_hourshift)
parser.add_argument("-m", "--minute-shift", default=0, type=int, dest="minute", help=help_minuteshift)
parser.add_argument("-s", "--second-shift", default=0, type=int, dest="second", help=help_secondshift)


args = parser.parse_args() 
ifile  = args.ifile
day    = args.day
hour   = args.hour
minute = args.minute
second = args.second

print("------------------------------------------")
print("Dealy or Advance Your Observation Schedule")
print("")
print("  Skd     -->  %s" % ifile)
print("  Days    -->  %d" % day)
print("  Hours   -->  %d" % hour)
print("  Minutes -->  %d" % minute)
print("  Seconds -->  %d" % second)
print("------------------------------------------")
print("")
print("  Before       -->  After")
print("")

iskd = open(ifile, "r").readlines()

i = 0
s = False
exper = ""
oskd = ""
for lines in iskd :
    
    line = lines.split()
    
    if "$EXPER" in line : exper = line[1]; continue
    
    if "$SKED" in line : oskd += lines; s = True
    
    if not s :  oskd += lines
    
    if s and line[0] != "$SKED" :
        
        i += 1
        
        scantime = datetime.datetime.strptime(line[1], "%y%j%H%M%S")
        scantime_shift = scantime + datetime.timedelta(days=day, hours=hour, minutes=minute, seconds=second)
        scantime_shift = datetime.datetime.strftime(scantime_shift, "%y%j%H%M%S")
        print(f"  {line[1]}  -->  {scantime_shift}")
        line[1] = scantime_shift
        oskd += "%-8s     %s  %5s    %s\n" % (line[0], line[1], line[2], "  ".join(line[3:]))
        
        if i == 1 :
            obsyyyyddd = scantime_shift[:5]

print("")
oname = os.path.dirname(ifile) + "/" + os.path.basename(ifile)[:1] + obsyyyyddd + os.path.basename(ifile)[6:]
#if os.path.isfile(oname) :
#    print("File (%s) exist!!" % oname)
#    print("Please set commandline arguments or erase an inputted file when you execute this program.")
#    print("program stop...")
#    exit()
ofile = open(oname, "w")
ofile.write("$EXPER %s\n" % (exper[:1]+obsyyyyddd+exper[6:]))
ofile.write(oskd)
ofile.close()
print(f"Make {oname}")

