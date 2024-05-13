import pytest
import time

@pytest.fixture()
def set_up_fixture():
    time.sleep(0.1)
    yield
    time.sleep(0.2)
    
def test_01(set_up_fixture):
    print("测试用例1")
    time.sleep(1.0)
    
def test_02(set_up_fixture):
    print("测试用例2")
    time.sleep(0.6)
    
def test_03(set_up_fixture):
    print("测试用例3")
    time.sleep(1.2)
    
def test_04(set_up_fixture):
    print("测试用例4")
    time.sleep(0.8)

def test_05(set_up_fixture):
    print("测试用例5")
    time.sleep(2.8)