from ..reports.pd_reports import BuiReports


class TestPdReportsDemo:

    def test_pd_obj(self):
        buireport = BuiReports(apiurl='https://admin:admin@demo.ziirish.me/api/')
        pd_brief_clients = buireport.clients_report()
        return pd_brief_clients
        
    def test_pdreports_buidemo(self):
        clients = self.test_pd_obj()
        
                