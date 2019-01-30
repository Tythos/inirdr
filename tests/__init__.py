"""Suite of test cases for inirdr package/module
"""

import os
import sys
import unittest
import inirdr

TEST_PATH, _ = os.path.split(os.path.abspath(__file__))

class ConfigTests(unittest.TestCase):
    """Verifies loading of config1.ini
    """

    def setUp(self):
        """Load for comparison in individual tests
        """
        with open(TEST_PATH + "/config1.ini", 'r') as f:
            self.config = inirdr.read(f)

    def test_sections(self):
        """Check fields
        """
        expected = ["one", "two"]
        actual = list(self.config.keys())
        self.assertEqual(expected, actual)

    def test_one(self):
        """Check contents of section one
        """
        expected = {
            "lorem": "ipsum",
            "dolor": 1,
            "sit": True
        }
        actual = self.config["one"]
        self.assertEqual(expected, actual)

    def test_two(self):
        """Check contents of section two
        """
        expected = {
            "amet": "consectetur",
            "adipiscing": 2,
            "elit": False
        }
        actual = self.config["two"]
        self.assertEqual(expected, actual)

class Config2Tests(unittest.TestCase):
    """Verifies loading of config2.ini
    """

    def setUp(self):
        """Load for comparison in individual tests
        """
        with open(TEST_PATH + "/config2.ini", 'r') as f:
            self.config = inirdr.read(f)

    def test_sections(self):
        """Check fields
        """
        expected = ["two", "three"]
        actual = list(self.config.keys())
        self.assertEqual(expected, actual)

    def test_two(self):
        """Check contents of section two
        """
        expected = {
            "amet": "nunc",
            "varius": 3,
        }
        actual = self.config["two"]
        self.assertEqual(expected, actual)

    def test_three(self):
        """Check contents of section three
        """
        expected = {
            "pharetra": "libero"
        }
        actual = self.config["three"]
        self.assertEqual(expected, actual)

class UtilityTests(unittest.TestCase):
    """Verifies other utility functions in inirdr
    """

    def setUp(self):
        """Load config1 and config2 for use in individual tests
        """
        with open(TEST_PATH + "/config1.ini", 'r') as f:
            self.config1 = inirdr.read(f)
        with open(TEST_PATH + "/config2.ini", 'r') as f:
            self.config2 = inirdr.read(f)

    def test_update(self):
        """Verify update() function
        """
        config3 = inirdr.update(self.config1, self.config2)
        sections = list(config3.keys())
        self.assertEqual(sections, ["one", "two", "three"])
        self.assertEqual(config3["one"], {
            "lorem": "ipsum",
            "dolor": 1,
            "sit": True
        })
        self.assertEqual(config3["two"], {
            "amet": "nunc",
            "adipiscing": 2,
            "elit": False,
            "varius": 3
        })
        self.assertEqual(config3["three"], {
            "pharetra": "libero"
        })

    def test_table(self):
        """Verify toTable() function
        """
        table = inirdr.toTable(self.config2)
        self.assertEqual(table[0], {
            "section": "two",
            "field": "amet",
            "value": "nunc"
        })
        self.assertEqual(table[1], {
            "section": "two",
            "field": "varius",
            "value": 3
        })
        self.assertEqual(table[2], {
            "section": "three",
            "field": "pharetra",
            "value": "libero"
        })

if __name__ == "__main__":
    if "--verbose" not in sys.argv:
        sys.argv.append("--verbose")
    unittest.main()
