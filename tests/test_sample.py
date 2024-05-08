import pytest

def testanswer(cmdopt):
    if cmdopt == 'type1':
        print('first')
    elif cmdopt == 'type2':
        print('second')
    assert 0
    
if __name__ == '__main__':
    pytest.main(['-s', 'test_sample.py'])