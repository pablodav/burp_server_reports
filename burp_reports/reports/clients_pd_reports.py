from .clients_reports import BurpReports


class BurpPdReports(BurpReports):

    def clients_outdated(self):
        outdated = self.clients_outdated()
