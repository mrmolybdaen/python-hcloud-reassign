# Copyright: (c) 2024, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# Import ConfigParser for file based configuration
from configparser import ConfigParser, NoSectionError, NoOptionError

# Provide hcloud Client object
from hcloud import Client
# Import warnings
import warnings

from . import constants


def make_client(token: str|None = None, url: str = constants.CONFIG_OPTION_API_URL) -> Client:
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

    return Client(token=token, api_endpoint=url)

class HcloudClient(Client):
    pass


class HcloudReassignIni:
    """
    Hcloud Reassign INI file
    """

    def __init__(self, path: str, api_token: str = None) -> None:
        """

        Parameters
        ----------
        path : str
        api_token : str, optional
        """

        self.config = ConfigParser()
        self.config.read(filenames=path, encoding='utf-8')
        self.resource_sections = self.config.sections()

        # Remove the client section from section list
        if constants.CONFIG_SECTION_CLIENT in self.resource_sections:
            self.resource_sections.remove(constants.CONFIG_SECTION_CLIENT)
        else:
            self.config.add_section(constants.CONFIG_SECTION_CLIENT)
            warnings.warn(f"Section '{constants.CONFIG_SECTION_CLIENT}' is not defined. Appending and setting defaults.")
            self.config.set(constants.CONFIG_SECTION_CLIENT, 'api_url', constants.CONFIG_DEFAULT_API_URL)

        # Set or get API token
        if api_token:
            self.config.set(constants.CONFIG_SECTION_CLIENT, constants.CONFIG_OPTION_API_TOKEN, api_token)
        else:
            self.config.has_section(constants.CONFIG_OPTION_API_TOKEN)

        # Expose configuration options
        self.__client_section2dict()
        self.__resource_section2dict()


    def __resource_section2dict(self):
        """This method creates a dictionary from resource sections"""

        # Create empty dictionary
        self.resource_section_dict = {}
        # Fill out resource dictionary with sub dictionaries made by sections.
        for section in self.resource_sections:
            self.resource_section_dict[section] = {}
            for option in self.config.options(section):
                self.resource_section_dict[section][option] = self.config.get(section, option)


    def __client_section2dict(self):
        """This method creates a dictionary from client sections"""

        # Create empty client dictionary
        self.client_section_dict = {}
        for option in self.config.options(constants.CONFIG_SECTION_CLIENT):
            self.client_section_dict[option] = self.config.get(constants.CONFIG_SECTION_CLIENT, option)


class HcloudClassBase:
    """This class provides all basics"""

    def __init__(self, section: dict, client: dict, hclient: HcloudClient|None = None, **kwargs) -> None:
        """Initialize HcloudClassBase

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

        # In case of multiple actions, we do not want too much
        # API connections and client objects because of rate limits.
        if not hclient:
            self.hclient = HcloudClient(token=self.client[constants.CONFIG_OPTION_API_TOKEN],
                                        api_endpoint=self.client[constants.CONFIG_DEFAULT_API_URL])
        else:
            self.hclient = hclient


    def __check_section(self, stype: str) -> None:
        """This method checks if section was defined correctly
        Parameters
        ----------
        stype : str
                Type of section
        """

        if 'type' not in self.section.keys() and not self.section['type']:
            raise KeyError("Section 'type' is not defined or empty.")

        if self.section['type'] != stype:
            raise ValueError(f"Wrong section type for this function. "
                             f"Configured '{self.section['type']}', wants '{stype}'.'")

        if 'source' not in self.client.keys() and not self.client['source']:
            raise KeyError("Option 'source' is not defined or empty.")

        if 'destination' not in self.client.keys() and not self.client['destination']:
            raise KeyError("Option 'destination' is not defined or empty.")


    def __check_client(self) -> None:
        """This method checks if client was defined correctly"""

        # Define shorthands for option names for readability
        url = constants.CONFIG_OPTION_API_URL
        token = constants.CONFIG_OPTION_API_TOKEN

        if url not in self.client.keys() and not self.client[url]:
            warnings.warn(f"Option '{url}' is not defined or empty. Using default constant.")
            self.client[url] = constants.CONFIG_DEFAULT_API_URL

        if token not in self.client.keys() and not self.client[token]:
            raise ValueError(f"Option '{token}' is not defined or empty. You an access/api token for authentication!")