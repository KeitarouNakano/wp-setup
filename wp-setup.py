#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import re
import pwd
import grp
import shutil
import urllib
import tarfile
from crypt import crypt
from ConfigParser import SafeConfigParser

configfile = 'config.ini'
tmpdir = '/tmp/'
salturl = 'https://api.wordpress.org/secret-key/1.1/salt/'
path = ''

def main():

    version = getParam("init", "version")
    path = getParam("init", "path")
    basic_auth = getParam("init", "basic_auth")

    params = {
        'dbname'  : getParam("mysql", "dbname"),
        'user'    : getParam("mysql", "user"),
        'host'    : getParam("mysql", "host"),
        'password': getParam("mysql", "password")
    }

    if(not path.endswith("/")):
        path = path + "/"
    print "wordpress install to " + path

    getWP(version, path)

    salt = getSalt()
    replaceWPConfig(path, params, salt)

    setHtaccess(path, basic_auth)

    setPermission(path)

def getParam(section, param_name):
    parser = SafeConfigParser()
    parser.read(configfile)
    return parser.get(section, param_name)

def setHtaccess(path):
    f_output = open(path + '.htaccess', 'a')

    f_output.write('# BEGIN WordPress')
    f_output.write('<IfModule mod_rewrite.c>')
    f_output.write('RewriteEngine On')
    f_output.write('RewriteBase /')
    f_output.write('RewriteRule ^index\.php$ - [L]')
    f_output.write('RewriteCond %{REQUEST_FILENAME} !-f')
    f_output.write('RewriteCond %{REQUEST_FILENAME} !-d')
    f_output.write('RewriteRule . /index.php [L]')
    f_output.write('</IfModule>')
    f_output.write('# END WordPress')

    f_output.close()

def setPermission(path):
    print "set owner and group"

    uid = pwd.getpwnam(getParam("init", "user")).pw_uid
    gid = grp.getgrnam(getParam("init", "group")).gr_gid

    files = os.listdir(path)
    for file in files:
        os.chown(path + file, uid, gid)

    os.chmod(path + "wp-content/", 0777)
    os.chmod(path + "wp-content/plugins/", 0777)
    os.chmod(path + "wp-content/themes/", 0777)

def replaceWPConfig(path, params, salt):

    print "set wordpress config data"
    f_input = open(path + 'wp-config-sample.php')
    f_output = open(path + 'wp-config.php', 'w')

    for line in f_input:
        if re.match(r"define\('DB_NAME", line):
            line = "define('DB_NAME', '" + params["dbname"] + "');" + '\n'
        elif re.match(r"define\('DB_USER", line):
            line = "define('DB_USER', '" + params["user"] + "');" + '\n'
        elif re.match(r"define\('DB_PASSWORD", line):
            line = "define('DB_PASSWORD', '" + params["password"] + "');" + '\n'
        elif re.match(r"define\('DB_HOST", line):
            line = "define('DB_HOST', '" + params["host"] + "');" + '\n'
        elif re.match(r"define\('AUTH_KEY'", line):
            line = salt[0] + '\n'
        elif re.match(r"define\('SECURE_AUTH_KEY'", line):
            line = salt[1] + '\n'
        elif re.match(r"define\('LOGGED_IN_KEY'", line):
            line = salt[2] + '\n'
        elif re.match(r"define\('NONCE_KEY'", line):
            line = salt[3] + '\n'
        elif re.match(r"define\('AUTH_SALT'", line):
            line = salt[4] + '\n'
        elif re.match(r"define\('SECURE_AUTH_SALT'", line):
            line = salt[5] + '\n'
        elif re.match(r"define\('LOGGED_IN_SALT'", line):
            line = salt[6] + '\n'
        elif re.match(r"define\('NONCE_SALT'", line):
            line = salt[7] + '\n'

        f_output.write(line)

    f_input.close()
    f_output.close()

def getSalt():
    salt = urllib.urlopen(salturl).read().split("\n")
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
        print "move from " + srcdir + fname + " to " + path
        shutil.move(srcdir + fname, path)

    print "delete tmp file " + tmpdir + filename
    os.remove(tmpdir + filename)

    print "delete tmp dir " + tmpdir + "wordpress/"
    os.removedirs(tmpdir + "wordpress/")

def untar(fname):
    if (fname.endswith("tar.gz")):
        print "untar " + fname
        tar = tarfile.open(fname)
        tar.extractall(tmpdir)
        tar.close()
    else:
        print "Not a tar.gz file: " + fname

if __name__ == '__main__':
    main()