#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import os
import csv
import sys
import datetime
log_file = sys.argv[1]
# log_file = r"C:\Users\li_ran\Desktop\KPI\ios_app_log1.log"
csv_content = []
# new_csv = sys.argv[2]
new_csv = r"result.csv"
csv_name = os.path.splitext(log_file)[0] + ".csv"
csvfile = file(csv_name, 'wb')
writer = csv.writer(csvfile)

"""
Aug 21 15:13:32 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>uninit start  = 1408605212132.380859 ms
Aug 21 15:13:32 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>uninit end  = 1408605212135.940918 ms
Aug 21 15:13:32 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>init start  = 1408605212137.761230 ms
Aug 21 15:13:32 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>init end  = 1408605212187.838135 ms
Aug 21 15:13:32 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>VOOSMP_SRC_PID_DRM_UNIQUE_IDENTIFIER value:or3ZXLBpDjPmNw/yvqZ+TJD8iQY=
Aug 21 15:13:32 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>open start  = 1408605212215.539062 ms
Aug 21 15:13:32 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>open itself using  = 21.567871 ms
Aug 21 15:13:33 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>> open finished  = 1408605213809.140869 ms
Aug 21 15:13:33 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>open finish run start  = 1408605213810.347168 ms
Aug 21 15:13:33 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>run end  = 1408605213812.279053 ms run using time = 1.936768
Aug 21 15:13:33 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>buffer start  = 1408605213817.316895 ms
Aug 21 15:13:34 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>buffer using time = 462.166965 ms
Aug 21 15:13:34 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>buffer stop  = 1408605214279.786133 ms
Aug 21 15:13:34 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>buffer start  = 1408605214280.173096 ms
Aug 21 15:13:34 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>buffer using time = 407.495975 ms
Aug 21 15:13:34 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>buffer stop  = 1408605214688.269043 ms
Aug 21 15:13:34 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>seek complete  = 1408605214687.869141 ms
Aug 21 15:13:34 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>open to render time = 2473.680973 ms
Aug 21 15:13:34 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>render start  = 1408605214689.552979 ms
Aug 21 15:13:36 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>stop start  = 1408605216348.291992 ms
Aug 21 15:13:37 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>stop end  = 1408605217202.619141 ms, stop using time: 854.336914
Aug 21 15:13:37 Viviande-mini2 Ericsson_SamplePlayer[1886] <Warning>: >>>>>>>>>>close start  = 1408605217204.575928 ms
"""
# pattern_Init = "Init using time.{2}(\d*) ms,"
pattern_Open = "\w{3} \d{2} \d{2}:\d{2}:\d{2}.{65}open itself using\s{1,2}= (\d*\.\d*) ms"
# pattern_Open_Complete = "Open complete using time.{2}(\d*) ms,"
pattern_Run = "\w{3} \d{2} \d{2}:\d{2}:\d{2}.{100}run using time.{3}(\d*\.\d*)"
pattern_Buffer = "\w{3} \d{2} \d{2}:\d{2}:\d{2}.{65}buffer using time\s{1,2}= (\d*\.\d*) ms"
pattern_Open_Render = "\w{3} \d{2} \d{2}:\d{2}:\d{2}.{65}open to render time.{3,4}(\d*\.\d*) ms"
pattern_Stop = '\w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}\s.{101}stop using time:\s(\d*\.\d*)'
pattern_IsHandshakeVerified = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR IsHandshakeVerified"
pattern_SetLogging = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR SetLogging"
pattern_SetVCASCommunicationHandlerSettings = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR SetVCASCommunicationHandlerSettings"
pattern_CheckVCASConnection = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR CheckVCASConnection"
pattern_Decrypt = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR Decrypt+"
pattern_IsDeviceProvisioned = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR IsDeviceProvisioned"
pattern_ConnectAndProvisionDevice = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR ConnectAndProvisionDevice"


patternDic = {
              # "Init": pattern_Init,
              "Open": pattern_Open,
              "Stop": pattern_Stop,
              "Run": pattern_Run,
              "Buffer": pattern_Buffer,
              "Open_to_render": pattern_Open_Render,
              "IsHandshakeVerified": pattern_IsHandshakeVerified,
              "SetLogging": pattern_SetLogging,
              "SetVCASCommunicationHandlerSettings":
              pattern_SetVCASCommunicationHandlerSettings,
              "CheckVCASConnection": pattern_CheckVCASConnection,
              "IsDeviceProvisioned": pattern_IsDeviceProvisioned,
              "ConnectAndProvisionDevice": pattern_ConnectAndProvisionDevice,
              "Decrypt": pattern_Decrypt,
              }

patternList1 = ["Open", "Stop", "Run",
                "Buffer", "Open_to_render"]

patternList2 = ["IsHandshakeVerified", "SetLogging",
                "SetVCASCommunicationHandlerSettings",
                "ConnectAndProvisionDevice",
                "IsDeviceProvisioned",
                "CheckVCASConnection",
                "Decrypt"]

patternList = patternList1 + patternList2
writer.writerow(patternList)


def timeshift(inputtime, outputtime):
    time1 = datetime.datetime.strptime(inputtime, '%H:%M:%S.%f')
    time2 = datetime.datetime.strptime(outputtime, '%H:%M:%S.%f')
    timeshift1 = abs(((time2 - time1).microseconds) / 1000.)
    return timeshift1


def segmentLog(logfile):
    """切分log，以便单独分析每段log"""
    f = open(logfile, "rb")
    flag1 = 1  # flag for readline
    # segment_start = "Init using time"
    segment_stop = ">>>>>>>>>>close end"
    tempList = []  # counter for readline
    content = []
    new_content = []

    while flag1:
        line = f.readline()
        tempList.append(line)
        # if re.search(segment_stop, line):  # keyword is in that line
        if line.find(segment_stop) >= 0:
            # print line
            temp = ''.join(tempList)
            content.append(temp)
            tempList = []
        else:
            pass
        if not line:
            flag1 = 0
            break

    # for each_segment in content:
    #     for each_line in each_segment.splitlines():
    #         if each_line.find(segment_start) >= 0:
    #             new_segment = each_segment[each_segment.index(each_line):]
    #             new_content.append(new_segment)
    return content


def text2list(logfile):
    """translate text segment to new dictionary: {"Stop":xx, "Close":yy..}"""
    #content = open("1.txt", "rb").read()
    content = segmentLog(logfile)
    print content
    segmentDicList = {}
    segmentList = []
    for segment in content:
        #print segment
        print '*' * 20
        for key, vaule in patternDic.items():
            result = re.findall(vaule, str(segment))
            if key in patternList1:  # 当关键字只能是唯一的时候
                # 如果搜寻不到，打印错误并且设置输出值为空
                try:
                    segmentDicList[key] = result[0]
                except Exception as e:
                    print key
                    print e
                    segmentDicList[key] = " "
            else:  # 当关键字应该出现2次的情况
                if len(result) == 2:
                    segmentDicList[key] = timeshift(result[0], result[1])
                elif len(result) > 2:  # 如果出现多于2次的数据，取前两次
                    print result
                    segmentDicList[key] = timeshift(result[0], result[1])
                else:
                    segmentDicList[key] = " "
        segmentList.append([segmentDicList[key] for key in patternList])
    return segmentList


if __name__ == '__main__':
    line_list = text2list(log_file)
    # line_list = segmentLog(log_file)
    for i in line_list:
        print i
        print "____________"
        writer.writerow(i)
    csvfile.close()
