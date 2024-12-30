# Copyright: (c) 2024, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# Import ConfigParser for file based configuration
from configparser import ConfigParser, NoSectionError, NoOptionError
# Provide hcloud Client object
from hcloud import Client
# Import warnings
import warnings

from . import constants


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


    def dest2source(self, sections: list[str] | None = None ) -> None:
        """This method swaps destination with source for given sections

        Parameters
        ----------
        sections : list[str] | None
                   List of sections to swap destination and source
        """

        if not sections:
            sections = self.resource_sections

        for section in sections:
            if section not in self.resource_sections:
                warnings.warn(f"'{section}' is not defined. Did you misspell it? Skipping ...")
                continue

            # Get destination name
            tmp = self.resource_section_dict[section]['destination']

            # Switch destination and source definitions
            self.resource_section_dict[section]['source'] = self.resource_section_dict[section]['destination']
            self.resource_section_dict[section]['destination'] = tmp

