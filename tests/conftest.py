import pytest

def pytest_collection_modifyitems(session, items):
    print(type(items))
    print('收集到的测试用例: %s' % items)
    
    # sort 排序, 根据用例名称 item.name 排序
    items.sort(key=lambda item: item.name)
    print('排序后的用例: %s' % items)
    for item in items:
        print('用例名称: %s' % item.name)