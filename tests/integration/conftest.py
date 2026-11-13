# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.
import glob
import os
import platform

import pytest


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
def arch() -> str:
    """Fixture to provide the platform architecture for testing."""
    platforms = {
        "x86_64": "amd64",
        "aarch64": "arm64",
    }
    return platforms.get(platform.machine(), "amd64")


@pytest.fixture(scope="module")
async def charm(ubuntu_base, arch):
    """Kafka charm used for integration testing."""
    files = glob.glob(f"*{ubuntu_base}-{arch}.charm")
    if not files:
        raise FileNotFoundError

    return f"./{files[0]}"
