#!/usr/bin/env python

import argparse
from runcore import config_paths
config_paths()

from core.django_external_setup import django_external_setup
from testing import critical, traffic_test


def main(iface):
    django_external_setup()
    load_test = traffic_test.NormalTrafficTest()
    threat_test = critical.HostThreatTest(iface)
    whitelist_test = critical.HostThreatTestWhitelist(iface)
    whitelist_test.perform_test()
    threat_test.perform_test()



if __name__ == '__main__':
    # TODO add file logger
    parser = argparse.ArgumentParser()
    parser.add_argument('interface')
    args = parser.parse_args()
    main(args.interface)
