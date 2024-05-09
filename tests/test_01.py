# coding: utf-8

import pytest

# 测试登录数据
testUser = ['admin', 'zhangsan']
testPwd = ['123456', '654321']

@pytest.fixture(scope='module')
def input_user(request):
    user = request.param
    print('登录账户: %s' % user)
    return user

@pytest.fixture(scope='module')
def input_pwd(request):
    pwd = request.param
    print('登录密码: %s' % pwd)
    return pwd
    
@pytest.mark.parametrize('input_user', testUser, indirect=True)
@pytest.mark.parametrize('input_pwd', testPwd, indirect=True)
def test_login(input_user, input_pwd):
    a = input_user
    b = input_pwd
    print('测试数据 a->%s, b->%s' % (a, b))
    assert b
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_01.py'])