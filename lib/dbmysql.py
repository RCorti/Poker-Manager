#!/usr/bin/python
from __future__ import print_function
import mysql.connector
from mysql.connector import Error, errorcode
 
class db: 
    def __init__(self, config):
        self.conn = None
        try:
            self.conn = mysql.connector.connect(**config)
            if not self.conn.is_connected():
                print('Could not connect to mysql.')
            
        except Error as e:
            print(e)
    
    def close(self):
        self.conn.commit()
        self.conn.close()

    def create(self, name, TABLES):
        print('\n')
        cursor = None
        try:
            cursor = self.conn.cursor()
            
            print("Creating database {}: ".format(name), end='')
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))

        except Error as e:
            if e.errno == errorcode.ER_DB_CREATE_EXISTS:
                print("already exists.")
            else:
                print(e.msg)
        else:
            print("OK")
        print('\n')
        
        self.conn.database = name
        for tables in list(TABLES):
            try:
                print("Creating table {}: ".format(tables[0]), end='')
                cursor.execute(tables[1])
            except Error as e:
                if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(e.msg)
            else:
                if len(tables) > 2:
                    query = tables[2]
                    if len(tables) > 3:
                        if len(tables[3]) > 1:
                            self.executemany(query, tables[3])
                        else:
                            self.execute(query, tables[3])
                    else:
                        self.execute(query)
                print("OK")
            
        if not (cursor is None):
            cursor.close()
    
    def execute(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        cursor.close()
        
    def executemany(self, query, params):
        cursor = self.conn.cursor()
        cursor.executemany(query, params)
        cursor.close()
        
    def query(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor

    def cursor(self):
        return self.conn.cursor()
        
    def commit(self):
        self.conn.commit()
        
        