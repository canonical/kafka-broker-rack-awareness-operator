# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import logging
from pathlib import Path
from unittest.mock import PropertyMock, patch

import pytest
import yaml
from ops.model import BlockedStatus
from ops.testing import Harness

from charm import KafkaBrokerRackAwarenessCharm

logger = logging.getLogger(__name__)

METADATA = str(yaml.safe_load(Path("./metadata.yaml").read_text()))


@pytest.fixture
def harness():
    harness = Harness(KafkaBrokerRackAwarenessCharm, meta=METADATA)
    harness.begin()
    return harness


def test_install_with_kafka(harness: Harness):
    with patch(
        "charm.KafkaBrokerRackAwarenessCharm.kafka_installed",
        new_callable=PropertyMock,
        return_value=True,
    ):
        harness.charm.on.install.emit()

    assert harness.charm.unit.status == BlockedStatus(
        "broker-rack config missing, please set a value"
    )


def test_install_without_kafka(harness: Harness):
    with patch(
        "charm.KafkaBrokerRackAwarenessCharm.kafka_installed",
        new_callable=PropertyMock,
        return_value=False,
    ):
        harness.charm.on.install.emit()

    assert harness.charm.unit.status == BlockedStatus(
        "Charmed Kafka missing in the unit. Please deploy the charm in machines along with Kafka"
    )


@pytest.mark.parametrize(
    "version_id, expected_user",
    [
        ("22.04", "snap_daemon"),
        ("24.04", "_daemon_"),
    ],
)
def test_config_changed_valid(harness: Harness, version_id, expected_user):
    with (
        patch(
            "charm.KafkaBrokerRackAwarenessCharm.kafka_installed",
            new_callable=PropertyMock,
            return_value=True,
        ),
        patch("charm.safe_write_to_file", return_value=None) as patched_write,
        patch("charm.shutil.chown", return_value=None) as patched_chown,
        patch("charm.platform.freedesktop_os_release", return_value={"VERSION_ID": version_id}),
    ):
        harness.update_config(key_values={"broker-rack": "us-west"})

        patched_write.assert_called_with(
            content="broker.rack=us-west",
            path="/var/snap/charmed-kafka/current/etc/kafka/rack.properties",
        )
        patched_chown.assert_called_with(
            "/var/snap/charmed-kafka/current/etc/kafka/rack.properties",
            user=expected_user,
            group="root",
        )


def test_config_changed_invalid(harness: Harness):
    # Install check fails and the unit is Blocked
    harness.charm.unit.status = BlockedStatus()
    with (
        patch("ops.framework.EventBase.defer") as patched_defer,
        patch("charm.safe_write_to_file", return_value=None) as patched_write,
        patch("charm.shutil.chown", return_value=None) as patched_chown,
    ):
        harness.update_config(key_values={"broker-rack": "us-west"})

        patched_write.assert_not_called()
        patched_chown.assert_not_called()
        patched_defer.assert_called()
