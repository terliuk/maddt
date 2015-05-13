"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


from ConfigParser import ConfigParser
import gridftpcopy 


try:
    from django.test import TestCase
except ImportError:
    from unittest import TestCase
    print ("Can not load django, using unittest instead")



class ConfigTest(TestCase):

    def test_is_configparser(self):


        cfg = gridftpcopy.configure()
        self.assertIsInstance(cfg,ConfigParser)

    def test_configfiler_read(self):


        cfg = gridftpcopy.configure()
        self.assertTrue(len(cfg.sections()))

class CheckVomsProxyTest(TestCase):

    def test_is_None(self):

        result = gridftpcopy.check_voms_proxy()
        self.assertIsNone(result)

class ChecksumCompareTest(TestCase):

    def test_is_equal(self):

        success = gridftpcopy.compare_checksums("R2:D2:C3:PO", "R2:D2:C3:PO")
        self.assertTrue(success)

    def test_is_not_equal(self):

        failed = gridftpcopy.compare_checksums("NC:C1:70:1A", "NC:C1:70:1B")
        self.assertFalse(failed)


class TokenTest(TestCase):

    def test_is_none(self):
        self.assertIsNone(gridftpcopy.get_afs_token())

class GetFileTest(TestCase):
        pass
    



if __name__ == '__main__':

    import unittest
    unittest.main()
