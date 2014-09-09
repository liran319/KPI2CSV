#!/usr/bin/python
# -*- coding:utf-8 -*-

import re
import os
import csv
import sys
import datetime

urlsPath = sys.argv[1]
csv_content = []
new_csv = urlsPath + '\\' + r"result.csv"
csvfile = file(new_csv, 'wb')


"""
15:51:59.768 @@@VOLOG,   Info, 0B010000, 00002364, cosmpengnwrap.cpp, COSMPEngnWrap::Open, 459, [Open] @ 22514603
15:52:10.392 @@@VOLOG,   Info, 0B010000, 00002FC0, cosmpengnwrap.cpp, COSMPEngnWrap::OSMPCommonHandleEvent, 2377, [Audio] gonna to be rendered @ 22525228
15:52:07.140 @@@VOLOG,    Run, 0A030000, 00000F60, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::OnSourceDrm, 802, VR Decrypt+ 223168
15:52:10.229 @@@VOLOG,    Run, 0A030000, 00000F60, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::OnSourceDrm, 804, VR Decrypt- 0 223168
15:52:10.558 @@@VOLOG,    Run, 0A030000, 00000F60, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::OnSourceDrm, 802, VR Decrypt+ 248928
15:52:10.702 @@@VOLOG,    Run, 0A030000, 00000F60, DRM_Verimatrix_AES128_Other.cpp, CDRM_Verimatrix_AES128::OnSourceDrm, 804, VR Decrypt- 0 248928

15:52:10.397 @@@VOLOG,   Info, 0B010000, 000024F4, cosmpengnwrap.cpp, COSMPEngnWrap::OSMPCommonHandleEvent, 2372, [Video] gonna to be rendered @ 22525233
"""


pattern_Open = "\d{2}:\d{2}:\d{2}\.\d{3} @@@VOLOG.*\[Open\]( call open)? @ (\d*)"
pattern_Video = "\d{2}:\d{2}:\d{2}\.\d{3} @@@VOLOG.*\[Video\]( gonna to be rendered)? @ (\d*)"
pattern_Decrypt = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR Decrypt"

patternDic = {
    "Open": pattern_Open,
    "Video": pattern_Video,
    "Decrypt": pattern_Decrypt,
}

patternList1 = ["Open", "Video"]
patternList2 = ["Decrypt"]
patternList3 = ["Open2Video"]

patternList = patternList1 + patternList2 + patternList3


def timeshift(inputtime, outputtime):
    time1 = datetime.datetime.strptime(inputtime, '%H:%M:%S.%f')
    time2 = datetime.datetime.strptime(outputtime, '%H:%M:%S.%f')
    delta = time2 - time1
    timeshift1 = delta.microseconds / 1000 + delta.seconds * 1000
    return timeshift1


def text2list(logfile):
    """translate text segment to new dictionary: {"Stop":xx, "Close":yy..}"""
    content = open(logfile).read()
    segmentDicList = {}
    segmentList = []
    for key, vaule in patternDic.items():
        result = re.findall(vaule, content)
        if key in patternList1:  # 当关键字只能是唯一的时候
            # 如果搜寻不到，打印错误并且设置输出值为空
            try:
                segmentDicList[key] = int(result[0][-1])
            except Exception as e:
                print key
                print "ErrorInfo: ", e
                segmentDicList[key] = "NA"
        else:  # 当关键字应该出现2次的情况
            if len(result) >= 2:
                segmentDicList[key] = timeshift(result[0], result[1])
            else:
                segmentDicList[key] = "NA"
    segmentList = [segmentDicList[key] for key in patternList[:3]]
    # if "NA" not in segmentList[0]:
    if segmentList[0] != 'NA' and segmentList[1] != 'NA':
        if len(segmentList) == 3:  # 如果成功取到三个元素，则可以进行运算计算出花费时间
            print "准备计算时间差"
            print segmentList
            cost = segmentList[1] - segmentList[0]
            segmentList.append(cost)
        else:
            pass
    else:
        print str(logfile) + " 数据缺失:("
    return segmentList


def main():
    file_list = os.listdir(urlsPath)
    dataList = []
    for each_file in file_list:
        if each_file.endswith(".log"):
            filespath = os.path.join(urlsPath, each_file).replace("\\", "/")
            dataList.append(text2list(filespath))
        else:
            pass
    return dataList


if __name__ == '__main__':
    writer = csv.writer(csvfile)
    writer.writerow(patternList)
    line_list = main()
    print line_list
    # line_list = segmentLog(log_file)
    for i in line_list:
        print i
        print "____________"
        writer.writerow(i)
    csvfile.close()
