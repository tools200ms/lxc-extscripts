import unittest
import ipaddress

from lxcext.lib.atoms.network import ip_range


class TestParseIpRangeAddress(unittest.TestCase):

    def test_valid_ipv4_cidr(self):
        result = ip_range.get("192.168.1.0/24")
        self.assertIsInstance(result, ipaddress.IPv4Network)
        self.assertEqual(str(result), "192.168.1.0/24")

    def test_valid_ipv6_cidr(self):
        result = ip_range.get("2001:db8::/32")
        self.assertIsInstance(result, ipaddress.IPv6Network)
        self.assertEqual(str(result), "2001:db8::/32")

    def test_valid_ipv4_range(self):
        result = ip_range.get("192.168.1.1-192.168.1.10")
        self.assertIsInstance(result[0], ipaddress.IPv4Address)
        self.assertIsInstance(result[1], ipaddress.IPv4Address)
        self.assertEqual(str(result[0]), "192.168.1.1")
        self.assertEqual(str(result[1]), "192.168.1.10")

    def test_valid_ipv6_range(self):
        result = ip_range.get("2001:db8::1-2001:db8::10")
        self.assertIsInstance(result[0], ipaddress.IPv6Address)
        self.assertIsInstance(result[1], ipaddress.IPv6Address)
        self.assertEqual(str(result[0]), "2001:db8::1")
        self.assertEqual(str(result[1]), "2001:db8::10")

    def test_invalid_iprange(self):
        with self.assertRaises(ValueError):
            ip_range.get("192.168.1.10-192.168.1.1")  # Invalid range

    def test_invalid_iprange_format(self):
        with self.assertRaises(ValueError):
            ip_range.get("192.168.1.10-192.168.1")  # Invalid format

    def test_invalid_iprange_mixed_types(self):
        with self.assertRaises(ValueError):
            ip_range.get("192.168.1.1-2001:db8::1")  # Mixed IPv4 and IPv6

    def test_invalid_cidr(self):
        with self.assertRaises(ValueError):
            ip_range.get("192.168.1.0/33")  # Invalid CIDR prefix

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            ip_range.get("")  # Empty string

if __name__ == '__main__':
    unittest.main()
