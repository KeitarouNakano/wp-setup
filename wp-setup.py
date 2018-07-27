#!/usr/bin/python
#-*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser

configfile = 'config.ini'

def main():
    print getParam("user")
    print getParam("password")
    print getParam("host")

def getParam(param_name):
    parser = SafeConfigParser()
    parser.read('mysql', configfile)
    return parser.get(param_name)

if __name__ == '__main__':
    main()