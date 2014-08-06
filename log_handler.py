# -*- coding:utf-8 -*-

import re
import os
import csv
import sys
import datetime
log_file = sys.argv[1]
# log_file = r"1.txt"
csv_content = []
# new_csv = sys.argv[2]
new_csv = r"result.csv"
csv_name = os.path.splitext(log_file)[0] + ".csv"
csvfile = file(csv_name, 'wb')
writer = csv.writer(csvfile)

"""
2.log:07-29 16:21:59.250 I/[APP][Time](27331): Init using time: 63 ms, current time: 1406622119262 ms
2.log:07-29 16:21:59.770 I/[APP][Time](27331): Open using time: 105 ms, current time: 1406622119781 ms
2.log:07-29 16:22:00.010 I/[APP][Time](27331): Open complete using time: 348 ms, current time: 1406622120024 ms
2.log:07-29 16:22:00.120 I/[APP][Time](27331): Run using time: 105 ms, current time: 1406622120130 ms
2.log:07-29 16:22:00.120 I/VOLOG   (27331): 16:22:00.131 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 138, VR IsHandshakeVerified+
2.log:07-29 16:22:00.120 I/VOLOG   (27331): 16:22:00.132 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 140, VR IsHandshakeVerified- 1
2.log:07-29 16:22:00.120 I/VOLOG   (27331): 16:22:00.132 @@@VOLOG,   Info, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, CheckDeviceVCASStatus, 336, VR SetVCASCommunicationHandlerSettings+ \data\data/com.visualon.AppUI/
2.log:07-29 16:22:01.370 I/VOLOG   (27331): 16:22:01.379 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, CheckDeviceVCASStatus, 338, VR SetVCASCommunicationHandlerSettings- 0
1.log:07-29 16:21:37.140 I/VOLOG   (27331): 16:21:37.150 @@@VOLOG,    Run, 0A030000, 02167790, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 259, VR SetLogging+
1.log:07-29 16:21:37.140 I/VOLOG   (27331): 16:21:37.151 @@@VOLOG,    Run, 0A030000, 02167790, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 261, VR SetLogging-
2.log:07-29 16:22:03.770 I/VOLOG   (27331): 16:22:03.784 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, CheckDeviceVCASStatus, 397, VR CheckVCASConnection+
2.log:07-29 16:22:05.800 I/VOLOG   (27331): 16:22:05.814 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, CheckDeviceVCASStatus, 399, VR CheckVCASConnection- 0
2.log:07-29 16:22:05.850 I/VOLOG   (27331): 16:22:05.861 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, OnSourceDrm, 829, VR Decrypt+ 601600
2.log:07-29 16:22:06.120 I/VOLOG   (27331): 16:22:06.127 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, OnSourceDrm, 831, VR Decrypt- 0 601600
2.log:07-29 16:22:06.330 I/VOLOG   (27331): 16:22:06.340 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, OnSourceDrm, 829, VR Decrypt+ 492944
2.log:07-29 16:22:06.450 I/VOLOG   (27331): 16:22:06.466 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, OnSourceDrm, 831, VR Decrypt- 0 492944
2.log:07-29 16:22:06.650 I/VOLOG   (27331): 16:22:06.658 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 138, VR IsHandshakeVerified+
2.log:07-29 16:22:06.650 I/VOLOG   (27331): 16:22:06.659 @@@VOLOG,    Run, 0A030000, 01FA7E60, DRM_Verimatrix_AES128_Other.cpp, VerifyVR, 140, VR IsHandshakeVerified- 1
2.log:07-29 16:22:06.870 I/[APP][Time](27331): Buffer using time: 6734 ms, current time: 1406622126885 ms
2.log:07-29 16:22:06.970 I/[APP][Time](27331): Open to render using time: 7308 ms, current time: 1406622126984 ms

"""
pattern_Init = "Init using time: (\d*) ms,"
pattern_Open = "Open using time: (\d*) ms,"
pattern_Open_Complete = "Open complete using time: (\d*) ms,"
pattern_Run = "Run using time: (\d*) ms,"
pattern_Buffer = "Buffer using time: (\d*) ms,"
pattern_Open_Render = "Open to render using time: (\d*) ms,"
pattern_IsHandshakeVerified = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR IsHandshakeVerified"
pattern_SetLogging = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR SetLogging"
pattern_SetVCASCommunicationHandlerSettings = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR SetVCASCommunicationHandlerSettings"
pattern_CheckVCASConnection = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR CheckVCASConnection"
pattern_Decrypt = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR Decrypt+"
pattern_IsDeviceProvisioned = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR IsDeviceProvisioned"
pattern_ConnectAndProvisionDevice = ".*I/VOLOG.*: (\d*:\d*:\d*.\d{3}) .* VR ConnectAndProvisionDevice"


patternDic = {"Init": pattern_Init,
              "Open": pattern_Open,
              "Open_Complete": pattern_Open_Complete,
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

patternList1 = ["Init", "Open", "Open_Complete", "Run",
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
    f = open(logfile, "rb")
    flag1 = 1  # flag for readline
    segment_stop = ".*Open to render using time:.*"
    # segment_start = ".*Init using time:.*"
    tempList = []  # counter for readline
    content = []
    while flag1:
        line = f.readline()
        # print re.search(segment_start, line)
        # print re.search(segment_stop, line)
        tempList.append(line)
        if re.search(segment_stop, line):  # keyword is in that line
            temp = ''.join(tempList)
            content.append(temp)
            tempList = []
        else:
            pass
        if not line:
            flag1 = 0
            break
    # print content
    new_content = []
    for each_segment in content:
        for each_line in each_segment.splitlines():
            if each_line.find("Init using time") >= 0:
                new_segment = each_segment[each_segment.index(each_line):]
                new_content.append(new_segment)
    return new_content


def text2list(logfile):
    """translate text segment to new dictionary: {"Stop":xx, "Close":yy..}"""
    #content = open("1.txt", "rb").read()
    content = segmentLog(logfile)
    segmentDicList = {}
    segmentList = []
    for segment in content:
        print segment
        print '*' * 20
        for key, vaule in patternDic.items():
            result = re.findall(vaule, str(segment))
            # if len(result) == 1:
            if key in patternList1:  # 当关键字只能是唯一的时候
                segmentDicList[key] = result[0]
                # print result.group(1)
            else:  # 当关键字应该出现2次的情况
                if len(result) == 2:
                    # print result
                    segmentDicList[key] = timeshift(result[0], result[1])
                elif len(result) > 2:  # 如果出现多于2次的数据，取前两次
                    print result
                    segmentDicList[key] = timeshift(result[0], result[1])
                else:
                    segmentDicList[key] = " "
                    # segmentDicList[key] = result[0]
        segmentList.append([segmentDicList[key] for key in patternList])
    return segmentList


if __name__ == '__main__':
    line_list = text2list(log_file)
    # line_list = segmentLog(log_file)
    # print line_list
    for i in line_list:
        print i
        print "____________"
        writer.writerow(i)
    csvfile.close()
