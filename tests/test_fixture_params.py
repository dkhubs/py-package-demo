import pytest

def delete_sql(user):
    sql = 'delete fron auth_user WHERE username = "%s";' % user
    print('执行的SQL: %s' % sql)
    
userData = ['admin', 'zhangsan']

@pytest.fixture(scope='function', params=userData)
def users(request):
    # 前置操作
    delete_sql(request.param)
    
    yield request.param
    
    # 后置操作
    delete_sql(request.param)
    
def test_request(users):
    print('注册用户: %s' % users)
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture_params.py'])