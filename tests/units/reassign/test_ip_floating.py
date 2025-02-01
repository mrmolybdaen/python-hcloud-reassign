#!/usr/bin/env python3

# Copyright: (c) 2025, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Test floating ip reassignments.

This module contains unit tests for hcloud_reassign.reassign.ip_floating.
"""

import pytest
from hcloud_reassign.reassign.ip_floating import HCloudFloatingIPSection


class TestHCloudFloatingIPSection:
    """Test group for hcloud_reassign.reassign.ip_floating."""

    def test_reassign_server(self) -> None:
        """Test the reassign server method."""
        print("test")

    def test_reassign_raise(self) -> None:
        """Check that invalid inputs to description raise ValueError."""
        with pytest.raises(ValueError):
            HCloudFloatingIPSection.reassign(direction="invalid")
