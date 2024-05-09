import pytest

def test_1(first):
    print('测试账号: %s' % first)
    assert first == 'yoyo'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture11.py'])