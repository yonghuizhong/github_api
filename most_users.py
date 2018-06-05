import mysql.connector
from multiprocessing import Pool

# 最大since值为limit，则共形成limit/100=39万条，为获取数据的链接(07-18年的大部分数据，每个链接可得到30条用户数据)
limit = 39000000


def gen_all_links(begin, end):
    list_array = []
    for k in range(begin, end, 100):
        if k <= limit:
            list_url = 'https://api.github.com/users?since={}'.format(k)
            print(k, list_url)
            list_array.append((k, list_url))

    config2 = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'database': 'user_test'
    }
    con2 = mysql.connector.connect(**config2)  # 建立连接
    cursor2 = con2.cursor()
    # SQL 插入语句，注意字符串还要加单括号
    sql2 = "INSERT INTO list(since, url) VALUES (%s, %s)"   # 不管什么类型，统一使用%s作为占位符
    cursor2.executemany(sql2, list_array)   # 一次插入多条数据
    con2.commit()  # 注意：插入是有提交这个语句的
    cursor2.close()
    con2.close()


if __name__ == '__main__':
    # 创建数据库表list
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'database': 'user_test'
    }
    con = mysql.connector.connect(**config)  # 建立连接
    cursor = con.cursor()
    # 如果表已经存在使用 execute() 方法删除表
    cursor.execute("DROP TABLE IF EXISTS list")
    sql = """CREATE TABLE list
        (
          since        INT   NOT NULL  PRIMARY KEY,
          url         VarCHAR(200) NOT NULL
        )"""
    cursor.execute(sql)  # 建表
    cursor.close()
    con.close()

    # 数据列表链接的获取
    num_array = [(i, i + 500000) for i in range(0, limit, 500000)]  # 分批次，一批次共500000/100=5000条链接
    print(num_array)
    pool = Pool()
    pool.starmap(gen_all_links, num_array)  # starmap:传入多个参数


