#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import re
import urllib
from ConfigParser import SafeConfigParser

configfile = 'config.ini'
tmpdir = '/tmp/'

def main():
    print getParam("mysql", "user")
    print getParam("mysql", "password")
    print getParam("mysql", "host")
    print getParam("init", "version")
    print getParam("init", "path")

    version = getParam("init", "version")

    downloadWP(version)

def getParam(section, param_name):
    parser = SafeConfigParser()
    parser.read(configfile)
    return parser.get(section, param_name)

def downloadWP(ver):
    # https://ja.wordpress.org/latest-ja.tar.gz
    # https://ja.wordpress.org/wordpress-4.9.7-ja.tar.gz
    url = "https://ja.wordpress.org/"

    regex = r'\d\.\d+.\d+'
    print re.match(regex, ver)
    if re.match(regex, ver):
        filename = "wordpress-" + ver + "-ja.tar.gz"
    else :
        filename = "latest-ja.tar.gz"

    print tmpdir + filename

    urllib.urlretrieve(url + filename, tmpdir + filename)

if __name__ == '__main__':
    main()