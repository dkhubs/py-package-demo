# pytest测试框架

### 安装
```
pip install pytest
```

### 用例设计原则

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

### 前置(setup)和后置(teardown)

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

### fixture:自定义测试用例的预置条件

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

### conftest.py配置

单独管理预置的操作场景, pytest默认读取conftest.py里面的配置。注意事项:

- conftest.py 配置脚本名称是固定的, 不能改名称

- conftest.py 与运行的用例要在同一个 package 下, 并且有 __init__.py 文件

- 不需要 import 导入 conftest.py, pytest 用例会自动查找

### pytest生成html报告

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

### 参数化

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

### 命令行传参

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