from burpui.misc.backend.burp2 import Burp
from burp_reports.backends.burpui_clients import Clients
clientes = Clients(burp_version=2, conf='/etc/burp/burp-ui.cfg')

clientes.get_clients()
clientes.get_client(client='monitor')

clientes.get_b_logs(client='monitor', number=1)