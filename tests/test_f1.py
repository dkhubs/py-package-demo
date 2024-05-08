import pytest
import smtplib

@pytest.fixture(scope='module')
def smtp():
    with smtplib.SMTP('smtp.gmail.com') as smtp:
        yield smtp

@pytest.fixture(scope='module')
def smtp_connection(request):
    smtpConn = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
    def fin():
        print('teardown smtp_connection')
        smtpConn.close()
    request.addfinalizer(fin)
    return smtpConn

@pytest.fixture(scope='module')
def open():
    print('打开浏览器, 并且打开百度首页')
    
    yield
    print('执行teardown')
    print('关闭浏览器')
    
def test_s1(open):
    print('用例1: 搜索python-1')
    
    # raise NameError
    
def test_s2(open):
    print('用例2: 搜索python-2')
    
def test_s3(open):
    print('用例3: 搜索python-3')
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_f1.py'])