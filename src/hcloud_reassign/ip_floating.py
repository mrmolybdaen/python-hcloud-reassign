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
        self.section_type = "ip_floating"
        self.section_model = {"resource": str, "source": str, "destination": str, "metrics": bool}

        super().__init__(section=section, client=client)

        self.resource: str = section["resource"]
        self.source: str = section["source"]
        self.destination: str = section["destination"]
        self.metrics: bool = section["metrics"]

    def reassign_server(self, dest: str) -> int:
        """Reassign floating IP section.

        Parameters
        ----------
        dest: str
              Name of the server object to get assigned.

        Returns
        -------
        status: int
                A status code word. Can be 'success' (0), 'running' (1) or 'error' (2).

        """
        dest_server = self.hclient.servers.get_by_name(name=dest)
        if dest_server is None:
            print(f"Server resource {dest_server} not found.")
            return self.status_error

        flip = self.hclient.floating_ips.get_by_name(self.resource)
        if flip is None:
            print(f"Floating IP resource {self.resource} not found.")
            return self.status_error

        # Reassign floating ip to server
        response = self.hclient.floating_ips.assign(floating_ip=flip, server=dest_server)
        # Check status of reassign action
        status = self.__check_action_status__(response=response)

        return status

    def __assign_destination(self) -> int:
        """Assign floating IP section to destination."""
        return self.reassign_server(dest=self.destination)

    def __assign_source(self) -> int:
        """Assign floating IP section to source."""
        return self.reassign_server(dest=self.source)

    def reassign(self, direction: str) -> int:
        """Reassign floating IP section by direction.

        Parameters
        ----------
        direction: str
                   Either 'src' or 'dest'.

        Raises
        ------
        ValueError: If 'dest' is not 'src' or 'dest'.
        """
        if direction not in ["src", "dest"]:
            raise ValueError(f"Invalid destination {direction}! Must be 'src' or 'dest'.")

        status = 0
        if direction == "src":
            status = self.__assign_source()
        if direction == "dest":
            status = self.__assign_destination()

        return status
