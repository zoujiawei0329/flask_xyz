#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import Flask, url_for
from flask import request
import json

from entity.menu_detail import ResData, errorRes
from db import db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello !'


def getSteps(id):
    with db.get_dbconn() as conn:
        cur = conn.cursor()
        cur.execute("select * from menusteps where menudetailId = %s" % str(id))
        res = [dict(id=row[0], step=row[2], detail=row[3]) for row in cur.fetchall()]

    return res


def getThings(id):
    with db.get_dbconn() as conn:
        cur = conn.cursor()
        cur.execute("select * from menuthings where menudetailId = %s" % str(id))
        res = [dict(id=row[0], name=row[2], unit=row[3]) for row in cur.fetchall()]

    return res


# def getThings(id):
#     with db.get_dbconn() as conn:
#         cur = conn.cursor()
#         cur.execute("select * from menuthings where menudetailId = %s" % str(id))
#         res = [dict(id=row[0], name=row[2], unit=row[3]) for row in cur.fetchall()]
#
#     return res


@app.route('/menu/list')
def menu_list():
    limit = int(request.args.get("limit", 20))
    cursor = int(request.args.get("cursor", 0))
    conn = db.get_dbconn()
    dbcursor = conn.cursor()
    resData = ResData()
    if limit != 0:
        sql = "select * from menudetail where id > %d limit %d" % (cursor, limit)
        dbcursor.execute(sql)
        rows = dbcursor.fetchall()
        resData.data = dict(
            items=[dict(id=row[0], name=row[1], url=row[2], title=row[3], imgurl=row[4], desc=row[5], steps=getSteps(row[0]), things=getThings(row[0])) for row in rows])
        resData.data["nextCursor"] = rows[-1][0]

    dbcursor.execute("select 1 from menudetail")
    resData.data["totalCount"] = dbcursor.fetchall().__len__()
    res = resData.toJsonRES()
    dbcursor.close()
    conn.commit()
    return res


@app.route('/menu/item')
def menu_detail():
    id = int(request.args.get("id"))
    with db.get_dbconn() as conn:
        cur = conn.cursor()
        cur.execute("select * from main.menudetail where id = %d" % id)
        row = cur.fetchall()[0]
        resData = ResData(data=dict(id=row[0], name=row[1], url=row[2], title=row[3], imgurl=row[4], desc=row[5],
                                    steps=getSteps(row[0]), things=getThings(row[0])))
    if resData != None:
        return resData.toJsonRES()
    else:
        return errorRes(10000, "错误")


@app.route('/menu/item/countnum/<int:index>')
def menu_countnum(index=0):
    with db.get_dbconn() as conn:
        cur = conn.cursor()
        rows = cur.execute("select *from menudetail limit %d,1" % index)
        row = cur.fetchone()
        resData = ResData(dict(id=row[0], name=row[1], url=row[2], title=row[3], imgurl=row[4], desc=row[5],
                               steps=getSteps(row[0]), things=getThings(row[0])))

    if resData is not None:
        return resData.toJsonRES()
    else:
        return errorRes(10000, "错误")


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(load_dotenv=False, host='0.0.0.0')
