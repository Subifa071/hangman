"""
This tests name and contact number by using pytest.
"""
import pytest
@pytest.fixture
def tester():
    name = "Jack"
    contact = 9803452929
    return [name, contact]

def testing_1(tester):
    first_name = "Jack"
    assert tester[0] == first_name

def testing_2(tester):

    contact_num = 9003452929
    assert tester[1] == contact_num
