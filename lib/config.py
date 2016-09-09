#!/usr/bin/python
from ConfigParser import ConfigParser
 
def read_config(filename='config.ini', section='general'):
    parser = ConfigParser()
    parser.read(filename)
 
    data = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return data