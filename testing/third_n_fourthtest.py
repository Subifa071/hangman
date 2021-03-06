"""
This tests username and password from login page by using pytest.
"""
import pytest

@pytest.mark.parametrize("username, password", [("admin", "admin"), ("admin", "John")])
def test_method(username, password):
    assert username == password
