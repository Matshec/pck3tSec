import time
from typing import Optional
import requests
import logging
import threading
import subprocess
import socket
from runcore import prepare_app
from rest_framework import status
from abc import ABC, abstractmethod
from django.test import TestCase
from rest.models import Host, Threat, ManageList
import django.test.utils as dutils
from rest.enum_classes import *
from django.core.management import execute_from_command_line

logger = logging.getLogger()


class CriticalTest(ABC, TestCase):

    class AppThread(threading.Thread):

        def __init__(self, iface):
            super().__init__()
            self.dispatcher = prepare_app(iface)

        def run(self):
            self.dispatcher.run()

        def join(self, *args) -> None:
            self.dispatcher.finish()
            super().join(*args)

    def __init__(self, iface):
        TestCase.__init__(self)
        self.app_thread = self.AppThread(iface)

    def start_app_threat(self):
        self.app_thread.start()

    def stop_app_threat(self):
        self.app_thread.join()

    def _wait_for_live_app(self, timeout=15):
        t0 = time.time()
        while not self.app_thread.dispatcher.active:
            time.sleep(0.2)
            if time.time() - t0 > timeout:
                raise TimeoutError

    @abstractmethod
    def test(self):
        pass

    def pre_test(self):
        dutils.setup_test_environment()
        old_conf = dutils.setup_databases(1, False, aliases='default')
        self.start_app_threat()
        self._wait_for_live_app()
        return old_conf

    def post_test(self, conf):
        self.stop_app_threat()
        # flush database with django
        execute_from_command_line(['scriptname', 'flush', '--noinput'])
        dutils.teardown_databases(conf, 1)
        dutils.teardown_test_environment()
        subprocess.run(['/sbin/iptables', '-F', 'INPUT'])
        subprocess.run(['/sbin/iptables', '-F', 'OUTPUT'])

    def perform_test(self):
        db_conf = self.pre_test()
        try:
            self.test()
        finally:
            self.post_test(db_conf)

class HostThreatTest(CriticalTest):

    def __init__(self, iface):
        # does not see https - only http ( because of paths)
        self.test_url = "http://testsafebrowsing.appspot.com/s/malware.html"
        super().__init__(iface)

    def test(self):
        logger.info("running host threat rest")
        res = requests.get(self.test_url)
        assert res.status_code == 200, "request fail"
        # wait to process request by app
        time.sleep(4)
        query = Threat.objects.filter(http_path=self.test_url[7:])
        self.assertTrue(query.exists())
        logger.info("threat object is {}".format(query.get().__dict__))
        with self.assertRaises(requests.exceptions.ConnectionError):
            requests.get(self.test_url)
        logger.info("Threat test passed")


class HostThreatTestWhitelist(CriticalTest):

    def __init__(self, iface):
        self.test_url = "http://testsafebrowsing.appspot.com/s/malware.html"
        super().__init__(iface)

    def hostname_to_ip(self, name) -> Optional[str]:
        try:
            return socket.gethostbyname(name)
        except socket.gaierror:
            pass

    def _setup_db(self):
        host = Host.objects.create(**{
            'fqd_name': 'testsafebrowsing.appspot.com',
            'original_ip': self.hostname_to_ip('testsafebrowsing.appspot.com'),
        })
        ManageList.objects.create(**{
            'host': host,
            'reason': 'some',
            'color': ListColor.WHITE.value
        })

    def test(self):
        logger.info('running test whitelist')
        self._setup_db()
        res = requests.get(self.test_url)
        assert res.status_code == status.HTTP_200_OK, 'request failed, no point testing'
        time.sleep(4)
        query = Threat.objects.filter(http_path=self.test_url[7:])
        self.assertTrue(query.exists())
        logger.info("threat object is {}".format(query.get().__dict__))
        res1 = requests.get(self.test_url)
        self.assertEqual(status.HTTP_200_OK, res1.status_code)
