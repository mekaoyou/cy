#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2
import urllib

reload(sys)
sys.setdefaultencoding('utf8')

url = "http://51pinyin.com/getdata.ashx?url=index"


def getSpell(words):
    data = {"name": words}
    res = urllib2.urlopen(url, urllib.urlencode(data))
    return res.read()


if __name__ == "__main__":
    print getSpell(r'测试')

