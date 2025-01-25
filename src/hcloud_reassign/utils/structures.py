# Copyright: (c) 2025, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module provides structures and function aliases."""

# Import utilities
from ..reassign import ip_floating
from .constants import STATUS_SUCCESS, STATUS_ERROR, STATUS_RUNNING, STATUS_TIMEOUT

# Enum of Classes to call, mapping to configuration
# section types.
hcloud_functions = {
    "ip_floating": ip_floating.HCloudFloatingIPSection,
}

# Enum for error messages.
status_message = {
    STATUS_SUCCESS: "success",
    STATUS_TIMEOUT: "timeout",
    STATUS_ERROR: "error",
    STATUS_RUNNING: "running",
}
