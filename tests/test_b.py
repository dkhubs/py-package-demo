import time
import pytest

@pytest.fixture(scope="function")
def setup_demo():
    yield 
    # raise TypeError("ERROR!")

def test_5(setup_demo):
    print("测试用例55555555")
    time.sleep(3)


def test_6():
    print("测试用例66666666")
    time.sleep(3)
    assert 1 == 2