#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Thu Feb 22 18:42:38 2018

    @author: Seung Il
"""

import time
# import math
import requests
import json
from collections import OrderedDict
import numpy as np
import pandas as pd


url = "http://125.140.110.217:54242/api/query"
new_url = "http://125.140.110.217:54242/api/put"

query_parameter = {
    "start": "2014-06-01 00:00:00",
    "end": "2014-06-01 00:01:00",
    "aggregator": "none",
    "metric": "TestData_Oneday_HanuriTN"}

query_tags = {
    "content": "spd",
    "carid": "*"}

# metric = "__test__HanuriTN_existData"
metric = "DIST_TEST00"
tagnames = ["content", "carid"]
MAX_BUFFER = 1000000


def convertTimeToEpoch(_time):

    date_time = "%s.%s.%s %s:%s:%s" % (_time[8:10], _time[5:7], _time[:4], _time[-8:-6], _time[-5:-3], _time[-2:])
    # print date_time
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(date_time, pattern)))
    return epoch


def httpPostQueryData(_url, _required, _tags):

    headers = {'content-type': 'application/json'}

    dp = OrderedDict()  # dp (Data Point)
    dp["start"] = convertTimeToEpoch(_required["start"])
    dp["end"] = convertTimeToEpoch(_required["end"])  # not exactly required

    temp = OrderedDict()
    temp["aggregator"] = _required["aggregator"]
    temp["metric"] = _required["metric"]
    temp["tags"] = _tags

    dp["queries"] = []
    dp["queries"].append(temp)

    print json.dumps(dp, ensure_ascii=False, indent=4)
    response = requests.post(url, data=json.dumps(dp), headers=headers)
    # print json.loads(response.content[1])
    return response


def putRequest(_session, _buffer):
    headers = {'content-type': 'application/json'}
    for i in range(0, len(_buffer)):

        # print json.dumps(_buffer[i:i+50], ensure_ascii=False, indent=4)
        response = _session.post(new_url, data=json.dumps(_buffer[i:i + 10]), headers=headers)

        while response.status_code > 204:
            response = _session.post(new_url, data=json.dumps(_buffer[i:i + 10]), headers=headers)
            print "error!"
            print response

        if i % 10 == 0:
            print "\tputData: %s / %s finished" % (i + 1, len(_buffer))


def makeData(_qdata):

    d=[]
    decode_data = json.loads(_qdata.content)
    for i in range(len(decode_data)):
        if decode_data[i]['dps']=={}:
            pass
        else:
            a = []
            b = []
            c = []
            for k,v in decode_data[i]['dps'].items():

                a.append(k)
                b.append(v)
                c.append(decode_data[i]['tags']['carid'])

            d.append([a,b,c])
    return d


def putDataHttpPost(_session, _data):

    buf = []

    for i in xrange(len(_data)):
        for j in xrange(len(_data[i][1])):
            dp = OrderedDict()  # dp (Data Point)

            dp["metric"] = metric
            dp["timestamp"] = _data[i][0][j]
            dp["value"] = _data[i][1][j]

            dp["tags"] = OrderedDict()
            dp["tags"]["content"] = "spd"
            dp["tags"]["carid"] = _data[i][2][j]

            buf.append(dp)

            if len(buf) >= MAX_BUFFER:
                putRequest(_session, buf)
                buf = []

        if i % 10 == 0:
            print "jsonData: %s / %s finished" % (i, len(_data))
        if i==len(_data):
            print "jsonData: %s / %s finished" % (i, len(_data))
    putRequest(_session, buf)

    # print "jsonData finish!\n\n"
    print "\n\nfinish!\n\n"


if __name__ == "__main__":

    # httpPostQueryData(url, query_parameter, query_tags)
    start_time = time.time()

    queryData = httpPostQueryData(url, query_parameter, query_tags)
    run_time = time.time() - start_time

    print "\n\nQuery time: %s ~ %s" % (query_parameter["start"], query_parameter["end"])
    print "Query status: %s\nRun time: %.4f (sec)" % (queryData.status_code, run_time)

    data = makeData(queryData)

    #t_length = convertTimeToEpoch(query_parameter["end"]) - convertTimeToEpoch(query_parameter["start"]) + 1
    #column = np.array(range(1, 605 + 1)).astype('str')
    #index = (np.array(range(t_length)) + convertTimeToEpoch(query_parameter["start"])).astype('str')

    s = requests.Session()
    putDataHttpPost(s, data)
