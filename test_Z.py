
from Z import *

def test_empty():
    assert True

hello = Object('hello')

def test_hello():
    assert Object('hello').test() == '\n<object:hello>'

world = Object('world')

def test_world():
    assert world.test() == '\n<object:world>'