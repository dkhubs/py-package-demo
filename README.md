# py-package-demo
Standard python packages

#### [pytest测试框架](https://www.cnblogs.com/yoyoketang/tag/pytest/)

#### 执行用例, 生成报告命令
```
pytest --html=report.html --self-contained-html
```

#### pytest用例规则

- 文件名以test_*.py文件和*_test.py

- 以test_开头的函数

- 以Test开头的类，test_开头的方法，并且不能带有__init__ 方法

- 所有的包pakege必须要有__init__.py文件

- 断言使用assert

#### 打包
```
py -m pip install --upgrade build
py -m build
```

#### 上传包到pypi
```
py -m pip install --upgrade twine
py -m twine upload --repository testpypi dist/*
```

#### 安装新包
```
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps example_package_dkhubs

py

from example_package_YOUR_USERNAME_HERE import example
example.add_one(2)
```