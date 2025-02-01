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

    # Define a simple mockup section
    mock_section = {
        "type": "ip_floating",
        "resource": "mock_floating_ip",
        "source": "mock_server_a",
        "destination": "mock_server_b",
        "metrics": False,
    }

    # Define a simple mock up client configuration
    mock_client = {"api_token": "1", "api_url": "http://mock_server"}

    # Initialize the mock floating ip
    MockFloatingIP = HCloudFloatingIPSection(mock_section, mock_client)

    def test_reassign_server(self) -> None:
        """Test the reassign server method."""
        print("test")

    def test_reassign_raise(self) -> None:
        """Check that invalid inputs to description raise ValueError."""
        with pytest.raises(ValueError):
            # %TODO: We need a mockup configuration
            self.MockFloatingIP.reassign(direction="invalid")
