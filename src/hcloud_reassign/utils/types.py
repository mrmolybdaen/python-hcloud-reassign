# Copyright: (c) 2025, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module provides custom type."""

from typing import TypeAlias, Literal

HcloudMetric_t: TypeAlias = Literal["cpu", "disk", "network"]
HcloudSectionFloatingIp_t: TypeAlias = dict[str, str, str, str, bool]

TimeNow_t: TypeAlias = Literal["now"]
