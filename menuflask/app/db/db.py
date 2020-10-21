#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from flask import g

import sqlite3

db_name = "static/test.db"


def connect_db():

    print 'dbpath',os.path.abspath(db_name)
    return sqlite3.connect(db_name)


def get_dbconn():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def close_db():
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

if __name__ == '__main__':
    print os.path.abspath("test.db")

    conn  = sqlite3.connect("../static/"+db_name)
    dbcursor = conn.cursor()
    dbcursor.execute("select * from menudetail")

    rows = dbcursor.fetchall()

    for row in rows:
        print(row)

    dbcursor.close()
    conn.commit()
    conn.close()
