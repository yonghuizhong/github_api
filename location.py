import random
import requests
import json
import time
import mysql.connector


def get_area(area, area_chinese):
    time.sleep(random.uniform(1, 2))
    headers = {
        "Authorization": 'token 27f8fabbe550fd6dd42098c118628ab9ff04e0e2'
    }
    url = 'https://api.github.com/search/users?q=location:{}'.format(area)
    url_cn = 'https://api.github.com/search/users?q=location:{}'.format(area_chinese)
    print(url)

    req = requests.get(url, headers=headers)    # 获取英文地区名的
    req_js = json.loads(req.text)
    num_en = req_js['total_count']

    req_cn = requests.get(url_cn, headers=headers)  # 获取中文地区名的
    req_cn_js = json.loads(req_cn.text)
    num_cn = req_cn_js['total_count']

    nums = num_en + num_cn  # 数据相加
    print(area, area_chinese, nums)

    config2 = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'database': 'gitdata'
    }
    con2 = mysql.connector.connect(**config2)  # 建立连接
    cursor2 = con2.cursor()

    sql = "INSERT INTO location(location, location_cn, usernum) values('%s', '%s', %d)"
    try:
        cursor2.execute(sql % (area, area_chinese, nums))
        con2.commit()
    except Exception as e:
        con2.rollback()
        print(e)
    con2.close()


if __name__ == '__main__':
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'database': 'gitdata'
    }
    con = mysql.connector.connect(**config)  # 建立连接
    cursor = con.cursor()
    # 如果表已经存在使用 execute() 方法删除表
    cursor.execute("DROP TABLE IF EXISTS location")

    my_sql = """CREATE TABLE location
        (
          usernum INT NOT NULL,
          location_cn CHAR(50) NOT NULL,
          location CHAR(50) NOT NULL PRIMARY KEY
        )"""
    cursor.execute(my_sql)  # 建表
    con.close()

    area_array = ['Anhui', 'Beijing', 'Fujian', 'Gansu', 'Guangdong',
                  'Guangxi', 'Guizhou', 'Hainan', 'Hebei', 'Henan', 'Heilongjiang',
                  'Hubei', 'Hunan', 'Jilin', 'Jiangsu', 'Jiangxi', 'Liaoning', 'Inner Mongoria IM',
                  'Ningxia', 'Qinghai', 'Shandong', 'Shanxi', 'Shaanxi', 'Shanghai', 'Sichuan', 'Tianjing',
                  'Tibet', 'Xinjiang', 'Yunnan', 'Zhejiang', 'Chongqing', 'Macao', 'Hong Kong', 'Taiwan']
    area_cn_array = ['安徽', '北京', '福建', '甘肃', '广东',
                     '广西', '贵州', '海南', '河北', '河南', '黑龙江',
                     '湖北', '湖南', '吉林', '江苏', '江西', '辽宁', '内蒙古',
                     '宁夏', '青海', '山东', '山西', '陕西', '上海', '四川', '天津',
                     '西藏', '新疆', '云南', '浙江', '重庆', '澳门', '香港', '台湾']

    for en, cn in zip(area_array, area_cn_array):
        get_area(en, cn)
