# coding: utf-8

import pytest

canshu = [{'user':'admin', 'pwd':''}]

@pytest.fixture(scope='module')
def login(request):
    user = request.param['user']
    pwd = request.param['pwd']
    print('正在操作登录, 账户: %s, 密码: %s' % (user, pwd))
    if pwd:
        return True
    else:
        return False
    
@pytest.mark.parametrize('login', canshu, indirect=True)
class Test_xx():
    def test_01(self, login):
        res = login
        print('用例1: %s' % res)
        assert res == True
        
    def test_02(self, login):
        res = login
        print('用例2: %s' % res)
        if not res:
            pytest.xfail('登录不成功, 标记为xfail')
        assert 1 == 1
        
    def test_03(self, login):
        res = login
        print('用例3: %s' % res)
        if not res:
            pytest.xfail('登录不成功, 标记为xfail')
        assert 1 == 1
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_01.py'])