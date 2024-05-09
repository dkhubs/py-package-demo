# pytest测试框架

### 1. 安装
```
pip install pytest
```

### 2. 用例设计原则

- 文件名以test_*.py文件和*_test.py

- 以test_开头的函数

- 以Test开头的类，test_开头的方法，并且不能带有__init__ 方法

- 所有的包pakege必须要有__init__.py文件

- 断言使用assert

#### 执行方法
```
1. pytest
2. py.test
3. python -m pytest
```

#### 执行用例规则

1. 执行某个目录下所有的用例
```
pytest 文件名/
```

2. 执行某一个py文件下用例
```
pytest 脚本名称.py
```

3. -k 按关键字匹配
```
pytest -k 'MyClass and not method'
```

4. 按节点运行
```
pytest test_mod.py::test_func

pytest test_mod.py::TestClass::test_method
```

5. 标记表达式
```
pytest -m slow
```

6. 从包里面运行
```
pytest --pyargs pkg.testing
```

7. 遇到错误时停止测试
```
pytest -x test_class.py
```

8. 达到指定数量错误时, 停止测试
```
pytest --maxfail=1
```

### 3. 前置(setup)和后置(teardown)

- 模块级: setup_module/teardown_module, 开始于模块始末, 全局的

```
# coding:utf-8
import pytest
# 函数式

def setup_module():
    print("setup_module：整个.py模块只执行一次")
    print("比如：所有用例开始前只打开一次浏览器")

def teardown_module():
    print("teardown_module：整个.py模块只执行一次")
    print("比如：所有用例结束只最后关闭浏览器")

def setup_function():
    print("setup_function：每个用例开始前都会执行")

def teardown_function():
    print("teardown_function：每个用例结束前都会执行")

def test_one():
    print("正在执行----test_one")
    x = "this"
    assert 'h' in x

def test_two():
    print("正在执行----test_two")
    x = "hello"
    assert hasattr(x, 'check')

def test_three():
    print("正在执行----test_three")
    a = "hello"
    b = "hello world"
    assert a in b

if __name__ == "__main__":
    pytest.main(["-s", "test_fixt.py"])
```

- 函数级: setup_function/teardown_function, 只对函数用例生效(不在类中)

```
# coding:utf-8
import pytest
# 函数式

def setup_function():
    print("setup_function：每个用例开始前都会执行")

def teardown_function():
    print("teardown_function：每个用例结束后都会执行")

def test_one():
    print("正在执行----test_one")
    x = "this"
    assert 'h' in x

def test_two():
    print("正在执行----test_two")
    x = "hello"
    assert hasattr(x, 'check')

def test_three():
    print("正在执行----test_three")
    a = "hello"
    b = "hello world"
    assert a in b

if __name__ == "__main__":
    pytest.main(["-s", "test_fixt.py"])
```

- 类级: setup_class/teardown_class, 只在类中前后运行一次(在类中)

- 方法级: setup_method/teardown_method, 开始于方法始末(在类中)

- 类里面的(setup/teardown)运行在调用方法的前后

### 4. fixture:自定义测试用例的预置条件

前面一篇讲到用例加setup和teardown可以实现在测试用例之前或之后加入一些操作, 但这种是整个脚本全局生效的, 如果我想实现以下场景: 用例1需要先登录，用例2不需要登录，用例3需要先登录。很显然这就无法用setup和teardown来实现了

#### fixture相对于setup和teardown的几点优势

- 命名方式灵活, 不局限于 setup 和 teardown

- conftest.py 配置里可以实现数据共享, 不需要import就能自动找到一些配置

- scope='module' 可以实现多个.py跨文件共享前置, 每个.py文件调用一次

- scope='session' 以实现多个.py跨文件使用一个session来完成多个用例

- scope='function' (默认级别) 使用场景: 用例1需要先登录，用例2不需要登录，用例3需要先登录

#### fixture 与 yield 关键字, 实现 teardown 操作

```
import pytest

@pytest.fixture(scope='module')
def open():
    print('打开浏览器, 并且打开百度首页')
    
    yield
    print('执行teardown!')
    print('最后关闭浏览器')
    
def test_s1(open):
    print('用例1: 搜索 python-1')
    
def test_s2(open):
    print('用例2: 搜索 python-2')
    
def test_s3(open):
    print('用例3: 搜索 python-3')
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_f1.py'])
```

##### yield 遇到异常

- 如果第一个用例异常, 不影响其他用例执行

```
import pytest

@pytest.fixture(scope='module')
def open():
    print('打开浏览器, 并且打开百度首页')
    
    yield
    print('执行teardown!')
    print('最后关闭浏览器')
    
def test_s1(open):
    print('用例1: 搜索 python-1')
    
    raise NameError
def test_s2(open):
    print('用例2: 搜索 python-2')
    
def test_s3(open):
    print('用例3: 搜索 python-3')
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_f1.py'])
```

- 如果在setup就异常了, 那么是不会去执行yield后面的teardown内容了

- yield也可以配合with语句使用
```
import smtplib
import pytest

@pytest.fixture(scope='module')
def smtp():
    with smtplib.SMTP('smtp.gmail.com') as smtp:
        yield smtp
```

#### addfinalizer 实现 teardown 操作

1. 除了 yield 可以实现 teardown, 在 request-context 对象中注册 addfinalizer 方法也可以实现终结函数
```
import smtplib
import pytest

@pytest.fixture(scope='module')
def smtp_connection(request):
    smtpConn = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
    def fin():
        print('teardown smtpConn')
        
    request.addfinalizer(fin)
    return smtpConn
```

2. yield 和 addfinalizer 方法都是在测试完成后调用相应的代码


***Fixtures可以选择使用yield语句为测试函数提供它们的值, 而不是return。在这种情况下, yield语句之后的代码块作为拆卸代码执行, 而不管测试结果如何。fixture功能必须只产生一次***

### 5. conftest.py配置

单独管理预置的操作场景, pytest默认读取conftest.py里面的配置。注意事项:

- conftest.py 配置脚本名称是固定的, 不能改名称

- conftest.py 与运行的用例要在同一个 package 下, 并且有 __init__.py 文件

- 不需要 import 导入 conftest.py, pytest 用例会自动查找

### 6. pytest生成html报告

pytest-HTML是一个插件，pytest用于生成测试结果的HTML报告

```
pip install pytest-html

pytest --html=report.html

# 指定报告路径
pytest --html=./report/report.html

# 报告独立显示
pytest --html=report.html --self-contained-html
```

#### 在html报告中展示报错截图 + 失败重跑

1. 失败截图可以写到conftest.py文件里, 这样用例运行时, 只要检测到用例实例, 就调用截图的方法, 并且把截图存到html报告上

```
from selenium import webdriver
import pytest

driver = None

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """当测试失败的时候, 自动截图, 展示到html报告中"""
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screenshot = driver.get_screenshot_as_base64()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                    'onclick="window.open(this.src)" align="right"/></div>' % screenshot
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        
@pytest.fixture(scope='session', autouse=True)
def browser(request):
    global driver
    if driver is None:
        driver = webdriver.Chrome()
    
    def end():
        driver.quit()
        
    request.addfinalizer(end)
    return driver

# test_01.py
from selenium import webdriver
import time

def test_yoyo_01(browser):
    browser.get('https://www.cnblogs.com/yoyoketang/')
    time.sleep(2)
    t = browser.title
    assert t == '上海-悠悠'

# test_02.py
from selenium import webdriver
import time

def test_yoyo_01(browser):
    browser.get("https://www.cnblogs.com/yoyoketang/")
    time.sleep(2)
    t = browser.title
    assert "上海-悠悠" in t
```

执行命令 `pytest --html=report.html --self-contained-html`

2. 失败重试

失败重跑需要依赖pytest-rerunfailures插件，使用pip安装就行

```
pip install pytest-rerunfailures
```

用例失败再重跑1次,命令行加个参数--reruns就行了

`pytest --reruns 1 --html=report.html --self-contained-html`

### 7. 参数化

1. pytest.mark.parametrize 装饰器可以实现测试用例参数化

```
# coding:utf-8
import pytest

@pytest.mark.parametrize('test_input,expected', [('3+5', 8), ('2+4', 6), ('6 * 9', 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_expectation.py'])
```

2. 它也可以标记单个测试实例在参数化，例如使用内置的mark.xfail
```
# coding:utf-8
import pytest

@pytest.mark.parametrize('test_input,expected', [('3+5', 8), ('2+4', 6), pytest.param('6*9', 42, marks=pytest.mark.xfail)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_expectation.py'])
```

#### 参数组合

若要获得多个参数化参数的所有组合，可以堆叠参数化装饰器

```
import pytest

@pytest.mark.parametrize('x', [0, 1])
@pytest.mark.parametrize('y', [2, 3])
def test_foo(x, y):
    print('测试数据组合: x->%s, y-%s' % (x, y))
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_canshu1.py'])
```

### 8. 命令行传参

命令行参数是根据命令行选项将不同的值传递给测试函数, 比如平常在cmd执行"pytest --html=report.html", 这里面的"--html=report.html"就是从命令行传入的参数: 对应的参数名称是html, 参数值是report.html

#### conftest 配置参数

1. 首先需要在conftest.py添加命令行选项, 命令行传入参数'--cmdopt', 用例如果需要用到从命令行传入的参数, 就调用cmdopt函数

```
# conftest.py

import pytest

def pytest_addoption(parser):
    parser.addoption('--cmdopt', action='store', default='type1', help='my option: type1 or type2')
    
@pytest.fixture
def cmdopt(request):
    return request.config.getoption('--cmdopt')
```

2. 测试用例编写

```
import pytest

def testanswer(cmdopt):
    if cmdopt == 'type1':
        print('first')
    elif cmdopt == 'type2':
        print('second')
    assert 0
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_sample.py'])
```

`pytest -s test_sample.py`

#### 带参数启动

1. 如果不带参数执行，那么传默认的default="type1"，接下来在命令行带上参数去执行

`pytest -s test_sample.py --cmdopt=type2`

2. 命令行传参数有两种写法，还有一种分成2个参数也可以的, 参数和名称用空格隔开

`pytest -s test_sample.py --cmdopt type2`

### 9. assert 断言

断言是写自动化测试基本最重要的一步，一个用例没有断言，就失去了自动化测试的意义了

什么是断言呢？简单来讲就是实际结果和期望结果去对比，符合预期那就测试pass，不符合预期那就测试 failed

#### assert

pytest允许您使用标准Python断言来验证Python测试中的期望和值

```
# test_assert1.py

def f():
    return 3

def test_function():
    assert f() == 5
```

#### 异常信息

接下来再看一个案例，如果想在异常的时候，输出一些提示信息，这样报错后，就方便查看是什么原因了

```
def f():
    return 3

def test_function():

    a = f()
    assert a % 2 == 0, "判断a为偶数，当前a的值为：%s"%a
```

#### 异常断言

```
import pytest

def test_zero_division():
    with pytest.raises(ZeroDivisionError) as excinfo:
        1 / 0
        
    assert excinfo.type == ZeroDivisionError
    assert 'division by zero' in str(excinfo.value)
```

excinfo 是一个异常信息实例，它是围绕实际引发的异常的包装器。主要属性是.type、.value 和 .traceback

***注意：断言type的时候，异常类型是不需要加引号的，断言value值的时候需转str***

在上下文管理器窗体中，可以使用关键字参数消息指定自定义失败消息：

```
with pytest.raises(ZeroDivisionError, message="Expecting ZeroDivisionError"):
    pass

结果：Failed: Expecting ZeroDivisionError
```

#### 常用断言

pytest里面断言实际上是python里面的assert断言方法, 常用的有以下几种

- assert xx 判断xx为真

- assert not xx 判断xx不为真

- assert a in b 判断b包含a

- assert a == b 判断a等于b

- assert a != b 判断a不等于b

```
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
```

### 10. skip 跳过用例

#### skip

1. 跳过测试函数最简单的方式是使用装饰器(reason参数可选填)
```
@pytest.mark.skip(reason='no way of currently testing this')
def test_the_unknown():
    ...
```

2. 也可以在测试执行或设置期间通过调用来强制跳过pytest.skip(reason)功能
```
def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")
```

3. 也可以使用命令性方法, pytest.skip(reason, allow_module_level = True)跳过整个模块级别
```
import pytest
if not pytest.config.getoption("--custom-flag"):
    pytest.skip("--custom-flag is missing, skipping tests", allow_module_level=True)
```

在导入时间无法评估跳过条件时, 该方法很有用

#### skipif

1. 有条件地跳过某些内容, 使用`-rs`时出现在摘要中

```
import sys
import pytest

@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_function():
    ...
```

2. 可以在模块之间共享skipif标记, 参考以下案例

```
import mymodule
minversion = pytest.mark.skipif(mymodule.__versioninfo__ < (1, 1), reason='at least mymodule-1.1 required')
@minversion
def test_funtion():
    ...
```

导入标记在另一个测试模块中重复使用它
```
from test_mymudlue import minversion
@minversion
def test_anotherfunction():
    ...
```

***对于较大的测试套件, 通常最好有一个文件来定义标记, 然后一致适用于整个测试套件***

#### skip类或模块

1. 在类上使用skipif标记, 如果条件为真则此标记将为该类的每个测试方法生成跳过结果

```
import sys
import pytest
@pytest.mark.skipif(sys.platform == 'win32', reason='does not run on windows')
class TestPosixCalls(object):
    def test_function(self):
        'will not be setup or run under "win32" platform'
```

**不要在使用继承的类上使用skipif, pytest中的一个已知错误可能会导致超类中的意外行为**

2. 在全局级别使用pytestmark名称, 跳过模块的所有测试功能

#### skip文件或目录

有时您可能需要跳过整个文件或目录, 例如:如果测试依赖于特定于Python的版本功能或包含您不希望pytest运行的代码

#### skip缺少导入依赖项

1. 可以在模块级别或测试设置功能中使用以下帮助程序, 如果无法在此处导入docutils, 则会导致测试跳过结果
```
docutils = pytest.importorskip('docutils')
```

2. 跳过库的版本号, 将从指定模块的__version__属性中读取版本
```
docutils = pytest.importorskip('docutils', minversion='0.3')
```

#### Summary -- 介绍在不同情况下跳过模块中的测试

1. 无条件地跳过模块中的所有测试

```
pytestmark = pytest.mark.skip('all tests still WIP')
```

2. 根据某些条件跳过模块中的所有测试

```
pytestmark = pytest.mark.skipif(sys.platform == 'win32', 'tests for linux -> only')
```

3. 如果缺少某些导入, 则跳过模块中的所有测试

```
pexpect = pytest.importorskip('pexpect')
```

### 11. 函数传参和fixture传参--request

函数的作用: 提高代码的复用性, 方便在用例中按需调用

#### 登录函数传参

1. 把登录功能独立出来, 单独写一个函数: 传入2个参数user和pwd, 写用例的时候调用登录函数, 输入几组user, pwd参数化登录用例

测试用例传参需要用装饰器@pytest.mark.parametrize, 里面写两个参数

- 第一个参数是字符串, 多个参数中间用逗号隔开

- 第二个参数是list, 多组数据用元组类型

```
# test_01.py

# coding: utf-8

import pytest

# 测试登录数据
testLoginData = [('admin', '111111'), ('zhangsan', '')]

def login(user, pwd):
    print('登录账号：%s, 密码: %s' % (user, pwd))
    if pwd:
        return True
    else:
        return False
    
@pytest.mark.parametrize('user, pwd', testLoginData)
def test_login(user, pwd):
    res = login(user, pwd)
    assert res == True, '失败原因: 密码为空'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_01.py'])
```

#### request参数

如果想把登录操作放到前置操作里, 也就是用到@pytest.fixture装饰器, 传参就用默认的request参数

```
# coding: utf-8

import pytest

# 测试登录数据
testLoginData = ['admin', 'zhangsan']

@pytest.fixture(scope='module')
def login(request):
    user = request.param
    print('登录账户：%s' % user)
    return user
    
@pytest.mark.parametrize('login', testLoginData, indirect=True)
def test_login(login):
    res = login
    print('测试用例中Login的返回值: %s' % res)
    assert res != ''
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_01.py'])
```

***添加indirect=True参数是为了把login当成一个函数去执行, 而不是一个参数***

#### request传2个参数

如果用到@pytest.fixture里面用2个参数的情况, 可以把多个参数用一个字典去存储, 这样最终还是只传一个参数; 不同的参数再从字典里面取对应key值就行, 如: user = request,param['user']

```
# coding: utf-8

import pytest

# 测试登录数据
testLoginData = [{'user':'admin', 'pwd':'111111'}, {'user':'zhangsan', 'pwd':''}]

@pytest.fixture(scope='module')
def login(request):
    user = request.param['user']
    pwd = request.param['pwd']
    print('登录账户：%s, 密码: %s' % (user, pwd))
    if pwd:
        return True
    else:
        return False
    
# indirect=True 声明login是一个fixture
@pytest.mark.parametrize('login', testLoginData, indirect=True)
def test_login(login):
    res = login
    print('测试用例中Login的返回值: %s' % res)
    assert res, '失败原因: 密码为空'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_01.py'])
```

***如果要用到login里面的返回值, def test_login(login)时, 传入login参数, 函数返回值就是login了***

#### 多个fixture

用例上面可以同时放多个fixture(也就是前置操作): 可以支持装饰器叠加, 使用parametrize装饰器叠加时, 用例组合是2个参数个数相乘

```
# coding: utf-8

import pytest

# 测试登录数据
testUser = ['admin', 'zhangsan']
testPwd = ['123456', '654321']

@pytest.fixture(scope='module')
def input_user(request):
    user = request.param
    print('登录账户: %s' % user)
    return user

@pytest.fixture(scope='module')
def input_pwd(request):
    pwd = request.param
    print('登录密码: %s' % pwd)
    return pwd
    
@pytest.mark.parametrize('input_user', testUser, indirect=True)
@pytest.mark.parametrize('input_pwd', testPwd, indirect=True)
def test_login(input_user, input_pwd):
    a = input_user
    b = input_pwd
    print('测试数据 a->%s, b->%s' % (a, b))
    assert b
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_01.py'])
```

### 自定义标记 mark

自定义标记可以把一个web项目划分多个模块, 然后指定模块名称执行。一个大项目自动化用例时, 可以划分多个模块, 也可以使用标记功能, 标明哪些是模块1用例、哪些是模块2的, 运行代码时指定mark名称运行就可以

#### mark标记

1. 以下用例, 标记test_send_http()为webtest

```
# test_server.py

# coding: utf-8

import pytest

@pytest.mark.webtest
def test_send_http():
    pass

def test_something_quick():
    pass

def test_another():
    pass

class TestClass:
    def test_method(self):
        pass
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_server.py', '-m=webtest'])
```

#### `::` 指定函数节点id

1. 例如想指定运行某个.py模块下, 类里面的一个用例

`pytest -v test_server.py::TestClass::test_method`

2. 运行整个类

`pytest -v test_server.py::TestClass`

3. 也能选择多个节点运行, 多个节点中间用空格隔开

`pytest -v test_server.py::TestClass test_server.py::test_send_http`

4. -k 匹配用例名称

- 匹配用例名称包含http的 `pytest -v -k http`

- 排除用例名称包含 send_http的 `pytest -k "not send_http" -v`

- 同时选择匹配 http 和 quick `pytest -k "http or quick" -v`