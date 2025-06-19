# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.
import os

import pytest
from pytest_operator.plugin import OpsTest


@pytest.fixture
def ubuntu_base():
    """Charm base version to use for testing."""
    return os.environ["CHARM_UBUNTU_BASE"]


@pytest.fixture
def series(ubuntu_base):
    """Workaround: python-libjuju does not support deploy base="ubuntu@22.04"; use series."""
    if ubuntu_base == "22.04":
        return "jammy"
    elif ubuntu_base == "24.04":
        return "noble"
    else:
        raise NotImplementedError


@pytest.fixture
async def charm(ops_test: OpsTest, series):
    """Kafka charm used for integration testing."""
    bases_index = 0 if series == "jammy" else 1
    charm = await ops_test.build_charm(".", bases_index=bases_index)
    return charm
