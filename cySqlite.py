#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3


class sqlitedb:
    conn = None
    cu = None

    def __init__(self, db_name):
        self.conn = sqlite3.connect(r'db/' + db_name + '.db')
        self.cu = self.conn.cursor()

    def dml(self, sql):
        try:
            self.cu.execute(sql)
            self.conn.commit()
        except Exception, e:
            print e
            self.conn.rollback()

    def query(self, sql):
        self.cu.execute(sql)
        cys = self.cu.fetchall()
        return cys if cys is not None else []

    def queryUnique(self, sql):
        cys = self.query(sql)
        if cys is not None and len(cys) > 0:
            return cys[0]
        else:
            return None

    def close(self):
        self.conn.close()
