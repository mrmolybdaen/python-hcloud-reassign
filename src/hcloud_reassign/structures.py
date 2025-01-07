# Copyright: (c) 2025, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module provides structures and function aliases."""

# Import utilities
from . import ip_floating
from . import ip_public
from . import route

# Enum of Classes to call, mapping to configuration
# section types.
hcloud_functions = {
    "ip_floating": ip_floating.HCloudFloatingIPSection,
    "ip_public": ip_public.HCloudPrimaryIpSection,
    "route": route.HCloudRouteSection,
}

# Enum for error messages.
status_message = {0: "success", 1: "timeout", 2: "error"}
