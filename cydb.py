#!/usr/bin/python
# -*- coding: utf-8 -*-


import win32com.client


class db:
    conn = None
    dsn = None

    def __init__(self, db_name):
        self.conn = win32com.client.Dispatch(r'ADODB.Connection')
        self.dsn = r'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=db/' + db_name + '.mdb;'
        self.conn.Open(self.dsn)

    def dml(self, sql):
        self.conn.Execute(sql)

    def query(self, sql):
        rs = win32com.client.Dispatch(r'ADODB.Recordset')
        rs.Open(sql, self.conn, 1, 3)  # 1和3是常数.代表adOpenKeyset 和adLockOptimist

        if rs.EOF:
            return None

        cys = []
        rs.MoveFirst()

        while not rs.EOF:
            items = {}
            for x in range(rs.Fields.Count):
                items[x] = rs.Fields.Item(x).Value
            cys.append(items)
            rs.MoveNext()
        return cys

    def queryUnique(self, sql):
        cys = self.query(sql)
        if cys is not None and len(cys) > 0:
            return cys[0]
        else:
            return None

    def close(self):
        self.conn.Close()
