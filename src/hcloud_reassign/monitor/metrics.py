# Copyright: (c) 2025, Christian Siegel <molybdaen@mr42.org>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module gathers metrics over the Hetzner Cloud API."""

# Import datetime
from datetime import datetime, timedelta

# Import utilities
from ..core import base
from ..reassign.ip_floating import ip_floating_section_model
from ..utils.types import TimeNow_t, HcloudSectionFloatingIp_t, HcloudMetric_t


class HServerMetricsServer(base.HcloudClassBase):
    """This class represents a metrics client to gather information about one or more cloud servers."""

    def __init__(self, section: HcloudSectionFloatingIp_t, client: dict) -> None:
        """Initialize the metrics object.

        Parameters
        ----------
        section : HcloudSectionFloatingIp_t
                  Dictionary with floating_ip section contents.
        client : dict
                 Dictionary of HCloud API client information.
        """
        self.section_type = "ip-floating"
        self.section_model = ip_floating_section_model

        super().__init__(section=section, client=client)

        self.resource: str = section["resource"]
        self.source: str = section["source"]
        self.destination: str = section["destination"]
        self.metrics: bool = section["metrics"]

    @staticmethod
    def __check_timedata(interval: tuple[str, str] | TimeNow_t, step: float = 1800) -> tuple[str, str]:
        """Check time formatting.

        Parameters
        ----------
        interval : tuple[str, str] | TimeNow_t
                   A list containing ISO8601 formatted datetime strings.
                   interval[0] represents t0, interval[1] represents t1.
                   Use 'now' to get current time string and this string
                   minus five minutes.
        step : float
               Minimal length of the interval in seconds.

        Returns
        -------
        tuple[str, str]

        Raises
        ------
        ValueError: Interval limits must be ISO8601 formatted.
        ValueError: Interval must be greater or equal to step size
        """
        if isinstance(interval, TimeNow_t):
            t1 = datetime.now()
            t0 = t1 - timedelta(seconds=1800)
            interval = (t0.isoformat(), t1.isoformat())
            return interval
        else:
            try:
                t0 = datetime.fromisoformat(interval[0])
                t1 = datetime.fromisoformat(interval[1])

                dt = (t1 - t0).total_seconds()
                if dt < step or dt < 1800:
                    raise ValueError("Interval must be greater or equal to step size and bigger than 1800 seconds")
            except ValueError as err:
                print(err)
                raise ValueError("Interval limits must be ISO8601 formatted.")

            interval = (interval[0], interval[1])

        return interval

    def __get_metrics__(
        self,
        srv: str,
        metrics_type: HcloudMetric_t | list[HcloudMetric_t],
        interval: tuple[str, str] | TimeNow_t = "now",
        step: float = 10,
    ) -> list:
        """Get metrics for Hetzner Cloud servers.

        Parameters
        ----------
        srv : str
              Name of the server as defined in the Hetzner Cloud Console.
        metrics_type : HcloudMetric_t | list[HcloudMetric_t]
                       Word or list of HCloud metrics. Choose between 'cpu',
                       'network' and 'disk'
        interval : tuple[str, str] | TimeNow_t, optional
                   default: 'now'
                   A tuple containing ISO8601 formatted datetime strings.
                   interval[0] represents t0, interval[1] represents t1.
        step : float, optional
               default: 10 seconds
               Minimal length of the interval in seconds.

        Returns
        -------
        list: List of timestamps and corresponding metrics measurements
        """
        start, end = self.__check_timedata(interval=interval, step=step)

        # Get server
        server = self.hclient.servers.get_by_name(name=srv)
        # Get metrics
        response = server.get_metrics(type=metrics_type, start=start, end=end, step=step)

        if isinstance(metrics_type, HcloudMetric_t):
            data = [response.metrics.time_series[metrics_type]]
        else:
            data = []
            keys = []

            for metric in metrics_type:
                for key in response.metrics.keys():
                    if key.startswith(metric):
                        keys.append(key)

            for metric in keys:
                data.append(response.metrics.time_series[metric])

        return data

    def get_dest(
        self,
        metrics_type: HcloudMetric_t | list[HcloudMetric_t],
        interval: tuple[str, str] | TimeNow_t,
        step: float = 10,
    ) -> list:
        """Get destination metrics for Hetzner Cloud servers.

        Parameters
        ----------
        metrics_type : HcloudMetric_t | list[HcloudMetric_t]
                       Word or list of HCloud metrics. Choose between 'cpu',
                       'network' and 'disk'
        interval : tuple[str, str] | TimeNow_t, optional
                   default: 'now'
                   A tuple containing ISO8601 formatted datetime strings.
                   interval[0] represents t0, interval[1] represents t1.
        step : float, optional
               default: 10 seconds
               Minimal length of the interval in seconds.

        Returns
        -------
        list: List of timestamps and corresponding metrics measurements
        """
        return self.__get_metrics__(srv=self.destination, metrics_type=metrics_type, interval=interval, step=step)

    def get_source(
        self,
        metrics_type: HcloudMetric_t | list[HcloudMetric_t],
        interval: tuple[str, str] | TimeNow_t,
        step: float = 10,
    ) -> list:
        """Get source metrics for Hetzner Cloud servers.

        Parameters
        ----------
        metrics_type : HcloudMetric_t | list[HcloudMetric_t]
                       Word or list of HCloud metrics. Choose between 'cpu',
                       'network' and 'disk'
        interval : tuple[str, str] | TimeNow_t, optional
                   default: 'now'
                   A tuple containing ISO8601 formatted datetime strings.
                   interval[0] represents t0, interval[1] represents t1.
        step : float, optional
               default: 10 seconds
               Minimal length of the interval in seconds.

        Returns
        -------
        list: List of timestamps and corresponding metrics measurements
        """
        return self.__get_metrics__(srv=self.destination, metrics_type=metrics_type, interval=interval, step=step)
