# Copyright: (c) 2024, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module provides a class and methods to reassign floating IP address objects."""

# Import utilities
from . import utils


class HCloudFloatingIPSection(utils.HcloudClassBase):
    """This class represents a Floating IP section."""

    def __init__(self, section: dict[str, str, str, str, bool], client: dict):
        """Initialize a Floating IP section object.

        Parameters
        ----------
        section: dict[str, str, str, str, bool]
                 Dictionary with floating_ip section contents.
        client: dict
                Dictionary of connection information such as API token and endpoint url.
        """
        super().__init__(section=section, client=client)

        self.__check_section(stype="floating")

        self.resource: str = section["resource"]
        self.source: str = section["source"]
        self.destination: str = section["destination"]
        self.metrics: bool = section["metrics"]

    def __reassign(self, dest: str):
        """Reassign floating IP section."""
        dest_server = self.hclient.servers.get_by_name(name=dest)
        flip = self.hclient.floating_ips.get_by_name(self.resource)

        response = self.hclient.floating_ips.assign(floating_ip=flip, server=dest_server)

        return response.status

    def assign_destination(self):
        """Assign floating IP section to destination."""
        return self.__reassign(dest=self.destination)

    def assign_source(self):
        """Assign floating IP section to source."""
        return self.__reassign(dest=self.source)
