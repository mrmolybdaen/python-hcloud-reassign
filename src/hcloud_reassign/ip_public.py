# Copyright: (c) 2024, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module stops server, reassigns primary IP addresses and starts the servers again."""

# Import utilities
from . import utils


class HCloudPrimaryIpSection(utils.HcloudClassBase):
    """This class represents a primary IP section of the configuration file."""

    pass
