__author__ = 'Matt Eland'

import time

import wmi
import win32com.client


c = wmi.WMI()
for s in c.Win32_Service():
    if s.State == 'Stopped':
        print s.Caption, s.State

obj = win32com.client.Dispatch("WbemScripting.SWbemRefresher")
# Create refresher object

WMIService = wmi.GetObject("winmgmts:\\root\cimv2")
#pointer to local WMI service to pass refresher

diskItems = obj.AddEnum(WMIService, "Win32_PerfFormattedData_PerfDisk_PhysicalDisk").objectSet
processorItems = obj.AddEnum(WMIService, "Win32_PerfFormattedData_PerfOS_Processor").objectSet
networkItems = obj.AddEnum(WMIService, "Win32_PerfFormattedData_Tcpip_NetworkInterface").objectSet
#add services you wish to monitor to refresher, and create pointers to the data
#structures that they modify when you call obj.Refresh()

while 1:
    obj.Refresh()  #Refresh all performance counters
    for item in diskItems:
        print item.Name, " ",
        print item.PercentDiskTime,
        print item.PercentIdleTime,
        print item.DiskReadsPerSec,
        print item.Timestamp_Sys100NS

    for item in processorItems:
        print item.Name, " ",
        print item.PercentProcessorTime, "%"

    for item in networkItems:
        if item.BytesTotalPerSec != "0":  #Screen out spurious network connections (most systems have several for loopback or internal use)
            print item.Description, item.Name
            print "Down", item.BytesReceivedPerSec, "B/s",
            print "Up", item.BytesSentPerSec, "B/s",
            print "Total", item.BytesTotalPerSec, "B/s"

    time.sleep(.5)