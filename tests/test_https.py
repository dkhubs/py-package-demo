import requests
import urllib3
# urllib3.disable_warnings()

def test_h():
    urllib3.disable_warnings()
    url = 'https://www.cnblogs.com/yoyoketang'
    s = requests.session()
    s.verify = False
    r = s.get(url)
    assert '上海-悠悠' in r.text