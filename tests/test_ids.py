import pytest

def login(username, password):
    return {'code':0, 'msg':'success'}

testDatas = [
    ({'username':'admin', 'password':'123456'}, 'success!'),
    ({'username':'zhangsan', 'password':'123456'}, 'success!'),
    ({'username':'lisi', 'password':'123456'}, 'success!')
]

@pytest.mark.parametrize('test_input,expected', testDatas, ids=['输入正确账号，密码，登录成功', '输入错误账号，密码，登录失败', '输入正确账号，密码，登录成功'])
def test_login(test_input, expected):
    result = login(test_input['username'], test_input['password'])
    assert result['msg'] == expected