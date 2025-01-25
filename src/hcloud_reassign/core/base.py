# Copyright: (c) 2025 Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module provides utility functions and classes used by other modules."""

# Import ConfigParser for file based configuration
from configparser import ConfigParser

# Import dataclass
from dataclasses import dataclass

# Import sleep
from time import sleep

# Import warnings
import warnings

# Provide hcloud Client object
from hcloud import Client
from hcloud.actions import Action, BoundAction, ResourceActionsClient

# Import local constants
from ..utils import constants

# Wrap hcloud.Client and others into our own type,
# though hcloud does not need to get imported in every module
HcloudClient = Client
HcloudAction = Action
HcloudBoundAction = BoundAction
HcloudResourceActions = ResourceActionsClient


def make_client(token: str | None = None, url: str = constants.CONFIG_OPTION_API_URL) -> HcloudClient:
    """Create an instance of the Hcloud client.

    This is a wrapper around hcloud.Client.

    Parameters
    ----------
    token : str
            API token to authenticate with the Hcloud.
    url : str, optional
          URL of the Hcloud API.

    Returns
    -------
    hcloud.Client
    """
    return HcloudClient(token=token, api_endpoint=url)


@dataclass
class HcloudReassignIni:
    """Hcloud Reassign INI file class."""

    def __init__(self, path: str, api_token: str = None) -> None:
        """Initialize configuration object.

        Create an instance with a configuration file and an optional api token parameter.

        Parameters
        ----------
        path : str
               Path to the INI file.
        api_token : str, optional
                    API token to authenticate with the Hcloud API.
        """
        self.config = ConfigParser()
        self.config.read(filenames=path, encoding="utf-8")
        self.resource_sections = self.config.sections()

        # Remove the client section from section list
        if constants.CONFIG_SECTION_CLIENT in self.resource_sections:
            self.resource_sections.remove(constants.CONFIG_SECTION_CLIENT)
        else:
            self.config.add_section(constants.CONFIG_SECTION_CLIENT)
            warnings.warn(
                f"Section '{constants.CONFIG_SECTION_CLIENT}' " f"is not defined. Appending and setting defaults.",
                stacklevel=2,
            )
            self.config.set(constants.CONFIG_SECTION_CLIENT, "api_url", constants.CONFIG_DEFAULT_API_URL)

        # Set or get API token
        if api_token:
            self.config.set(constants.CONFIG_SECTION_CLIENT, constants.CONFIG_OPTION_API_TKN, api_token)
        else:
            self.config.has_section(constants.CONFIG_OPTION_API_TKN)

        # Expose configuration options
        self.__client_section2dict()
        self.__resource_section2dict()

    def __resource_section2dict(self):
        """Create a dictionary from resource sections."""
        # Create empty dictionary
        self.resource_section_dict = {}
        # Fill out resource dictionary with sub dictionaries made by sections.
        for section in self.resource_sections:
            self.resource_section_dict[section] = {}
            for option in self.config.options(section):
                if option == "metrics":
                    self.resource_section_dict[section][option] = self.config.getboolean(section, option)
                else:
                    self.resource_section_dict[section][option] = self.config.get(section, option)

    def __client_section2dict(self):
        """Create a dictionary from client sections."""
        # Create empty client dictionary
        self.client_section_dict = {}
        for option in self.config.options(constants.CONFIG_SECTION_CLIENT):
            self.client_section_dict[option] = self.config.get(constants.CONFIG_SECTION_CLIENT, option)


@dataclass
class HcloudClassBase:
    """This class provides all basics."""

    section_model: dict[str, type]
    section_type: str

    # Error codes
    status_success = constants.STATUS_SUCCESS
    status_running = constants.STATUS_RUNNING
    status_error = constants.STATUS_ERROR

    def __init__(self, section: dict, client: dict, hclient: HcloudClient | None = None) -> None:
        """Initialize HcloudClassBase.

        Parameters
        ----------
        section : dict
                  Dictionary of options contained by a section.
        client : dict
                 Dictionary of client section information
        hclient : Client|None, optional
                  hcloud.Client object. Use when to reassign multiple resources.
        """
        # Assign section
        self.section = section
        self.client = client

        self.__check_client()
        self.__check_section()

        # In case of multiple actions, we do not want too much
        # API connections and client objects because of rate limits.
        if not hclient:
            self.hclient = HcloudClient(
                token=self.client[constants.CONFIG_OPTION_API_TKN],
                api_endpoint=self.client[constants.CONFIG_OPTION_API_URL],
            )
        else:
            self.hclient = hclient

    def __check_section(self) -> None:
        """Check if section was defined correctly."""
        if not ("type" in self.section.keys() and self.section["type"]):
            raise KeyError("Section 'type' is not defined or empty.")

        if self.section["type"] != self.section_type:
            raise ValueError(
                f"Wrong section type for this Class. Configured '{self.section['type']}', wants '{self.section_type}'.'"
            )

        # Check if section model and defined section match.
        for option_name, option_type in self.section_model.items():
            if option_name not in self.section.keys():
                if not (isinstance(self.section[option_name], bool) or self.section[option_name]):
                    raise KeyError(f"Option '{option_name}' is not defined or empty.")
            if not isinstance(self.section[option_name], option_type):
                raise TypeError(f"Option '{option_name}' is not of type '{option_type}'.")

    def __check_client(self) -> None:
        """Check if client was defined correctly."""
        # Define shorthands for option names for readability
        url = constants.CONFIG_OPTION_API_URL
        token = constants.CONFIG_OPTION_API_TKN

        if not (url in self.client.keys() and self.client[url]):
            warnings.warn(f"Option '{url}' is not defined or empty. Using default constant.", stacklevel=2)
            self.client[url] = constants.CONFIG_DEFAULT_API_URL

        if not (token in self.client.keys() and self.client[token]):
            raise ValueError(f"Option '{token}' is not defined or empty. You an access/api token for authentication!")

    def __check_action_status__(self, response: HcloudBoundAction | HcloudAction, retries: int = 5) -> int:
        """Check status of an action.

        Parameters
        ----------
        response : HcloudBoundAction | HcloudAction
                   Action response object.

        Returns
        -------
        int:    Status, 0 on success, 1 on timeout, 2 on error.
        """
        retry_count = 0
        r = response

        while retry_count < retries and r.status != r.STATUS_SUCCESS:
            r = HcloudResourceActions(client=self.hclient, resource=None).get_by_id(response.id)
            retry_count += 1
            # wait a bit, so we do not spam the HCloud API.
            sleep(0.1)

        if r.status == r.STATUS_RUNNING:
            return self.status_running

        if r.status == r.STATUS_ERROR:
            return self.status_error

        return self.status_success
