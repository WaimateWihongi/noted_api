#from .modules.base import Base
from .modules.users import Users
from .modules.clients import Clients
from .modules.records import Records

class API(
    Users,
    Clients,
    Records,
): pass

if __name__ == "__main__":
    api = API()
    api.login("WaimateWihongi", "tTq!Mgk4yAqCyaC")
    print(api.get_user(3033))