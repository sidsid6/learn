#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import requests
import HTTP_POST_request
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import json

""" 단기간을 기준으로 기능 테스트 위한 query parameter"""

""" 실제 작업에 필요한 query parameter """
spd = {
    "start" : "2014-06-02 09:00:00",
    "end": "2014-06-02 10:00:00",
    "aggregator" : "none",
    "metric" : "HanuriTN_00"
}

url = "http://서버주소:포트번호/api/query"


""" 쿼리 하려는 tag """
spd_query_tags = {
    "content": "spd|rpm",
    "carid" : "283"
}


def convertTimeToEpoch(_time):
    date_time = "%s.%s.%s %s:%s:%s" %(_time[8:10], _time[5:7], _time[:4], _time[-8:-6], _time[-5:-3], _time[-2:])
    #print date_time
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int (time.mktime(time.strptime(date_time, pattern)))
    return epoch


def convertEpochToTime(_time):

    T = time.strftime("%H:%M:%S", time.gmtime(float(_time)))
    return T


''' OpenTSDB에 HTTP POST방식으로 쿼리하는 함수 '''
def QueryData(_url, _required, _tags):
    headers = {'content-type': 'application/json'}

    dp = OrderedDict()    # dp (Data Point)
    dp["start"] = convertTimeToEpoch(_required["start"])
    dp["end"] = convertTimeToEpoch(_required["end"])    # not exactly required

    temp = OrderedDict()
    temp["aggregator"] = _required["aggregator"]
    temp["metric"] = _required["metric"]
    temp["tags"] = _tags

    dp["queries"] = []
    dp["queries"].append(temp)
    print 'dp'
    print " [Querying]" + json.dumps(dp, ensure_ascii=False, indent=4)
    response = requests.post(_url, data=json.dumps(dp), headers= headers)

    while response.status_code > 204:
        print " [Bad Request] Query status: %s" % (response.status_code)
        print " [Bad Request] We got bad request, Query will be restarted after 3 sec!\n"
        time.sleep(3)

        print " [Querying]" + json.dumps(dp, ensure_ascii=False, indent=4)
        response = requests.post(_url, data=json.dumps(dp), headers= headers)

    print " [Query finish and out]"
    return response

def getkeyvalue(_url, _parameter, _tags):

    queryData = QueryData(_url, _parameter, _tags)
    d = json.loads(queryData.content.decode())

    _spd = []
    _rpm = []
    _time= []

    for k,v in sorted(d[0]['dps'].items()):
        _spd.append(v)
        _time.append(convertEpochToTime(k))

    for k,v in sorted(d[1]['dps'].items()):
        _rpm.append(v)

    return [_spd, _rpm, _time]


if __name__ == "__main__":

    #time 함수는 컴퓨터의 현재 시각을 구하는 함수.

    _spd= getkeyvalue(url, spd, spd_query_tags)  # 3549개
    plt.plot(_spd[0])
    plt.xlabel("Time" + spd["start"] +"  To  "+spd["end"])
    plt.xticks(rotation=90)
    plt.ylabel("spd (KM)")
    plt.title("Car283 Spd Variation")
    plt.show()

    print "\n\n [Main] Query time: %s ~ %s" % (spd["start"], spd["end"])
