import pytest

@pytest.fixture()
def login():
    print('前置操作: 准备数据')
    yield
    print('后置操作: 清理数据')
    
def test_01(login):
    a = 'hello'
    b = 'hello'
    assert a == b

def test_02(login):
    a = 'hello'
    b = 'hello world'
    assert a == b
    