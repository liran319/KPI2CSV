#/usr/bin/python
# -*- coding:utf-8 -*-

import re
import os
import csv
import sys
import datetime

log_file = sys.argv[1]
# log_file = r"C:\Users\li_ran\Desktop\Decrypt2.log"
csv_content = []
csv_name = os.path.splitext(log_file)[0] + ".csv"
csvfile = file(csv_name, 'wb')
writer = csv.writer(csvfile)

"""
10:09:34.191 @@@VOLOG,    Run, 0A030000, 06355000, DRM_Verimatrix_AES128_iOS.mm, OnSourceDrm, 569, VR Decrypt+
10:09:37.996 @@@VOLOG,    Run, 0A030000, 06355000, DRM_Verimatrix_AES128_iOS.mm, OnSourceDrm, 571, VR Decrypt- 0
10:09:38.052 @@@VOLOG,    Run, 0A030000, 06355000, DRM_Verimatrix_AES128_iOS.mm, OnSourceDrm, 569, VR Decrypt+
10:09:38.106 @@@VOLOG,    Run, 0A030000, 06355000, DRM_Verimatrix_AES128_iOS.mm, OnSourceDrm, 571, VR Decrypt- 0
10:09:38.585 @@@VOLOG,    Run, 0A030000, 06355000, DRM_Verimatrix_AES128_iOS.mm, OnSourceDrm, 569, VR Decrypt+
10:09:38.679 @@@VOLOG,    Run, 0A030000, 06355000, DRM_Verimatrix_AES128_iOS.mm, OnSourceDrm, 571, VR Decrypt- 0
10:09:38.909 @@@VOLOG,    Run, 0A030000, 06355000, DRM_Verimatrix_AES128_iOS.mm, OnSourceDrm, 569, VR Decrypt+
10:09:38.961 @@@VOLOG,    Run, 0A030000, 06355000, DRM_Verimatrix_AES128_iOS.mm, OnSourceDrm, 571, VR Decrypt- 0
"""

# pattern_Decrypt_in = "(\d*:\d*:\d*.\d{3}) @@@VOLOG,\D{7}, \d\w\d{6}, \d{8}, \D{3,30}\d{3}_iOS\.mm, \w{11}, \d{3}, VR Decrypt\+"
pattern_Decrypt_in = "(\d*:\d*:\d*.\d{3})\s@@@VOLOG,\D{7},\s\d\w\d{6},\s\d{8},\s\D{3,30}\d{3}_iOS\.mm,\s\w{11},\s\d{3},\sVR Decrypt\+"
pattern_Decrypt_out = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR Decrypt- 0"

patternList = ["Decrypt+", "Decrypt-", "Decrype_time"]
writer.writerow(patternList)


def timeshift(inputtime, outputtime):
    time1 = datetime.datetime.strptime(inputtime, '%H:%M:%S.%f')
    time2 = datetime.datetime.strptime(outputtime, '%H:%M:%S.%f')
    delta = time2 - time1
    timeshift1 = delta.microseconds / 1000 + delta.seconds * 1000
    return timeshift1


def text2list(logfile):
    """translate text segment to new dictionary: {"Stop":xx, "Close":yy..}"""
    file_content = open(logfile, "r")
    content = file_content.read()
    DecryptInList = re.findall(pattern_Decrypt_in, content)  # 先匹配所有结果
    DecryptOutList = re.findall(pattern_Decrypt_out, content)
    print DecryptInList
    print DecryptOutList
    if len(DecryptInList) == len(DecryptOutList) and len(DecryptInList) > 0:
        DataList = zip(DecryptInList, DecryptOutList, map(timeshift, DecryptInList, DecryptOutList))
        print DataList
    elif abs(len(DecryptInList) - len(DecryptOutList)) == 1:
        shortList = min(len(DecryptInList), len(DecryptOutList))
        NewInList = DecryptInList[:shortList]
        NewOutList = DecryptOutList[:shortList]
        print len(NewInList), len(NewOutList)
        DataList = zip(NewInList, NewOutList, map(timeshift, NewInList, NewOutList))
    else:
        print "数据不正常, 请再次检查文件!"
        DataList = ["ERROR"]
    file_content.close()
    return DataList


if __name__ == '__main__':
    line_list = text2list(log_file)
    for i in line_list:
        print i
        print "____________"
        writer.writerow(i)
    csvfile.close()
