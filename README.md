# py-package-demo
Standard python packages

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