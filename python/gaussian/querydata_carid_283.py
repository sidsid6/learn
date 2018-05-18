#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time
import datetime
import requests
import json
import copy
import sys
from multiprocessing import Pool, current_process
import HTTP_POST_request
import csv
from collections import OrderedDict

""" 단기간을 기준으로 기능 테스트 위한 query parameter"""

""" 실제 작업에 필요한 query parameter """
spd = {
    "start" : "2014-06-02 09:00:00",
    "end": "2014-06-02 10:00:00",
    "aggregator" : "none",
    "metric" : "HanuriTN_00"
}

sudden_stop = {
    "start" : "2014-06-02 09:00:00",
    "end": "2014-06-02 10:00:00",
    "aggregator" : "none",
    "metric" : "__fixtest.sudden-stop__"
}

rapid_accel = {
    "start" : "2014-06-02 09:00:00",
    "end": "2014-06-02 10:00:00",
    "aggregator" : "none",
    "metric" : "__fixtest.rapid-acceleration__"
}

fuel = {
    "start" : "2014-06-02 09:00:00",
    "end": "2014-06-02 10:00:00",
    "aggregator" : "none",
    "metric" : "__fixtest.inst-dlyf__"
}

url = "http://서버주소:/api/query"


""" 쿼리 하려는 tag """
spd_query_tags = {
    "content": "spd|rpm",
    "carid" : "283"
}

stop_query_tags = {
    "content": "sudden_stop",
    "carid" : "283"
}

accel_query_tags = {
    "content": "rapid_accel",
    "carid" : "283"
}

fuel_query_tags = {
    "content": "inst_dlyf",
    "carid" : "283"
}

def convertTimeToEpoch(_time):
    date_time = "%s.%s.%s %s:%s:%s" %(_time[8:10], _time[5:7], _time[:4], _time[-8:-6], _time[-5:-3], _time[-2:])
    #print date_time
    pattern = '%d.%m.%Y %H:%M:%S'
    epoch = int (time.mktime(time.strptime(date_time, pattern)))
    return epoch

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

def getkeyvalueH(_url, _parameter, _tags):

    queryData = QueryData(_url, _parameter, _tags)
    d = json.loads(queryData.content.decode())

    _spd = []
    _rpm = []

    for k,v in d[0]['dps'].items():
        _spd.append(v)
    for k,v in d[1]['dps'].items():
        _rpm.append(v)
    return [_spd, _rpm, queryData]


def getkeyvalue(_url, _parameter, _tags):
    queryData = QueryData(_url, _parameter, _tags)
    d = json.loads(queryData.content.decode())
    _value = []

    for k,v in d[0]['dps'].items():
        _value.append(v)
    print _value
    return [_value, queryData]

if __name__ == "__main__":

    #time 함수는 컴퓨터의 현재 시각을 구하는 함수.
    start_time = time.time()
    start_datetime = datetime.datetime.now()

    _spd= getkeyvalueH(url, spd, spd_query_tags)  # 3549
    _accel=getkeyvalue(url, rapid_accel, accel_query_tags) #3547
    _stop=getkeyvalue(url, sudden_stop,stop_query_tags) #3547
    _fuel=getkeyvalue(url, fuel, fuel_query_tags) #3547

    f=open('283car.csv', 'wb' )

    wr= csv.writer(f)
    wr.writerow(['spd','rpm' ,'accel', 'stop', 'fuel'])
    for i in range(0,len(_accel[0])):
        wr.writerow([_spd[0][i],_spd[1][i],_accel[0][i],_stop[0][i],_fuel[0][i]])
    f.close

    run_time = time.time() - start_time

    print "\n\n [Main] Query time: %s ~ %s" % (spd["start"], spd["end"])

#318번 차량
