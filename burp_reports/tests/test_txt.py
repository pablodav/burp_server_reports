from ..lib.txt import TxtReports
from .test_clients_dummy import test_dummy

class TestTxt:
    
    def test_detail_txt(self):
        clients = test_dummy()
        # Create the object to export the report
        clients_reports = TxtReports(clients,
                                     detail=True,
                                     foot_notes="This is a test foot txt"
                                     )

        clients_reports.report_to_txt(print_text=True)

    def test_detail_txt_body(self):
        clients = test_dummy()
        # Create the object to export the report
        clients_reports = TxtReports(clients,
                                     detail=True
                                     )

        clients_reports.print(print_text=True)
        
