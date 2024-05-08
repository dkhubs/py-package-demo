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
