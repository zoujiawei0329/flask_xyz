#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from json import JSONEncoder

import flask


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class ResData:

    def __init__(self, data={}, code=200000, message="message"):
        self.data = data
        self.code = code
        self.message = message

    def __dict__(self):
        dict(data=self.data, code=self.code, message=self.message)

    def toJson(self):
        return MyEncoder().encode(self)

    def toJsonRES(self):
        resp = flask.Response(self.toJson())
        resp.headers['content-type'] = 'application/json; charset=utf-8'
        return resp


def errorRes(code, message):
    res = ResData({}, code=code, message=message)
    return res.toJsonRES()
