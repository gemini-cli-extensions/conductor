import unittest
from aic.skeleton import TypeScriptSkeletonizer, GoSkeletonizer

class TestMultiLangSkeletonizer(unittest.TestCase):
    def test_typescript_skeleton(self):
        ts_code = """
import { Request, Response } from 'express';
import * as fs from 'fs';

/**
 * Interface for User
 */
export interface User {
    id: number;
    name: string;
}

async function getUser(id: number): Promise<User> {
    const user = await db.find(id);
    return user;
}
"""
        skel = TypeScriptSkeletonizer()
        skeleton, deps = skel.skeletonize(ts_code, "test.ts")
        self.assertIn("'express'", str(deps))
        self.assertIn("'fs'", str(deps))
        self.assertIn("interface User { ... }", skeleton)
        self.assertIn("async function getUser(id: number): Promise<User> { ... }", skeleton)
        self.assertIn("Interface for User", skeleton)

    def test_go_skeleton(self):
        go_code = """
package main

import (
    "fmt"
    "net/http"
)

// Greeter interface
type Greeter interface {
    Greet() string
}

func main() {
    fmt.Println("Hello")
}
"""
        skel = GoSkeletonizer()
        skeleton, deps = skel.skeletonize(go_code, "test.go")
        self.assertIn("fmt", deps)
        self.assertIn("net/http", deps)
        self.assertIn("package main", skeleton)
        self.assertIn("type Greeter interface { ... }", skeleton)
        self.assertIn("func main() { ... }", skeleton)
        self.assertIn("// Greeter interface", skeleton)

if __name__ == "__main__":
    unittest.main()
