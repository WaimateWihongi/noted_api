from .modules.base import Base
from .modules.users import Users
from .modules.clients import Clients
from .modules.records import Records
from .modules.keyworkers import Keyworkers
from .modules.groups import Groups
from .modules.billing import Billing
from .modules.client_lists import ClientLists

class API(
    Users,
    Clients,
    ClientLists,
    Records,
    Keyworkers,
    Groups,
    Billing,
): pass
