import pytest

@pytest.mark.run(order=2)
def test_foo():
    print('用例11111')
    assert True
    
@pytest.mark.run(order=1)
def test_bar():
    print('用例22222')
    assert True
    
@pytest.mark.run(order=3)
def test_g():
    print('用例33333')
    assert True