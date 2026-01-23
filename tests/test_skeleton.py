import unittest
from aic.skeleton import PythonSkeletonizer

class TestSkeletonizer(unittest.TestCase):
    def setUp(self):
        self.skeletonizer = PythonSkeletonizer()

    def test_basic_function(self):
        source = '''
def hello(name: str) -> str:
    """Greets the user."""
    return f"Hello, {name}"
'''
        skeleton, deps = self.skeletonizer.skeletonize(source, "test.py")
        self.assertIn("def hello(name: str) -> str:", skeleton)
        self.assertIn('"""Greets the user."""', skeleton)
        self.assertIn("RETURNS: f'Hello, {name}'", skeleton)
        self.assertIn("...", skeleton)

    def test_class_skeleton(self):
        source = '''
class MyClass:
    """A test class."""
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
'''
        skeleton, deps = self.skeletonizer.skeletonize(source, "test.py")
        self.assertIn("class MyClass:", skeleton)
        self.assertIn('"""A test class."""', skeleton)
        self.assertIn("def __init__(self, value):", skeleton)
        self.assertIn("def get_value(self):", skeleton)

if __name__ == "__main__":
    unittest.main()

