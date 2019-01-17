#-*- coding:utf-8 -*-
"""
" Hive python udf
" ip 地址转地区
"
" Author: Mo<zhoujg@weipaitang.com>
" Date : 2019-01-17 11:57:32
"
" 用法：
" ## 添加脚本到 hive
" add file path/to/ip2region.db path/to/ip2Region.py ipath/to/p2area.py;
" ## 使用脚本
" select TRANSFORM(ip) USING "python ip2area.py" as (ip,country,province,city,isp) from  ( select '127.0.2222.1' as ip ) t;
"
"""
import sys, re

from ip2Region import Ip2Region

def check_ip(ipAddr):
    compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')

    if compile_ip.match(ipAddr):
        return True
    else:
        return False

searcher = Ip2Region("ip2region.db")

for line in sys.stdin:
    line = line.strip()

    # 检查 ip 是否合法
    if not check_ip(line):
        print(line)
        continue

    try:
        # 可替换的查询方式：memorySearch, btreeSearch, binarySearch
        # 速度：
        # memorySearch > btreeSearch > binarySearch
        data = searcher.btreeSearch(line)

        region = data["region"].split('|')
        # region[1] 为区域，如有需要，可加入到最后
        # a.append(region[1])
        del region[1]
        region.insert(0, line)

        # hive 中使用制表符(\t)来分隔字段，可返回多个字段供 hive 使用。
        print('\t'.join(region))
    except Exception as e:
        print(line)