def test_01():
    a = 'hello'
    b = 'world'
    assert a== b
    
def test_02():
    a = 'hello'
    b = 'hello world'
    assert a == b
    
def test_03():
    a = 'hello'
    b = 'hello world'
    assert a in b
    
def test_04():
    a = 'hello'
    b = 'hello world'
    assert a not in b