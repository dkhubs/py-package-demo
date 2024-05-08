# coding:utf-8

import pytest

# @pytest.fixture(scope='module')
# def open():
#     print('打开浏览器, 并且打开百度首页')
    
# def test_s1(open):
#     print('用例1: 搜索 python-1')
    
# def test_s2(open):
#     print('用例2: 搜索 python-2')
    
# def test_s3(open):
#     print('用例3: 搜索 python-3')
    
# if __name__ == '__main__':
#     pytest.main(['-s', 'test_f1.py'])

# @pytest.fixture(scope='module')
# def open():
#     print('打开浏览器, 并且打开百度首页')
    
#     yield
#     print('执行teardown!')
#     print('最后关闭浏览器')
    
# def test_s1(open):
#     print('用例1: 搜索 python-1')
    
# def test_s2(open):
#     print('用例2: 搜索 python-2')
    
# def test_s3(open):
#     print('用例3: 搜索 python-3')
    
# if __name__ == '__main__':
#     pytest.main(['-s', 'test_f1.py'])

# @pytest.fixture(scope='module')
# def open():
#     print('打开浏览器, 并且打开百度首页')
    
#     yield
#     print('执行teardown!')
#     print('最后关闭浏览器')
    
# def test_s1(open):
#     print('用例1: 搜索 python-1')
    
#     # 如果第一个用例异常, 不影响其他用例执行
#     raise NameError
# def test_s2(open):
#     print('用例2: 搜索 python-2')
    
# def test_s3(open):
#     print('用例3: 搜索 python-3')
    
# if __name__ == '__main__':
#     pytest.main(['-s', 'test_f1.py'])

# import smtplib
# import pytest

# @pytest.fixture(scope='module')
# def smtp():
#     with smtplib.SMTP('smtp.gmail.com') as smtp:
#         yield smtp

import smtplib
import pytest

@pytest.fixture(scope='module')
def smtp_connection(request):
    smtpConn = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
    def fin():
        print('teardown smtpConn')
        
    request.addfinalizer(fin)
    return smtpConn