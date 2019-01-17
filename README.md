# udf-ip2region
`Hive UDF`, 实现 `ip` 转地理位置

## 简介
- `ip2region.db`: 数据库来源：https://github.com/lionsoul2014/ip2region
该地址会定时更新，可设置定时更新此数据库文件。

- `ip2Region.py`: 为官方类，主要实现 `db` 文件数据查询。

- `ip2area.py`: 为 `hive` 需要调用的脚本。

## 添加脚本到 hive
```sql
add file /data/hive-pyhton-udf/udf-ip2region/ip2region.db /data/hive-pyhton-udf/udf-ip2region/ip2Region.py /data/hive-pyhton-udf/udf-ip2region/ip2area.py;
```

## Hive 中使用
```sql
select TRANSFORM(ip) USING "python ip2area.py" as (ip,country,province,city,isp) from  ( select '127.0.222.1' as ip ) t;
```