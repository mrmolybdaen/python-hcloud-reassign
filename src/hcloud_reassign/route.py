# Copyright: (c) 2024, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module provides a class and methods to recreate routes."""

from hcloud import networks

# Import utilities
from . import utils


class HCloudRouteSection(utils.HcloudClassBase):
    """This class represents a route section to recreate routes and reassign standard gateways."""

    net = networks.annotations
    print(net)
