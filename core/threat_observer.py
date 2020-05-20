import logging
from django.utils import timezone
from core.abstracts import IObserver
from core.django_external_setup import django_external_setup
from rest.enum_classes import ThreatType, ListColor
from typing import Dict

django_external_setup()
from rest.models import Host, Threat, ManageList
from rest.host_blocker import HostBlocker
logger = logging.getLogger()


class ThreatObserver(IObserver):
    def __init__(self):
        self.blocker = HostBlocker()

    def update(self, host: str, threat_details: Dict, ip: str):
        http_path = host if '/' in host else ""
        host_name = host.split('/')[0]
        host_db, created = Host.objects.get_or_create(fqd_name=host_name, original_ip=ip) # is_threat=True

        db_threat = Threat(
            threat_type=ThreatType.HOST.value,
            threat_details=threat_details or "no details",
            http_path=http_path,
            discovered=timezone.now(),
            host_source=host_db
        )
        self._save_if_not_doubled(db_threat, host_db)

    def _save_if_not_doubled(self, threat: Threat, source_host: Host):
        query = Threat.objects.filter(threat_type=ThreatType.HOST.value, host_source=source_host.id)
        if query.exists():
            logger.info("Such threat entry already exists")
        else:
            self._block_host(source_host)
            threat.save()
            logger.info("Threat saved in database")
        source_host.is_threat = True
        source_host.save()

    def _block_host(self, host: Host):
        if not self._whitelisted(host):
            self.blocker.block_host(host.original_ip)
            logger.info('Host blocked')
        else:
            logger.info(f"Host {host.fqd_name} is whitelisted not blocking")

    def _whitelisted(self, host):
        return ManageList.objects.filter(color=ListColor.WHITE.value, host=host).exists()