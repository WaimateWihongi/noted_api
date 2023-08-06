from .modules.base import Base
from .modules.users import Users
from .modules.clients import Clients
from .modules.records import Records
from .modules.keyworkers import Keyworkers

class API(
    Users,
    Clients,
    Records,
    Keyworkers,
): pass

if __name__ == "__main__":
    api = API()
    api.login("WaimateWihongiTest", "WaimateWihongi123")
    #print(api.set_keyworker(190222, 2587))
    print(len(api.get_clients_with_keyworker(2170)))