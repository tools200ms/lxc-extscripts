import unittest
import sys

from lxc_extrpy import *

class ExtrPy(unittest.TestCase):
    def test_extr_DKMI(self):
        with open('./tests/selector-test.txt') as file:
            selector, value, comment = extractDKMITxt(file.read())

        self.assertEqual(selector, "selector-test._domainkey")
        self.assertEqual(value, "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2HsdfX/iBgLEDVRjXtwECUVtg6FHO6lAb11AaXC58jLDgP/iP5iCxd4VVPu5bI72/rM7syC7q7KA0+1dPGPlSlenp9yQjKDhx+qers+adAg7dMYt2zDJdktEaGhMf0EQB48+htrgqMI245OWEOC+f3RNi39nKZ1NtOTXv/FzOqu5Ha3ioaxQGWrh61XJajLz819GNN9dgkAILZZ2tTb8Cb06/hv1ZhyvFjZa2jtLhEvQng9uH6rRKBQOzy0Ic8n0/WEJg8yHy5FI/A5911xF+IvWw9Ycb1E092HujmNaTZVhQspm6OPFWcBgO2QATD6XRXl9CURmGyAqKK255C5l0wIDAQAB")
        self.assertEqual(comment, "DKIM key selector-test for example.com")

    def test_extr_DKMI_broken(self):

        with self.assertRaises(ValueError) as context:
            with open('./tests/selector-test-broken.txt') as file:
                selector, value, comment = extractDKMITxt(file.read())

        self.assertTrue("Inappropriate selector: selector-tes_t._domainkey" in str(context.exception))

