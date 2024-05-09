# coding: utf-8

import pytest

@pytest.fixture(scope='module', autouse=True)
def start(request):
    print('开始执行module')
    print('module: %s ' % request.module.__name__)
    
    yield
    print('module: %s 执行完毕' % request.module.__name__)
    
class Test_aa():
    @pytest.fixture(scope='function', autouse=True)
    def open_home(self, request):
        print('function: %s ----' % request.function.__name__)

    def test_01(self):
        print('用例1')
        
    def test_02(self):
        print('用例2')

if __name__ == '__main__':
    pytest.main(['-s', 'test_03.py'])   