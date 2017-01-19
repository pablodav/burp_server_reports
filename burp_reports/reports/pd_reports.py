from ..backends.burpui_api import Clients
from pandas.io.json import json_normalize
import pandas as pd


class BuiPdReports(Clients):

    def clients_report(self) -> pd.DataFrame:
        """

        :return (pandas.DataFrame):
             name server  stats.total  stats.totsize stats.windows
            0  demo3  Burp2       541260     8624522478       unknown
            1  demo4  Burp2       541260     8624522478       unknown
            2  demo1  Burp1       541254     8723581166         false
            3  demo2  Burp1       541260     8624522478         false

        """
        dreport = json_normalize(self.get_clients_reports_brief())
        preport = pd.DataFrame(dreport)

        return preport
