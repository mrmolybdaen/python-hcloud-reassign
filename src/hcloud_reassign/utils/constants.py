# Copyright: (c) 2025, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module contains constants used throughout hcloud_reassign."""
from sys import version, version_info, platform, prefix, executable
from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentalInfo:
    """This class contains system and interpreter information."""

    # Note some system information
    PYTHON_INFO = version
    PYTHON_VERSION = version_info
    PYTHON_EXECUTABLE = executable
    PYTHON_PLATFORM = platform

    # Note some module information
    SCRIPT_VERSION = "0.1.0"
    SCRIPT_PATH = prefix


# Configuration default section
CONFIG_SECTION_CLIENT = "client"

# API endpoint URL
CONFIG_DEFAULT_API_URL = "https://api.hetzner.cloud/v1"

# Configuration options
CONFIG_OPTION_API_URL = "api_url"
CONFIG_OPTION_API_TKN = "api_token"

# Create numeric status numbers
STATUS_SUCCESS = 0
STATUS_RUNNING = 1
STATUS_ERROR = 2
STATUS_TIMEOUT = 3
