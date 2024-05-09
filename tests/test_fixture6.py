import pytest

@pytest.fixture()
def first():
    print('获取用户名')
    a = 'yoyo'
    return a

@pytest.fixture()
def second(first):
    a = first
    b = '123456'
    return (a, b)

def test_1(second):
    print('测试账户: %s, 密码: %s' % (second[0], second[1]))
    
    assert second[0] == 'yoyo'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture6.py'])