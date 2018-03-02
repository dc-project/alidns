#!/usr/bin/env python3
# coding=utf-8

"""
@version:0.1
@author: ysicing
@file: alidns/core.py 
@time: 05/02/186 14:02
"""

import json

from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest, DescribeDomainRecordsRequest, DescribeSubDomainRecordsRequest\
    , DeleteDomainRecordRequest, UpdateDomainRecordRequest
from aliyunsdkcore import client


class DNS(object):

    def __init__(self, aliid, alikey):
        self.aliid = aliid
        self.alikey = alikey
        self.clt = client.AcsClient(self.aliid, self.alikey, 'cn-hangzhou')

    def _domain_prefix(self, domain):
        sub_domain = domain.split('.')[0]
        main_domain = ".".join(domain.split('.')[1:])
        pre_sub_domain = ".".join(domain.split('.')[:-2])
        pre_main_domain = ".".join(domain.split('.')[-2:])
        print(pre_main_domain, pre_sub_domain)
        return {'sub': pre_sub_domain, 'main': pre_main_domain}

    def check_rr(self, domain):
        ckd = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        ckd.set_accept_format('json')
        ckd.add_query_param('DomainName', self._domain_prefix(domain)['main'])
        ckd.add_query_param('RR', self._domain_prefix(domain)['sub'])
        rst_ckd = self.clt.do_action_with_exception(ckd)
        return rst_ckd

    def _check_domain(self, domain, types=None):
        chk = DescribeSubDomainRecordsRequest.DescribeSubDomainRecordsRequest()
        chk.set_accept_format('json')
        chk.add_query_param('SubDomain', domain)
        rst_chk = self.clt.do_action_with_exception(chk)
        if types:
            return json.loads(rst_chk)['DomainRecords']['Record'][0]['RecordId']
        return json.loads(rst_chk)['DomainRecords']['Record']

    def add_record(self, domain, types, ip):
        if not self._check_domain(domain=domain):
            add = AddDomainRecordRequest.AddDomainRecordRequest()
            add.set_accept_format('json')
            add.add_query_param('DomainName', self._domain_prefix(domain)['main'])
            add.add_query_param('RR', self._domain_prefix(domain)['sub'])
            add.add_query_param('Type', types)
            add.add_query_param('Value', ip)
            rst_add = self.clt.do_action_with_exception(add)
            return rst_add
        print(self._check_domain(domain=domain, types="add"))
        return "domain record [{}] isexist".format(self._domain_prefix(domain)['sub'])

    def del_record(self, domain):
        dels = DeleteDomainRecordRequest.DeleteDomainRecordRequest()
        dels.set_accept_format('json')
        dels.add_query_param('RecordId', self._check_domain(domain, types="deles"))
        rst_dels = self.clt.do_action_with_exception(dels)
        return rst_dels

    def update_record(self, domain, types, ip):
        if self._check_domain(domain=domain):
            update = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
            update.set_accept_format('json')
            update.add_query_param('RecordId', self._check_domain(domain, types='update'))
            update.add_query_param('RR', self._domain_prefix(domain)['sub'])
            update.add_query_param('Type', types)
            update.add_query_param('Value', ip)
            rst_up = self.clt.do_action_with_exception(update)
            return rst_up








