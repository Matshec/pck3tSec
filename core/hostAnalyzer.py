from googleSafeBrowsing import GoogleSafeBrowsing
from scapy.layers import http, inet
from analyzerBase import AnalyzerBase
from scapy.all import conf
from typing import Optional
import socket
import logging


logger = logging.getLogger()


class HostAnalyzer(AnalyzerBase):
    """
    for now we are onyl considering destination hosts for ip packets and
    host/path for http layer
    """

    def __init__(self, google_safe: GoogleSafeBrowsing):
        self.safe_browsing = google_safe
        self.own_interfaces = self._get_own_interfaces()

    def _get_own_interfaces(self) -> list:
        """
        get interface with ips for that which has gateway
        :return: list of ips of this machine that have gateways
        """
        ifaces = conf.route.routes
        own_ifaces = [x[4] for x in ifaces if x[2] != '0.0.0.0']
        return own_ifaces

    @staticmethod
    def resolve_ip_to_hostname(ips: str) -> str:
        return socket.gethostbyaddr(ips)[0]

    def _get_ip_of_foreign_host(self, ip: inet.IP) -> Optional[str]:
        if ip.dst not in self.own_interfaces:
            return ip.dst

    def _handle_ip_layer(self, packet) -> Optional[str]:
        ip_packet = packet.getlayer(inet.IP)
        dst_host = self._get_ip_of_foreign_host(ip_packet)
        if dst_host:
            hostname = self.resolve_ip_to_hostname(dst_host)
            return hostname

    def _handle_http_layer(self, packet) -> Optional[str]:
        http_packet = packet.getlayer(http.HTTPRequest)
        host_path = f"{http_packet.Host}{http_packet.Path}"
        return host_path

    def analyze(self, packet):
        # TODO make it not return and comm with database
        host = None
        try:
            if packet.haslayer(http.HTTPRequest):
                host = self._handle_http_layer(packet)
            elif packet.haslayer(inet.IP):
                host = self._handle_ip_layer(packet)
            if host:
                return self.safe_browsing.api_call([host])
        except Exception:
            logger.exception(f"failed to check host for packet {packet.show}")
