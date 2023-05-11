#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Collection of helper methods."""

import logging
import os

logger = logging.getLogger(__name__)


def safe_write_to_file(content: str, path: str, mode: str = "w") -> None:
    """Ensure destination filepath exists before writing.

    Args:
        content: the content to be written to a file
        path: the full destination filepath
        mode: the write mode. Usually "w" for write, or "a" for append. Default "w"
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as f:
        f.write(content)
