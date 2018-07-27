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
    parser.read(configfile)
    return parser.get('mysql', param_name)

if __name__ == '__main__':
    main()