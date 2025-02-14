#!/usr/bin/env python3

# Copyright: (c) 2025, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""HCloud Reassignment script.

This script provides an easy-to-use command line api for the Hetzner HCloud module.
You can easily reassign Hetzner Cloud network resources to different machines.
"""

import sys

# Import ArgumentParser for command line based configuration
from argparse import ArgumentParser

# Import getpass for password/token
from getpass import getpass

try:
    from ..utils.structures import hcloud_functions, status_message
    from ..utils.constants import EnvironmentalInfo
    from ..core.base import HcloudReassignIni
except ImportError as error:
    print(error)
    print("You might need to install hcloud-reassign.")
    raise error


def main():
    """Call this function when this module is used as a script.

    Returns
    -------
    status_code : int
                  Return status code

    """
    # Create argument parser
    parser = ArgumentParser(
        prog="hcloud-reassign", description="Reassign Hetzner Cloud network resources to different machines."
    )
    parser.add_argument("-c", "--config", action="store", dest="config", help="Path to configuration file")
    parser.add_argument(
        "-t",
        "--token",
        action="store_true",
        dest="token",
        help="API token for manual use. If defined, the 'token' in the configuration file will be ignored.",
    )
    parser.add_argument(
        "-r",
        "--resource",
        nargs="*",
        action="store",
        dest="resource",
        help="Resource to reassign. This matches the section name in the INI file.",
    )
    parser.add_argument(
        "-d",
        "--direction",
        action="store",
        choices=["dest", "src"],
        default="dest",
        dest="machine",
        help="Choose assignment destination. To reassign from source to dest, choose 'dest', otherwise choose 'src",
    )
    parser.add_argument(
        "--source", action="store", dest="source", help="Source to reassign, alternative to source in INI file"
    )
    parser.add_argument(
        "--destination",
        action="store",
        dest="destination",
        help="Destination to reassign, alternative to destination in INI file",
    )
    parser.add_argument(
        "--version", action="store_true", dest="version", help="Display version and environment information."
    )

    # Parse arguments
    cli_args = parser.parse_args()

    if cli_args.version:
        print(f"SCRIPT VERSION: {EnvironmentalInfo.SCRIPT_VERSION}")
        print(f"SCRIPT PATH: {EnvironmentalInfo.SCRIPT_PATH}")
        print("---")
        print(f"PYTHON EXECUTABLE: {EnvironmentalInfo.PYTHON_EXECUTABLE}")
        print(f"PYTHON VERSION: {EnvironmentalInfo.PYTHON_VERSION}")
        print(f"PYTHON PLATFORM: {EnvironmentalInfo.PYTHON_PLATFORM}")
        print(f"PYTHON INFO: {EnvironmentalInfo.PYTHON_INFO}")

        return 0

    token = None
    if cli_args.token:
        token = getpass(prompt="Password or Token: ")

    status = 0

    if cli_args.config and not (cli_args.source or cli_args.destination):
        config = HcloudReassignIni(path=cli_args.config, api_token=token)

        # Do all resources if --resource is not defined
        # else do resources defined in --resource
        if cli_args.resource:
            resources = cli_args.resource
        else:
            resources = config.resource_sections

        # Iterate through all the resources
        for resource in resources:
            reassignment_function = hcloud_functions[config.resource_section_dict[resource]["type"]]
            reassignment = reassignment_function(
                section=config.resource_section_dict[resource], client=config.client_section_dict
            )
            status = reassignment.reassign(direction=cli_args.machine)

            print(f"{resource}: {status_message[status]}")

    return status


if __name__ == "__main__":
    sys.exit(main())
