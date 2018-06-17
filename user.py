import requests
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool
import mysql.connector
from requests.exceptions import ReadTimeout


def getFollowers(url):
    headers = {
        "Authorization": 'token 放入自己的token'
    }
    res = requests.get(url, headers=headers).json()
    id = res.get('id')
    followers = res.get('followers')
    name = res.get('name')
    config3 = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123456',
        'port': 3306,
        'database': 'gitdata'
    }
    db3 = mysql.connector.connect(**config3)  # 建立连接
    cursor3 = db3.cursor()

    sql3 = 'update user set followers={} where id={}'.format(followers, id)
    print(url, sql3)
    try:
        cursor3.execute(sql3)
        db3.commit()
    except Exception as e:
        print(e)
        db3.rollback()
    cursor3.close()
    db3.close()
    # print(followers,name)


def myfun(language):
    headers = {
        "Authorization": 'token 27f8fabbe550fd6dd42098c118628ab9ff04e0e2'
    }
    url = 'https://api.github.com/search/users?q=language:{}&sort=followers'.format(language)
    print(url)
    config2 = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123456',
        'port': 3306,
        'database': 'gitdata'
    }
    db2 = mysql.connector.connect(**config2)  # 建立连接
    cursor2 = db2.cursor()

    item = []
    try:
        response = requests.get(url, headers=headers).json()
        item = response.get('items')
    except ReadTimeout:
        print('error')
    urls = []
    sql2 = 'INSERT INTO User(id,name,url,language) values(%s,%s,%s,%s)'
    if item:
        for it in item:
            id2 = it.get('id')
            name = it.get('login')
            url = it.get('html_url')
            urls.append(it.get('url'))
            print(id2, name, url, language)
            try:
                cursor2.execute(sql2, (id2, name, url, language))
                db2.commit()
            except Exception as e:
                print(e)
                db2.rollback()
    cursor2.close()
    db2.close()

    pool1 = ThreadPool()
    pool1.map(getFollowers, urls)
    pool1.close()
    print(language, 'finish!')


if __name__ == '__main__':
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123456',
        'port': 3306,
        'database': 'gitdata'
    }
    db = mysql.connector.connect(**config)  # 建立连接
    cursor = db.cursor()
    # 如果表已经存在使用 execute() 方法删除表
    cursor.execute("DROP TABLE IF EXISTS User")

    sql = """CREATE TABLE IF NOT EXISTS User(id INT NOT NUll,
              name VARCHAR(255) NOT NULL,url VARCHAR(255) NOT NULL,followers INT ,
              language VARCHAR(50) NOT NULL,PRIMARY KEY (id))
          """
    cursor.execute(sql)
    cursor.close()
    db.close()

    pool = Pool()
    Language = ['JavaScript', 'Python', 'Java', 'PHP', 'Ruby', 'C%2B%2B', 'C', 'C%23', 'Shell', 'HTML']
    pool.map(myfun, Language)
    pool.close()
