# -*- coding:utf-8 -*-

import re
import os
import csv
import sys
import datetime
# log_file = sys.argv[1]
log_file = r"D:\volog.log"
csv_content = []
# new_csv = sys.argv[2]
new_csv = r"result.csv"
csv_name = os.path.splitext(log_file)[0] + ".csv"
csvfile = file(csv_name, 'wb')
writer = csv.writer(csvfile)

"""
14:31:33.078 @@@VOLOG,   Info, 0B010000, 0000303C, COSMPEngnWrap.cpp, COSMPEngnWrap::Open, 468, [Open] @ 103528277

14:31:21.823 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 138, VR IsHandshakeVerified+
14:31:21.823 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 140, VR IsHandshakeVerified- 0
14:31:21.823 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 195, VR InitializeSSL+
14:31:21.825 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 197, VR InitializeSSL- 0
14:31:22.853 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 211, VR VerifyHandshake+
14:31:23.914 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 213, VR VerifyHandshake- 0
14:31:23.914 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 255, VR GetVersion+
14:31:23.914 @@@VOLOG,   Info, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 257, VR GetVersion- Verimatrix-ViewRight-Web-3.6.0.0-ItrH-1-web_pc-win32
14:31:23.914 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 259, VR SetLogging+
14:31:23.914 @@@VOLOG,    Run, 0A030000, 0000303C, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::VerifyVR, 261, VR SetLogging-

14:31:48.077 @@@VOLOG,   Info, 0B010000, 000021D4, COSMPEngnWrap.cpp, COSMPEngnWrap::OSMPCommonHandleEvent, 2399, [Video] gonna to be rendered @ 103543276
"""


pattern_Open = ".*[Open] @ (\d*)"
pattern_Video = ".*[Video] @ (\d*)"
pattern_IsHandshakeVerified = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR IsHandshakeVerified"
pattern_SetLogging = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR SetLogging"
pattern_SetVCASCommunicationHandlerSettings = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR SetVCASCommunicationHandlerSettings"
pattern_CheckVCASConnection = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR CheckVCASConnection"
pattern_Decrypt = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR Decrypt+"
pattern_IsDeviceProvisioned = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR IsDeviceProvisioned"
pattern_ConnectAndProvisionDevice = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR ConnectAndProvisionDevice"


patternDic = {
    "Open": pattern_Open,
    "Video": pattern_Video,
    "IsHandshakeVerified": pattern_IsHandshakeVerified,
    "SetLogging": pattern_SetLogging,
    "SetVCASCommunicationHandlerSettings":
    pattern_SetVCASCommunicationHandlerSettings,
    "CheckVCASConnection": pattern_CheckVCASConnection,
    "IsDeviceProvisioned": pattern_IsDeviceProvisioned,
    "ConnectAndProvisionDevice": pattern_ConnectAndProvisionDevice,
    "Decrypt": pattern_Decrypt,
}

patternList1 = ["Open", "Video"]

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
    segment_start = r"[Open]"
    # segment_stop = "[Video]"
    tempList = []  # counter for readline
    content = []
    new_content = []

    while flag1:
        line = f.readline()
        tempList.append(line)
        if re.search(pattern_Video, line):  # keyword is in that line
            temp = ''.join(tempList)
            content.append(temp)
            tempList = []
        else:
            pass
        if not line:
            flag1 = 0
            break

    for each_segment in content:
        for each_line in each_segment.splitlines():
            if each_line.find(segment_start) >= 0:
                new_segment = each_segment[each_segment.index(each_line) - 1:]
                new_content.append(new_segment)
    return new_content
    # return content


def text2list(logfile):
    """translate text segment to new dictionary: {"Stop":xx, "Close":yy..}"""
    #content = open("1.txt", "rb").read()
    content = segmentLog(logfile)
    segmentDicList = {}
    segmentList = []
    for segment in content:
        # print segment
        # print '*' * 20
        for key, vaule in patternDic.items():
            result = re.findall(vaule, str(segment))
            print result
            if key in patternList1:  # 当关键字只能是唯一的时候
                # 如果搜寻不到，打印错误并且设置输出值为空
                try:
                    segmentDicList[key] = result[0]
                except Exception as e:
                    print "ErrorInfo: ", e
                    segmentDicList[key] = " "
            else:  # 当关键字应该出现2次的情况
                if len(result) >= 2:
                    segmentDicList[key] = timeshift(result[0], result[1])
                # elif len(result) > 2:  # 如果出现多于2次的数据，取前两次
                #     # print result
                #     segmentDicList[key] = timeshift(result[0], result[1])
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
