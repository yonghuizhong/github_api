import requests
import json
import mysql.connector
from multiprocessing import Pool


def get_language(str_type):
    headers = {
        "Authorization": '放入自己的token'
    }
    # url = 'https://api.github.com/rate_limit'  # 查看请求次数，查询的次数为30次/分钟，其他为5000次/分钟
    url_rep = 'https://api.github.com/search/repositories?q=language:{}&sort=stars'.format(str_type)
    url_user = 'https://api.github.com/search/users?q=language:{}&sort=followers'.format(str_type)

    rep = requests.get(url_rep, headers=headers)
    rep_js = json.loads(rep.text)
    rep_nums = rep_js['total_count']

    user = requests.get(url_user, headers=headers)
    user_js = json.loads(user.text)
    user_nums = user_js['total_count']

    if str_type == 'C%2B%2B':
        str_type = 'C++'
    if str_type == 'C%23':
        str_type = 'C#'
    print(str_type, rep_nums, user_nums)

    config2 = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'database': 'git_visual',
        'charset': 'utf8'
    }
    con2 = mysql.connector.connect(**config2)  # 建立连接
    cursor2 = con2.cursor()

    # SQL 插入语句，注意字符串还要加单括号
    sql2 = """INSERT INTO language(users,
             repositories, type)
             VALUES (%d, %d, '%s')"""
    cursor2.execute(sql2 % (user_nums, rep_nums, str_type))
    con2.commit()  # 注意：插入是有提交这个语句的
    con2.close()


# get_language('JavaScript')
lan_array = ['JavaScript', 'Python', 'Java', 'PHP', 'Ruby', 'C%2B%2B', 'C', 'C%23', 'Shell', 'HTML']
if __name__ == '__main__':  # 采用多线程获取，因为本次总共查询不超过30次/min，所以不用设置sleep，其他视情况而定（注意！！）
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'database': 'git_visual',
        'charset': 'utf8'
    }
    con = mysql.connector.connect(**config)  # 建立连接
    cursor = con.cursor()
    # 如果test表已经存在使用 execute() 方法删除test表
    cursor.execute("DROP TABLE IF EXISTS language")

    sql = """CREATE TABLE language
    (
      users        INT      NOT NULL,
      repositories INT      NOT NULL,
      type         CHAR(50) NOT NULL PRIMARY KEY
    )"""
    cursor.execute(sql)  # 建表
    con.close()

    pool = Pool()
    pool.map(get_language, lan_array)


# config = {
#     'host': '127.0.0.1',
#     'user': 'root',
#     'password': 'root',
#     'port': 3306,
#     'database': 'git_visual',
#     'charset': 'utf8'
# }
# con = mysql.connector.connect(**config)  # 建立连接
# cursor = con.cursor()
# cursor.execute("select version()")
# data = cursor.fetchone()
# print('database version:%s' % data)
#
# con.close()
