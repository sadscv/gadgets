#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-7-28 下午9:34
# @Author  : sadscv
# @File    : autoLogin.py

import requests


pre_url = 'http://222.204.3.221:804/srun_portal_pc.php?ac_id=1&url=www.baidu.com'
post_url = 'http://222.204.3.221:804/include/auth_action.php'
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'User-Agent': agent
}

logindata = {
    'action': 'login',
    'username': '416116115079',
    'password': '{B}Mjg2MTE1',
    'ac_id' : 1,
    'save_me' : 1,
    'ajax' : 1
}

print('#' * 80)

# p1 = session.get(pre_url)
def login(session):
    print(requests.get(pre_url))
    # p1_cookies = p1.cookies
    login_result = session.post(post_url, data=logindata, headers=headers)
    if login_result.status_code == 200:
        print('login success')
    else:
        print('login fail')

if __name__ == '__main__':
    session = requests.Session()
    login(session)
