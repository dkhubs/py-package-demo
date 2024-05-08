import pytest

def test_s4(login):
    print('用例1: 登录之后其他动作1111')
    
def test_s5():
    print('用例2: 不需要登录, 操作2222')
        
if __name__ == '__main__':
    pytest.main(['-s', 'test_fix2.py'])