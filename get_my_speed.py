import requests
import json


def get_speed():
    headers = {
        "Authorization": 'token 放入自己的token'
    }
    url = 'https://api.github.com/rate_limit'  # 查看请求次数，查询的次数为30次/分钟，其他为5000次/小时
    rep = requests.get(url, headers=headers)
    rep_js = json.loads(rep.text)
    print(rep_js)


get_speed()
