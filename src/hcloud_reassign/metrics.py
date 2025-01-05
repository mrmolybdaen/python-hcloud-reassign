# Copyright: (c) 2024, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module gathers metrics over the Hetzner Cloud API."""

# Import utilities
from . import utils


class HServerMetrics(utils.HcloudClassBase):
    """This class represents a metrics client to gather information about one or more cloud servers."""

    pass
