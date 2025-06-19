# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.
import os

import pytest
from pytest_operator.plugin import OpsTest


@pytest.fixture(scope="module")
def ubuntu_base():
    """Charm base version to use for testing."""
    return os.environ["CHARM_UBUNTU_BASE"]


@pytest.fixture(scope="module")
def series(ubuntu_base):
    """Workaround: python-libjuju does not support deploy base="ubuntu@22.04"; use series."""
    if ubuntu_base == "22.04":
        return "jammy"
    elif ubuntu_base == "24.04":
        return "noble"
    else:
        raise NotImplementedError


@pytest.fixture(scope="module")
async def charm(ops_test: OpsTest, ubuntu_base):
    """Kafka charm used for integration testing."""
    charm_paths = await ops_test.build_charm(".", return_all=True)
    for p in charm_paths:
        if ubuntu_base in str(p):
            return p
    raise FileNotFoundError
