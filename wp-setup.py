#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import re
import shutil
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
    path = getParam("init", "path")

    getWP(version, path)

def getParam(section, param_name):
    parser = SafeConfigParser()
    parser.read(configfile)
    return parser.get(section, param_name)

def getWP(ver, path):
    url = "https://ja.wordpress.org/"

    regex = r'\d\.\d+.\d+'
    if re.match(regex, ver):
        filename = "wordpress-" + ver + "-ja.tar.gz"
    else :
        filename = "latest-ja.tar.gz"

    print tmpdir + filename

    # download wordpress and untar
    urllib.urlretrieve(url + filename, tmpdir + filename)
    untar(tmpdir + filename)

    # copy to setup directory
    if(not os.path.isdir(path)):
        print path + " is not directory."
        sys.exit(1)

    if(not path.endswith("/")):
        path = path + "/"

    srcdir = tmpdir + "wordpress/"
    files = os.listdir(srcdir)
    for fname in files:
        shutil.copy(srcdir + fname, path)

    #os.remove(tmpdir + filename)

def untar(fname):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall(tmpdir)
        tar.close()
    else:
        print "Not a tar.gz file: " + fname

if __name__ == '__main__':
    main()