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