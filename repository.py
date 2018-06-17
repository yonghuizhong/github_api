import requests
from multiprocessing import Pool
import mysql.connector
from requests.exceptions import ReadTimeout


def myfun(language):
    headers = {
        "Authorization": 'token 放入自己的token'
    }
    url = 'https://api.github.com/search/repositories?q=language:{}&sort=stars'.format(language)
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
    sql2 = 'INSERT INTO Repository(id, name,star,url,language) values(%s, %s, %s,%s,%s)'
    if item:
        for it in item:
            id2 = it.get('id')
            name = it.get('full_name')
            url = it.get('html_url')
            star = it.get('stargazers_count')
            language = it.get('language')
            print(id2, name, star, url, language)
            try:
                cursor2.execute(sql2, (id2, name, star, url, language))
                db2.commit()
            except Exception as e:
                print(e)
                db2.rollback()
    cursor2.close()
    db2.close()


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
    cursor.execute("DROP TABLE IF EXISTS Repository")

    sql = """CREATE TABLE IF NOT EXISTS Repository(id VARCHAR(255) NOT NULL,
              name VARCHAR(255) NOT NULL,star INT NOT NULL,url VARCHAR(255) NOT NULL, 
              language VARCHAR(255) NOT NULL, PRIMARY KEY (id))
          """
    cursor.execute(sql)
    cursor.close()
    db.close()

    pool = Pool()
    Language = ['JavaScript', 'Python', 'Java', 'PHP', 'Ruby', 'C%2B%2B', 'C', 'C%23', 'Shell', 'HTML']
    pool.map(myfun, Language)
    pool.close()
