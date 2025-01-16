import ast
import unittest

from lxc_ext.lib.atoms.service import fssize


class TestParseSize(unittest.TestCase):

    def test_valid_si_units(self):
        self.assertEqual(fssize.get("5M"), 5000000)
        self.assertEqual(fssize.get("5 MB"), 5000000)
        self.assertEqual(fssize.get("2G"), 2000000000)
        self.assertEqual(fssize.get("2 GB"), 2000000000)

    def test_valid_iec_units(self):
        self.assertEqual(fssize.get("1MiB"), 2**20)
        self.assertEqual(fssize.get("1 MiB"), 2**20)
        self.assertEqual(fssize.get("1GiB"), 2**30)
        self.assertEqual(fssize.get("1 GiB"), 2**30)
        self.assertEqual(fssize.get("1024 MiB"), 2**30)

    def test_case_insensitivity(self):
        self.assertEqual(fssize.get("1mb"), 10**6)
        self.assertEqual(fssize.get("1gib"), 2**30)
        self.assertEqual(fssize.get("1 MB"), 10**6)
        self.assertEqual(fssize.get("1 GiB"), 2**30)

    def test_with_spaces(self):
        self.assertEqual(fssize.get(" 5M "), 5000000)
        self.assertEqual(fssize.get("   2 GiB  "), 2*2**30)

    def test_invalid_units(self):
        with self.assertRaises(ValueError):
            fssize.get("5 XB")
        with self.assertRaises(ValueError):
            fssize.get("5 KB")
        with self.assertRaises(ValueError):
            fssize.get("5 XYZ")

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            fssize.get("abc")
        with self.assertRaises(ValueError):
            fssize.get("5MB5")
        with self.assertRaises(ValueError):
            fssize.get("")

    def test_default_to_bytes(self):
        with self.assertRaises(ValueError):  # Since no unit and 'b' isn't defined
            fssize.get("500")

    def test_edge_cases(self):
        self.assertEqual(fssize.get("0M"), 0)
        self.assertEqual(fssize.get("0 MiB"), 0)
        with self.assertRaises(ValueError):
            fssize.get("-5M")  # Negative size should not be valid

if __name__ == '__main__':
    unittest.main()
