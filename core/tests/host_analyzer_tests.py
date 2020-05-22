import unittest
from unittest.mock import patch


class HostAnalyzerTest(unittest.TestCase):

    @patch('GoogleSafeBrowsing', '')
    def test_is_host_safe(self, gsafe):
        gsafe.ap