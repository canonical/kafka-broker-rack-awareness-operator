#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

import logging
from pathlib import Path

import pytest
import yaml
from pytest_operator.plugin import OpsTest

logger = logging.getLogger(__name__)

METADATA = yaml.safe_load(Path("./metadata.yaml").read_text())
APP_NAME = METADATA["name"]


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test: OpsTest, series, charm):
    """Build the charm-under-test and deploy it together with related charms.

    Assert on the unit status before any relations/configurations take place.
    """
    # Deploy the charm and wait for active/idle status
    if series == "jammy":
        kafka_channel = "3/edge"
    elif series == "noble":
        kafka_channel = "4/edge"

    await ops_test.model.deploy(
        "kafka",
        channel=kafka_channel,
        application_name="kafka",
        num_units=1,
    )
    await ops_test.model.wait_for_idle(
        apps=["kafka"], status="blocked", idle_period=50, timeout=1000
    )
    machine_ids = await ops_test.model.get_machines()

    logger.info(f"Using charm built for {series} series: {charm}")
    await ops_test.model.deploy(
        charm,
        application_name=APP_NAME,
        series=series,
        to=machine_ids[0],
        config={"broker-rack": "integration-zone"},
    )
    await ops_test.model.wait_for_idle(apps=[APP_NAME], idle_period=50, timeout=1000)

    assert ops_test.model.applications[APP_NAME].status == "active"
