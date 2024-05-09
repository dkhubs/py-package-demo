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

### 失败标记 xfail

场景描述: 当用例a失败的时候, 如果用例b和用例c都依赖于a的结果, 那可以直接跳过用例b和c的测试, 直接给它们标记为xfail

#### 用例设计

1. pytest里面用xfail标记用例为失败的用例, 可以直接跳过。基本实现思路

- 把登录写为前置操作

- 对登录的账户和密码参数化, 参数用 canshu = [{'user':'admin', 'pwd':'111'}] 表示

- 多个用例放到一个Test_xx的class里面

- test_01, test_02, test_03全部调用fixture里面的login功能

- test_01测试登录用例

- test_02和test_03执行前用if判断登录的结果, 登录失败就执行, pytest.xfail('登录不成功, 标记为xfail')

```
# coding: utf-8

import pytest

canshu = [{'user':'admin', 'pwd':'123456'}]

@pytest.fixture(scope='module')
def login(request):
    user = request.param['user']
    pwd = request.param['pwd']
    print('正在操作登录, 账户: %s, 密码: %s' % (user, pwd))
    if pwd:
        return True
    else:
        return False
    
@pytest.mark.parametrize('login', canshu, indirect=True)
class Test_xx():
    def test_01(self, login):
        res = login
        print('用例1: %s' % res)
        assert res == True
        
    def test_02(self, login):
        res = login
        print('用例2: %s' % res)
        if not res:
            pytest.xfail('登录不成功, 标记为xfail')
        assert 1 == 1
        
    def test_03(self, login):
        res = login
        print('用例3: %s' % res)
        if not res:
            pytest.xfail('登录不成功, 标记为xfail')
        assert 1 == 1
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_01.py'])
```

#### 标记为xfail

让pwd参数为空, 再看看登录失败情况的用例, 修改登录的参数

### fixture的autouse参数

调用fixture的三种方法

1. 函数或类里面方法直接传fixture的函数参数名称。先定义start功能, 用例全部传start参数, 调用该功能

```
# coding: utf-8

import time
import pytest

@pytest.fixture(scope='function')
def start(request):
    print('\n-----开始执行function------')
    
def test_a(start):
    print('-----用例a执行-----')
    
class Test_aaa():
    def test_01(self, start):
        print('-----用例1执行-----')
    def test_02(self, start):
        print('-----用例2执行-----')
        
if __name__ == '__main__':
    pytest.main(['-s', 'test_03.py'])   
```

2. 使用装饰器@pytest.mark.usefixtures()修饰需要运行的用例

```
# coding: utf-8

import time
import pytest

@pytest.fixture(scope='function')
def start(request):
    print('开始计时')

@pytest.mark.usefixtures('start')
def test_1():
    print('用例1: 用例1')
    
@pytest.mark.usefixtures('start')
def test_2():
    print('用例2: 用例2')

if __name__ == '__main__':
    pytest.main(['-s', 'test_03.py'])   
```

3. autouse = True自动调用fixture功能, 用例很多的时候这个方法更方便

- start设置scope为module级别, 在当前.py用例模块只执行一次, autouse=True自动使用

- open_home设置scope为function级别, 每个用例前都调用一次, 自动使用

```
# coding: utf-8

import pytest

@pytest.fixture(scope='module', autouse=True)
def start(request):
    print('开始执行module')
    print('module: %s ' % request.module.__name__)
    
    yield
    print('module: %s 执行完毕' % request.module.__name__)
    
@pytest.fixture(scope='function', autouse=True)
def open_home(request):
    print('function: %s ----' % request.function.__name__)

def test_01():
    print('用例1')
    
def test_02():
    print('用例2')

if __name__ == '__main__':
    pytest.main(['-s', 'test_03.py'])   
```

写到class里一样可以

```
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
```

### 配置文件 pytest.ini

**路径：放在顶层文件夹下**

它是一个固定的文件, 读取配置信息, 按照指定的方式去运行

pytest里面有些文件是非test文件

- pytest.ini pytest的主配置文件, 可以改变pytest的默认行为

- conftest.py 测试用例的一些fixture配置

- __init__.py 识别该文件夹为python的package包

- tox.ini 与 pytest.ini 类似, 用 tox 工具时候才有用

- setup.cfg 也是ini格式文件, 影响setup.py的行为

ini文件基本格式

```
# 保存为pytest.ini文件

[pytest]
addopts = -rsxX
xfail_strict = true
```

***-rsxX 表示 pytest 报告所有测试用例被跳过、预计失败、预计失败但实际被通过的原因***

#### mark标记

1. 编写用例
```
import pytest

@pytest.mark.webtest
def test_send_http():
    print("mark web test")

def test_something_quick():
    pass

def test_another():
    pass

@pytest.mark.hello
class TestClass:
    def test_01(self):
        print("hello :")

    def test_02(self):
        print("hello world!")

if __name__ == "__main__":
    pytest.main(["-v", "test_mark.py", "-m=hello"])
```

2. 配置标签
```
[pytest]

markers =
    webtest: Run the webtest case
    hello: Run the hello case
```

3. 执行 `pytest --markers`

#### 禁用xpass

设置 xfail_strict = true 可以让那些标记为 @pytest.mark.xfail 但实际通过的测试用例被报告为失败

```
import pytest

def test_hello():
    print('hello world!')
    assert 1

@pytest.mark.xfail()
def test_xfail():
    a = 'hello'
    b = 'hello world'
    assert a == b
    
@pytest.mark.xfail()
def test_xpass():
    a = 'hello'
    b = 'hello world!'
    assert a != b
    
if __name__ == '__main__':
    pytest.main(['-v', 'test_xpass.py'])
```

test_aa 和 test_bb 这2个用例一个是 `a == b`, 一个是 `a == b`, 两个都标记失败了，我们希望两个用例不用执行全部显示xfail。实际上最后一个却显示xpass。为了让两个都显示xfail，那就加个配置

```
xfail_strict = true
```

#### addopts

addopts参数可以更改默认命令行选项, 这个当我们在cmd输入指令去执行用例的时候, 会用到, 比如我想测试完生成报告, 指令比较长

```
pytest -v --reruns 1 --html=report.html --self-contained-html
```

每次输入这么多不太好记, 于是可以加到 pytest.ini 里

```
# pytest.ini
[pytest]

markers =
  webtest:  Run the webtest case
  hello: Run the hello case

 xfail_strict = true

 addopts = -v --reruns 1 --html=report.html --self-contained-html
```

### doctest测试框架

doctest从字面意思上看, 就是文档测试。doctest是python里面自带的一个模块, 它实际上是单元测试的一种。官方解释: doctest模块会搜索那些看起来像交互会话的Python代码片段, 然后尝试执行并验证结果

doctest测试用例可以放在两个地方

- 函数或者方法下的注释里面

- 模块的开头

#### 案例

将需要测试的代码片段，标准格式，需要运行的代码前加>>>, 相当于进入cmd这种交互环境执行, 期望的结果前面不需要加>>>
```
>>> multiply(4, 3)
    12
>>> multiply('a', 3)
    'aaa'
```

放到multiply函数的注释里
```
def multiply(a, b):
    """
    function: 两个数相乘
    >>> multiply(4, 3)
    12
    >>> multiply('a', 3)
    'aaa'
    """
    return a * b

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
```

#### 失败案例

doctest的内容放到.py模块的开头也是可以识别到的

```
'''
function: 两个数相乘
>>> multiply(4, 8)
12
>>> multiply('a', 5)
'aaa'
'''

def multiply(a, b):
    """
    function: 两个数相乘
    """
    return a * b

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
```

***verbose参数, 设置为True则在执行测试的时候会输出详细信息***

#### cmd执行

以上案例是在编辑器直接运行的, 如果在cmd里面, 也可以用指令去执行

```
python -m doctest -v xxx.py
```

- m 参数指定运行方式为 doctest

- -v 参数是verbose, 带上 -v 参数相当于 verbose=True

#### pytest运行

pytest框架是可以兼容doctest用例, 执行的时候加个参数 --doctest-modules, 这样它就能自动搜索到doctest的用例

```
pytest -v --doctest-modules xxx.py
```

#### doctest独立文件

doctest内容也可以和代码抽离开, 单独用一个.txt文件保存。在当前xxx.py同一目录新建一个xxx.txt文件，写入测试的文档, 要先导入该功能, 导入前面也要加>>>

```
>>> from xxx import multiply
>>> multiply(4, 3)
12
>>> multiply('a', 3)
'aaa'
```

命令行执行用例 `python -m doctest -v xxx.txt`

### pytest-html报告优化(添加Description)

pytest-html框架是可以修改生成的报告内容的, 可以自己添加和删除html报告的table内容

#### 修改报告

可以通过标题行实现自定义钩子来修改列, 下面的示例在conftest.py脚本中使用测试函数docstring添加描述(Description)列, 添加可排序时间(Time)列, 并删除链接(Link)列

```
# 安装库
# pip install -U py

import pytest
from py.xml import html

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()
    
@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()
    
@pytest.mark.optionalhook
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
```

1. 通过删除所有单元格来删除结果

```
import pytest

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    if report.passed:
      del cells[:]
```

2. 日志输出和附加HTML可以通过pytest_html_results_table_html hooks来修改

```
import pytest

@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('No log output captured.', class_='empty log'))
```

#### 添加 Desciption

通过上面的官方文档, 可以自己修改测试报告, 在报告里面添加一列的内容, 添加到第二列, 于是修改如下

```
import pytest
from py.xml import html

driver = None

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))

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
        report.description = str(item.function.doc)
```

执行用例生成报告 `pytest --html=report.html --self-contained-html`

### fixtue详细介绍

fixture是pytest的核心功能, 也是亮点功能, 熟练掌握fixture的使用方法, pytest用起来才会得心应手

#### fixture简介

fixture的目的是提供一个固定基线, 该基线上测试可以可靠地和重复地执行

- 有独立的命名, 并通过声明它们从测试函数、模块、类或整个项目中的使用来激活

- 按模块化的方式实现, 每个fixture都可以互相调用

- fixture的范围从简单的单元扩展到复杂的功能测试, 允许根据配置和组件选项对fixture和测试用例进行参数化, 或者跨函数function、类class、模块module或整个测试会话session范围

#### fixtuer作为参数传入

定义fixture跟定义普通函数差不多, 唯一区别就是在函数上加个装饰器@pytest.fixture()

- fixture命名不要用test_开头, 跟用例区分开

- fixture是可以有返回值的, 如果没有return默认返回None。用例调用fixture的返回值, 直接就是把fixture的函数名称当成变量名称

```
import pytest

@pytest.fixture()
def user():
    print('获取用户名称')
    a = 'yoyo'
    return a

def test_1(user):
    assert user == 'yoyo'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture1.py'])
```

#### error 和 failed 区别

测试结果一般有三种: passed、failed、error(skip的用例除外)

1. 如果在test_用例里面断言失败, 那就是failed

```
import pytest

@pytest.fixture()
def user():
    print('获取用户名')
    a = 'yoyo'
    return a

def test_1(user):
    assert user == 'yoyo111' # 用例失败就是failed
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture2.py'])
```

2. 如果在fixture里面断言失败了, 那就是error

```
import pytest

@pytest.fixture()
def user():
    print('获取用户名')
    a = 'yoyo'
    assert a == 'yoyo123' # fixture失败就是error
    return a

def test_1(user):
    assert user == 'yoyo'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture3.py'])
```

### 多个fixture及相互调用

#### 使用多个fixture

如果用例需要用到多个fixture的返回数据, fixture也可以

1. return一个元组、list或字典, 然后从里面取出对应数据

```
import pytest

@pytest.fixture()
def user():
    print('获取用户名')
    a = 'yoyo'
    b = '123456'
    return (a, b)

def test_1(user):
    u = user[0]
    p = user[1]
    print('测试账户: %s, 密码: %s' % (u, p))
    assert u == 'yoyo'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture4.py'])
```

2. 分开定义成多个fixtuer, 然后test_用例传入多个fixture参数

```
import pytest

@pytest.fixture()
def user():
    print('获取用户名')
    a = 'yoyo'
    return a

@pytest.fixture()
def pwd():
    print('获取密码')
    b = '123456'
    return b

def test_01(user, pwd):
    print('测试账号: %s, 密码: %s' % (user, pwd))
    assert user == 'yoyo'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture5.py'])
```

#### fixture之间互相调用

```
import pytest

@pytest.fixture()
def first():
    print('获取用户名')
    a = 'yoyo'
    return a

@pytest.fixture()
def second(first):
    a = first
    b = '123456'
    return (a, b)

def test_1(second):
    print('测试账户: %s, 密码: %s' % (second[0], second[1]))
    
    assert second[0] == 'yoyo'
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_fixture6.py'])
```

### fixture 作用范围

fixture里面有个scope参数可以控制fixture的作用范围: session > module > class > function(默认)

- function 每个函数或方法都会调用

- class 每个类调用一次, 一个类可以有多个方法

- module 每个.py文件调用一次, 该文件内又有多个function和class

- session 是多个文件调用一次, 可以跨.py文件调用, 每个.py文件就是module。也就是当我们有多个.py文件用例的时候, 如果多个用例只需要调用一次fixture, 那就可以设置为scope='session', 并且写到conftest.py文件里

```
# conftest.py

import pytest
@pytest.fixture(scope='session')
def first():
    print('\n获取用户名, scope为session级别多个.py模块只运行一次')
    a = 'yoyo'
    return a
```

### conftest.py 的作用范围

一个测试工程下是可以有多个 conftest.py 的文件, 一般在工程根目录放一个 conftest.py 起到全局作用。在不同的测试子目录也可以放 conftest.py, 作用范围只在该层级以及以下目录生效

#### conftest 层级关系

在 web_conf+py 项目工程下建两个子项目 baidu、blog, 并且每个目录下都放一个 conftest.py 和 __init__.py (python的每个package必须要有__init__.py)

```
web_conf_py 是工程名称

├─baidu
│  │  conftest.py
│  │  test_1_baidu.py
│  │  __init__.py
│  
│          
├─blog
│  │  conftest.py
│  │  test_2_blog.py
│  │  __init__.py
│   
│  conftest.py
│  __init__.py

```

1. 案例分析

web_conf_py 工程下 conftest.py 文件代码案例

```
import pytest

@pytest.fixture(scope='session')
def start():
    print('\n打开首页')
```

baidu目录下 conftest.py 和 test_1_baidu.py

```
# web_conf_py/baidu/conftest.py
import pytest

@pytest.fixture(scope='session')
def open_baidu():
    print('打开百度页面_session')

# web_conf_py/baidu/test_1_baidu.py
import pytest

def test_01(start, open_baidu):
    print('测试用例 test_01')
    assert 1

def test_02(start, open_baidu):
    print('测试用例 test_02')
    assert 1

if __name__ == '__main__':
    pytest.main(['-s', 'test_1_baidu.py'])
```

blog 目录下 conftest.py 和 test_2_blog.py 代码

```
# web_conf_py/blog/conftest.py
import pytest

@pytest.fixture(scope='function')
def open_blog():
    print('打开 blog 页面 _function')

# web_conf_py/blog/test_2_blog.py
import pytest

def test_03(start, open_blog):
    print('测试用例 test_03')
    assert 1

def test_04(start, open_blog):
    print('测试用例 test_04')
    assert 1

def test_05(start, open_baidu):
    print('测试用例 test_05, 跨模块调用 baidu')
    assert 1

if __name__ == '__main__':
    pytest.main(['-s', 'test_2_blog.py'])
```

### 运行上次失败用例

"80%的bug集中在20%的模块, 越是容易出现bug的模块, bug是越改越多" 平常我们做手工测试的时候, 比如用100个用例需要执行, 其中10个用例失败了, 当开发修复完bug后, 我们一般是重点测上次失败的用例。那么自动化测试也一样, 当用例特别多时, 为了节省时间, 第一次部分用例失败了, 修复完之后, 可以只测上次失败的用例

#### `--lf`

--last-failed 只重新运行上次运行失败的用例(或如果没有失败的话会全部跑)


#### `--ff`

--failed-first 运行所有测试，但首先运行上次运行失败的测试(这可能会重新测试，从而导致重复的fixture setup/teardown)

### pytest分布式执行插件 pytest-xdist

1. 安装

```
pip install pytest-xdist
```

2. [pytest-xdist](https://github.com/pytest-dev/pytest-xdist/blob/master/OVERVIEW.md) 插件扩展了一些独特的测试执行模式 pytest

- 测试运行并行化: 如果有多个CPU或主机, 则可以将它们用于组合测试运行, 加快运行速度

- --looponfail: 在子进程中重复运行测试, 每次运行之后, pytest会等待, 直到项目中的文件发生更改, 然后重新运行以前失败的测试。重复此过程直到所有测试通过, 之后再次执行完整运行

- 多平台覆盖: 您可以指定不同的Python解释器或不同的平台, 并在所有平台上并行运行测试。在远程运行测试之前, pytest有效地将程序源代码`rsyncs`到远程位置, 报告所有测试结果并显示给本地终端

3. 并行测试

多CPU并行执行用例, 直接加个-n参数即可, 后面num参数就是并行数量, 比如num设置为3

```
pytest -n 3
```

4. 运行以下代码, 项目结构如下

```
web_conf_py是项目工程名称
│  conftest.py
│  __init__.py
│              
├─baidu
│  │  conftest.py
│  │  test_1_baidu.py
│  │  test_2.py
│  │  __init__.py 
│          
├─blog
│  │  conftest.py
│  │  test_2_blog.py
│  │  __init__.py   
```

代码参考

```
# web_conf_py/conftest.py
import pytest

@pytest.fixture(scope="session")
def start():
    print("\n打开首页")
    return "yoyo"

# web_conf_py/baidu/conftest.py
import pytest

@pytest.fixture(scope="session")
def open_baidu():
    print("打开百度页面_session")

# web_conf_py/baidu/test_1_baidu.py
import pytest
import time

def test_01(start, open_baidu):
    print("测试用例test_01")
    time.sleep(1)
    assert start == "yoyo"

def test_02(start, open_baidu):
    print("测试用例test_02")
    time.sleep(1)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_1_baidu.py"])


# web_conf_py/baidu/test_2.py
import pytest
import time

def test_06(start, open_baidu):
    print("测试用例test_01")
    time.sleep(1)
    assert start == "yoyo"
def test_07(start, open_baidu):
    print("测试用例test_02")
    time.sleep(1)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_2.py"])


# web_conf_py/blog/conftest.py
import pytest

@pytest.fixture(scope="function")
def open_blog():
    print("打开blog页面_function")

# web_conf_py/blog/test_2_blog.py

import pytest
import time
def test_03(start, open_blog):
    print("测试用例test_03")
    time.sleep(1)
    assert start == "yoyo"

def test_04(start, open_blog):
    print("测试用例test_04")
    time.sleep(1)
    assert start == "yoyo"

def test_05(start, open_blog):
    '''跨模块调用baidu模块下的conftest'''
    print("测试用例test_05,跨模块调用baidu")
    time.sleep(1)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_2_blog.py"])
```

1. 正常运行:耗时7秒
```
pytest
```

2. 并行运行:耗时不到4秒
```
pytest -n 3
```

3. 测试报告

```
pytest -n 3 --html=report.html --self-contained-html
```