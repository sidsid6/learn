#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    Created on Thu Feb 22 18:42:38 2018

    @author: Taewoo
"""

import time
# import math
import requests
import json
from collections import OrderedDict
import numpy as np
import pandas as pd

#url = "http://125.140.110.217:44242/api/query"
new_url = "http://125.140.110.217:44242/api/put"


query_parameter = {
    "start": "2014-06-01 00:00:00",
    "end": "2014-06-07 23:59:59",
    "aggregator": "none",
    "metric": "HanuriTN_00"}

query_tags = {
    "content": "spd",
    "carid": "*"}


# metric = "__test__HanuriTN_existData"
metric = "DIST_TEST"
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

    return response


def makeData(_qdata):
    decode_data = json.loads(_qdata.content)

    data = np.zeros((t_length, 603), dtype=int)

    print "\n\nstart: %s" % (convertTimeToEpoch(query_parameter["start"]))
    print "end: %s" % convertTimeToEpoch(query_parameter["end"])
    print "t_length: %s" % (t_length)
    print "column shape: %s" % str(column.shape)
    print "index shape: %s\n" % str(index.shape)

    for i in xrange(len(decode_data)):
        carid = decode_data[i]["tags"]["carid"]

        for t in xrange(t_length):

            if str(t + convertTimeToEpoch(query_parameter["start"])) in decode_data[i]["dps"]:
                # data[t][int(carid)-1] = decode_data[i]["dps"][str(t + convertTimeToEpoch(query_parameter["start"]))]
                data[t][int(carid) - 1] = 1

        if i % 10 == 0:
            print "makeData: %s / %s finished" % (i, len(decode_data))

    print "makeData finish!\n\n"
    return data


def putRequest(_buffer):
    headers = {'content-type': 'application/json'}

    for i in xrange(0, len(_buffer), 50):

        # print json.dumps(_buffer[i:i+50], ensure_ascii=False, indent=4)
        response = requests.post(new_url, data=json.dumps(_buffer[i:i + 50]), headers=headers)

        while response.status_code > 204:
            response = requests.post(new_url, data=json.dumps(_buffer[i:i + 50]), headers=headers)
            print "error!"
            print response

        if i % 1000 == 0:
            print "\tputData: %s / %s finished" % (i + 1, len(_buffer))


def putDataHttpPost(_dframe):
    buf = []
    t_length = convertTimeToEpoch(query_parameter["end"]) - convertTimeToEpoch(query_parameter["start"]) + 1
    column = np.array(range(1, 603 + 1)).astype('str')
    index = (np.array(range(t_length)) + convertTimeToEpoch(query_parameter["start"])).astype('str')

    for col in xrange(len(column)):

        for ix in xrange(len(index)):
            dp = OrderedDict()  # dp (Data Point)

            select = [column[col], index[ix]]
            # print select

            dp["metric"] = metric
            dp["timestamp"] = int(index[ix])
            dp["value"] = int(_dframe[select[0]][select[1]])
            # print dp["value"]

            dp["tags"] = OrderedDict()
            dp["tags"]["content"] = "exist"
            dp["tags"]["carid"] = column[col]

            buf.append(dp)

        if col % 10 == 0:
            print "jsonData: %s / %s finished" % (col, len(column))

        if len(buf) >= MAX_BUFFER:
            putRequest(buf)
            buf = []

    # print "jsonData finish!\n\n"

    putRequest(buf)
    print "\n\nfinish!\n\n"


if __name__ == "__main__":
    # httpPostQueryData(url, query_parameter, query_tags)
    start_time = time.time()

    queryData = httpPostQueryData(url, query_parameter, query_tags)

    run_time = time.time() - start_time

    print "\n\nQuery time: %s ~ %s" % (query_parameter["start"], query_parameter["end"])
    print "Query status: %s\nRun time: %.4f (sec)" % (queryData.status_code, run_time)

    data = makeData(queryData)

    dataframe = pd.DataFrame(data=data, columns=column, index=index)
    putDataHttpPost(dataframe)
