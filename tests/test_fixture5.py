import pytest

@pytest.fixture()
def user():
    print('获取用户名')
    a = 'yoyo'
    return a

@pytest.fixture()
def pwd():
    print('获取密码')
    b = '123456'
    return b

def test_01(user, pwd):
    print('测试账号: %s, 密码: %s' % (user, pwd))
    assert user == 'yoyo'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture5.py'])