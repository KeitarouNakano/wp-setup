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
salturl = 'https://api.wordpress.org/secret-key/1.1/salt/'
path = ''

def main():
    print getParam("mysql", "user")
    print getParam("mysql", "password")
    print getParam("mysql", "host")
    print getParam("init", "version")

    version = getParam("init", "version")
    path = getParam("init", "path")

    params = {\
        'user': getParam("mysql", "user"), \
        'host': getParam("mysql", "host"), \
        'password': getParam("mysql", "password")
    }

    if(not path.endswith("/")):
        path = path + "/"
    print path

    #getWP(version, path)

    salt = getSalt()
    salt[0]
    print salt
    #replaceWPData(params, salt)


def getParam(section, param_name):
    parser = SafeConfigParser()
    parser.read(configfile)
    return parser.get(section, param_name)

def replaceWPData(params, salt):

    f_input = open(path + 'wp-config-sample.php')
    f_output = open(path + 'wp-config.php', 'w')

    for line in f_input:
        f_output.write(line)

    f_input.close()
    f_output.close()

def getSalt():
    salt = urllib.urlopen(salturl).read().split()

    return salt

def getWP(ver, path):

    if(not os.path.isdir(path)):
        print path + " is not directory or no such directory."
        sys.exit(1)

    url = "https://ja.wordpress.org/"

    regex = r'\d\.\d+.\d+'
    if re.match(regex, ver):
        filename = "wordpress-" + ver + "-ja.tar.gz"
    else :
        filename = "latest-ja.tar.gz"

    print tmpdir + filename

    # download wordpress and untar
    print "downloading... " + url + filename
    urllib.urlretrieve(url + filename, tmpdir + filename)
    untar(tmpdir + filename)
    print "done."

    # move to setup directory

    srcdir = tmpdir + "wordpress/"
    files = os.listdir(srcdir)
    for fname in files:
        print "copy from " + srcdir + fname + " to " + path
        shutil.move(srcdir + fname, path)

    print "delete tmp file. " + tmpdir + filename
    os.remove(tmpdir + filename)

    print "delete tmp dir. " + tmpdir + "wordpress/"
    os.removedirs(tmpdir + "wordpress/")

def untar(fname):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname)
        tar.extractall(tmpdir)
        tar.close()
    else:
        print "Not a tar.gz file: " + fname

if __name__ == '__main__':
    main()