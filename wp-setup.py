#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import re
import urllib
import tarfile
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
    url = "https://ja.wordpress.org/"

    regex = r'\d\.\d+.\d+'

    if re.match(regex, ver):
        filename = "wordpress-" + ver + "-ja.tar.gz"
    else :
        filename = "latest-ja.tar.gz"

    print tmpdir + filename

    urllib.urlretrieve(url + filename, tmpdir + filename)

    untar(tmpdir + filename)

def untar(fname):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall()
        tar.close()
        print "Extracted in Current Directory"
    else:
        print "Not a tar.gz file: " + fname

if __name__ == '__main__':
    main()