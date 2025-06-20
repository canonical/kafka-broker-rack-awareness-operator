#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charmed Machine Operator for Rack Awareness in Kafka Broker."""

import logging
import platform
import shutil

from charms.operator_libs_linux.v2 import snap
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus, StatusBase

from utils import safe_write_to_file

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)


class KafkaBrokerRackAwarenessCharm(CharmBase):
    """Charmed Rack Awareness for Kafka Broker."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    @property
    def kafka_installed(self) -> bool:
        """Check if kafka snap is installed."""
        cache = snap.SnapCache()
        charmed_kafka = cache["charmed-kafka"]

        return charmed_kafka.present

    @property
    def rack_properties_file(self) -> str:
        """Return the path to the rack properties file."""
        return "/var/snap/charmed-kafka/current/etc/kafka/rack.properties"

    @property
    def kafka_snap_username(self) -> str:
        """Return the username for the Kafka snap."""
        user = "snap_daemon"
        if platform.freedesktop_os_release()["VERSION_ID"] == "24.04":
            user = "_daemon_"

        return user

    def _on_install(self, _):
        """Handle on install event."""
        self.unit.status = self._get_status()

    def _on_config_changed(self, event):
        """Handle config changed event."""
        self.unit.status = self._get_status()
        if not isinstance(self.unit.status, ActiveStatus):
            event.defer()
            return

        broker_rack = self.config.get("broker-rack")
        content = f"broker.rack={broker_rack}"

        safe_write_to_file(content=content, path=self.rack_properties_file)

        # Normalize file to have same owner as kafka charm files
        shutil.chown(self.rack_properties_file, user=self.kafka_snap_username, group="root")

    def _get_status(self) -> StatusBase:
        """Return the current application status."""
        if not self.kafka_installed:
            return BlockedStatus(
                "Charmed Kafka missing in the unit. Please deploy the charm in machines along with Kafka"
            )
        if not self.config.get("broker-rack"):
            return BlockedStatus("broker-rack config missing, please set a value")

        return ActiveStatus()


if __name__ == "__main__":  # pragma: nocover
    main(KafkaBrokerRackAwarenessCharm)
