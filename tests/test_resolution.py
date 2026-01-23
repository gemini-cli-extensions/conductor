import unittest
import os
import shutil
import tempfile
from aic.utils import resolve_dep_to_path

class TestResolution(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Create a mock project structure
        # /pkg1/__init__.py
        # /pkg1/mod1.py
        # /pkg2/mod2.py
        # /ts/index.ts
        # /go/main.go
        os.makedirs(os.path.join(self.test_dir, "pkg1"))
        os.makedirs(os.path.join(self.test_dir, "pkg2"))
        os.makedirs(os.path.join(self.test_dir, "ts"))
        os.makedirs(os.path.join(self.test_dir, "go"))
        
        with open(os.path.join(self.test_dir, "pkg1", "__init__.py"), "w") as f: f.write("")
        with open(os.path.join(self.test_dir, "pkg1", "mod1.py"), "w") as f: f.write("")
        with open(os.path.join(self.test_dir, "pkg2", "mod2.py"), "w") as f: f.write("")
        with open(os.path.join(self.test_dir, "ts", "index.ts"), "w") as f: f.write("")
        with open(os.path.join(self.test_dir, "go", "utils.go"), "w") as f: f.write("")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_python_relative(self):
        # From pkg1/mod1.py, import ..pkg2.mod2
        res = resolve_dep_to_path("..pkg2.mod2", "pkg1/mod1.py", self.test_dir)
        self.assertEqual(res, "pkg2/mod2.py")

    def test_python_absolute(self):
        # From pkg1/mod1.py, import pkg2.mod2
        res = resolve_dep_to_path("pkg2.mod2", "pkg1/mod1.py", self.test_dir)
        self.assertEqual(res, "pkg2/mod2.py")

    def test_typescript_index(self):
        res = resolve_dep_to_path("./ts", "main.ts", self.test_dir)
        self.assertEqual(res, "ts/index.ts")

    def test_go_package(self):
        res = resolve_dep_to_path("go", "main.go", self.test_dir)
        self.assertEqual(res, "go/utils.go")

if __name__ == "__main__":
    unittest.main()
