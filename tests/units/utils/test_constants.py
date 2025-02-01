#!/usr/bin/env python3

# Copyright: (c) 2025, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Hcloud Reassign Script utility unit tests for constants.

This module contains unit tests for hcloud_reassign.utils.constants
"""

from importlib.metadata import version
import hcloud_reassign.utils.constants as constants


class TestConstants:
    """Test group for hcloud_reassign.utils.constants."""

    def test_script_version(self) -> None:
        """Check if SCRIPT_VERSION is the same as package version.

        Note: This test needs a build and install of the python package.
        """
        environmental_info = constants.EnvironmentalInfo()
        assert environmental_info.SCRIPT_VERSION == version("hcloud_reassign")
