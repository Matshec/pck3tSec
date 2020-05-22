import unittest
import logging
from core.django_external_setup import django_external_setup
from scapy.all import *
from scapy.layers import http
from unittest.mock import patch, call

django_external_setup()
from core.stat_analyzer import StatAnalyzer

logging.disable(logging.CRITICAL)


class StatAnalyzerTests(unittest.TestCase):

    MOCK_PACKET = Ether()/ IP(dst='1.1.1.1')/ TCP() / http.HTTPRequest(Host='one.one')

    def setUp(self) -> None:
        self.analyzer = None

    def tearDown(self) -> None:
        self.analyzer.finish()

    def test_analyze(self):
        with patch.object(StatAnalyzer, '_handle_db_save') as db_save:
            self.analyzer = StatAnalyzer()
            self.analyzer.analyze(self.MOCK_PACKET)
            self.analyzer.db_cache.flush()
            db_save.assert_called()
            self.assertEqual(call('one.one', '1.1.1.1'), db_save.call_args)
