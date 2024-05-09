import pytest

def is_true(a):
    if a > 0:
        return True
    else:
        return False
    
def test_01():
    a = 5
    b = -1
    assert is_true(a)
    assert not is_true(b)
    
def test_02():
    a = 'hello'
    b = 'hello world'
    assert a in b
    
def test_03():
    a = 5
    b = 6
    assert a != b
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_assert1.py'])
    