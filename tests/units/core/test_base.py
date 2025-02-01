# Copyright: (c) 2025 Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module provides unit tests for hcloud_reassign.core.base."""

from hcloud_reassign.core.base import make_client, HcloudClient
from secrets import token_urlsafe


class TestHcloudReassignCoreBase:
    """This class groups unit tests for hcloud_reassign.core.base."""

    client = make_client(token=token_urlsafe())

    def test_make_client_instance_type(self) -> None:
        """Tests if the make_client function indeed creates an instance of HcloudClient."""
        assert isinstance(self.client, HcloudClient)
