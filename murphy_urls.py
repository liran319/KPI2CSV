# -*- coding: utf-8 -*-

import os
import urllib2

url_file = r"C:\Users\li_ran\Desktop\urls.txt"
new_file = os.path.splitext(url_file)[0] + "_new.txt"


class UrlsHandler(object):

    """docstring for UrlsHandler"""

    def __init__(self, arg):
        self.arg = arg
        
    def verify_urls(self):
        file_open = open(self.arg, "r")
        file_writer = open(new_file, "w")
        content = file_open.read().split()
        print file_open.readlines()
        new_contentList = []
        for line in content:
            try:
                response = urllib2.urlopen(line)
                if int(response.getcode()) == 200:
                    new_contentList.append(line)
                else:
                    new_contentList.append("#" + line)
            except Exception as e:
                new_contentList.append("# " + line)
                print "ErrorInfo: ", e
        new_content = '\r\n'.join(new_contentList)
        # for i in new_contentList:
        file_writer.writelines(new_content)
        file_open.close()
        file_writer.close()

demo = UrlsHandler(url_file)

demo.verify_urls()
