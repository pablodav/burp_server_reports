from burp_reports.reports.pd_reports import BuiPdReports


class TestPdReportsDemo:

    def test_pd_obj(self):
        buireport = BuiPdReports(apiurl='https://admin:admin@demo.burp-ui.org/api/')
        pd_brief_clients = buireport.clients_report()
        return pd_brief_clients
        
    def test_pdreports_buidemo(self):
        clients = self.test_pd_obj()
        
                