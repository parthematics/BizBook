import requests
from bs4 import BeautifulSoup

payload = {
    'action': 'login',
    'username': '691615110@qq.com',
    'password': 'challengelab'
}

with session() as c:
    c.post('http://crunchbase.com/login.php', data=payload)
    response = c.get('http://crunchbase/protected_page.php')
    print(response.headers)
    print(response.text)
