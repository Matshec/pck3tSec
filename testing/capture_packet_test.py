import json
import logging
import pprint
import time

import scapy.utils

# from scapy.layers import http
from scapy.layers import http

from core.packet_reader import PacketReader

logger = logging.getLogger()

packet_reader = PacketReader(None)
packet_reader.sniff()

time.sleep(5)
packets = packet_reader.get_packets()
json_data = json.load(scapy.utils.tcpdump(pktlist=packets, prog=conf.prog.tshark, args=["-T", "json"], getfd=True))
pprint.pprint(json_data)

# for packet in packets:
#     scapy.utils.tcpdump(packet)
#     packet.show()
packet_reader.end()