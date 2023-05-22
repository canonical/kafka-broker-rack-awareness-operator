#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

https://discourse.charmhub.io/t/4208
"""

import logging
import shutil

from charms.operator_libs_linux.v1 import snap
from ops.charm import CharmBase
from ops.framework import EventBase
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus
from utils import safe_write_to_file

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)


class KafkaBrokerRackAwarenessCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_install(self, event: EventBase):
        """Handle on install event."""
        cache = snap.SnapCache()
        charmed_kafka = cache["charmed-kafka"]

        # The charm should be deployed
        if not charmed_kafka.present:
            self.unit.status = BlockedStatus(
                "Charmed Kafka missing in the unit. Please deploy the charm in machines along with Kafka"
            )
            event.defer()
            return

        self.unit.status = ActiveStatus()

    def _on_config_changed(self, event):
        """Handle config changed event."""
        if not isinstance(self.unit.status, ActiveStatus):
            event.defer()
            return
        broker_rack = self.config.get("broker-rack")
        if broker_rack is None:
            self.unit.status = BlockedStatus("broker-rack config missing, please set a value") 

        content = f"broker.rack={broker_rack}"
        rack_properties_file = "/var/snap/charmed-kafka/current/etc/kafka/rack.properties"

        safe_write_to_file(content=content, path=rack_properties_file)

        # Normalize file to have same owner as kafka charm files
        shutil.chown(rack_properties_file, user="snap_daemon", group="root")


if __name__ == "__main__":  # pragma: nocover
    main(KafkaBrokerRackAwarenessCharm)
