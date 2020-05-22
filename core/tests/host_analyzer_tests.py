import unittest
from unittest.mock import patch, MagicMock
from core.google_safe_browsing import GoogleSafeBrowsing
from core.host_analyzer import HostAnalyzer
from scapy.all import *
from scapy.layers import http


class HostAnalyzerTest(unittest.TestCase):

    MOCK_PACKET = Ether()/ IP(dst='1.1.1.1')/ TCP() / http.HTTPRequest(Host='one.one')

    def setUp(self) -> None:
        gsafe = MagicMock()
        gsafe.api_call = MagicMock(return_value=(False, ""))
        self.analyzer = HostAnalyzer(gsafe)

    def tearDown(self) -> None:
        self.analyzer.finish()

    def test_analyze(self):
        mock_notify = MagicMock()
        self.analyzer.notify = mock_notify
        self.analyzer.analyze(self.MOCK_PACKET)
        mock_notify.assert_called()
