"""
Unofficial Noted API v1.2
This will need to be updated when the official API is available.
"""
import requests
import logging
import datetime
from ._wrappers import *

class Record():
    """Represents a record in Noted"""
    def __init__(self, api, id):
        self.api = api
        self.id = id

class User():
    """Represents kaimahi in Noted"""
    def __init__(self, api, id):
        self.api = api
        self.id = id
    
    def get(self):
        url = f"https://api.noted.com/api/v1/users/{self.id}"
        r = self.api.session.get(url)
        return r.json()
    
    def get_records():
        url = f"https://api.noted.com/api/v1/records/user/{self.id}"
    
    def suspend(self):
        url = f"https://api.noted.com/api/v1/graphql"
        data = self.get()
        payload = {
            "query": "\n    mutation UserUpdate($user: UpdateUserInput!) {\n  updateUser(input: $user) {\n    user {\n      ...UserDetails\n    }\n  }\n}\n    \n    fragment UserDetails on User {\n  id\n  authenticationDetails {\n    username\n  }\n  title\n  firstName\n  lastName\n  name\n  gender\n  registrationNumber\n  phone\n  email\n  shortCode\n  suspended\n  notAllowedToDelete\n  isAdminUser\n  securityRoles {\n    id\n    name\n    key\n  }\n  services {\n    id\n    name\n  }\n  privileges {\n    id\n    name\n    key\n  }\n  deleted\n}\n    ",
        }
        r = self.api.session.post(url)
        return r.status_code == 204

class LoginInfo():
    def __init__(self, api):
        """
            Information about the current user logged in
        """
        self.api = api
        self.details_raw = self.api.get_me()
        self.is_admin = any([r["id"] == 2 for r in self.details_raw["securityRoles"]])

class Client():
    def __init__(self, api, id):
        self.api = api
        self.id = id
    
    def edit(self, data):
        url = f"https://api.noted.com/api/v1/clients/{self.id}"
        r = self.api.session.put(url, json=data)
        return r.json()
    
    def get(self):
        url = f"https://api.noted.com/api/v1/clients/{self.id}"
        r = self.api.session.get(url)
        return r.json()
    
    def add_keyworker(self, keyworker_id, start_date=datetime.datetime.now().isoformat()):
        data = self.get()
        if keyworker_id not in data['keyWorkerIds']:
            url = f"https://api.noted.com/api/v1/key-worker-relationships"
            json_data = {
                "client":{"id": self.id},
                "relationshipStart": f"{start_date}+13:00",
                "user": {"id": keyworker_id}
            }
            r = self.api.session.post(url, json=json_data)
            return {"success":r.status_code == 201}
        else:
            return {"error": "Keyworker already set"}
    
    def remove_keyworker(self, keyworker_id, remove=False, end_date=datetime.datetime.now().isoformat()):
        """
        Removes a keyworker from a client
        @param keyworker_id: The ID of the keyworker to remove
        @param remove: If True, the keyworker will be removed from the client.
            If False, the keyworker will be ended with a date.
        """
        
        # Get the client data to check if the keyworker is set
        data = self.get()
        if keyworker_id in data['keyWorkerIds']:

            url = f"https://api.noted.com/api/v1/key-worker-relationships?clientId={self.id}"
            relationships = self.api.session.get(url)
            
            # Loop through the relationships and find the one with the keyworker ID
            for relationship in relationships.json():
                if relationship['user']['id'] == keyworker_id:
                    url = f"https://api.noted.com/api/v1/key-worker-relationships/{relationship['id']}"
                    
                    # Remove the keyworker
                    if remove:
                        r = self.api.session.delete(url)
                        if r.status_code == 204:
                            return {"success": True}
                        else:
                            return {"error": "Unknown error"}
                    # Or just set the end date
                    else:
                        new_relationship_data = relationship
                        new_relationship_data['relationshipEnd'] = f"{end_date}+13:00"
                        r = self.api.session.put(url, json=new_relationship_data)
                        if r.status_code == 200:
                            return {"success": True}
                        else:
                            print(r.json())
                            return {"error": "Unknown error"}
            return {"error": "Keyworker not found"}
        else:
            return {"error": "Keyworker not set"}

    def search_notes(self,
        term:str,
        client_id:str,
        count=50,
        size=20,
        page=0, 
        status="ALL",
        total=1,
        type="CONSULTATION"):
        url = "https://api.noted.com/api/v1/records/client/%s" % client_id
        params = {
            "count": count,
            "page":page,
            "pages":1,
            "searchterm":term,
            "size":size,
            "status":status,
            "total":total,
            "type": type
        }
        return self.api.session.get(url, params=params).json()

class API():
    def __init__(self):
        self.session = requests.Session()
        self.session.hooks['response'].append(self.response_hook)
        self.logged_in = False
        self.login_info = None
    
    def response_hook(self, response, *args, **kwargs):
        if response.status_code == 401:
            logging.error("Unauthorized")
            raise Exception("Unauthorized")
        return response

    def login(self, username, password):
        self.username = username
        self.password = password

        headers = {
            'authority': 'api.noted.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-NZ,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://app.noted.com',
            'referer': 'https://app.noted.com/login',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        json_data = {
            'query': '\n    mutation authenticate($input: AuthenticationInput!) {\n  authenticate(input: $input) {\n    result\n    lastLogin\n    shouldChangePasswordHint\n    token\n    version\n    lockoutSeconds\n    roles\n  }\n}\n    ',
            'variables': {
                'input': {
                    'username': username,
                    'password': password,
                    'eulaAgreed': False,
                    'captcha': '',
                },
            },
        }
        response = self.session.post('https://api.noted.com/api/v1/graphql', headers=headers, json=json_data)
        if response.status_code == 200:
            logging.info("Login successful")
            self.logged_in = True
            self.session.headers.update({'x-auth-token': response.json()['data']['authenticate']['token']})
            return True
        else:
            logging.error("Login failed")
            return False
    
    @login_required
    def get_me(self):
        r = self.session.get("https://api.noted.com/api/v1/users/me")
        return r.json()

    @login_required
    def query_graphql(self, query, variables):
        """
        Query GraphQL.
        @param query: Query
        @param variables: Variables
        """
        url = "https://api.noted.com/api/v1/graphql"
        data = {
            "query": query,
            "variables": variables,
        }
        
        # If variables is None, remove it from the data
        if variables is None:
            data = {
                "query": query,
            }
        
        r = self.session.post(url, json=data)
        return r.json()

    @login_required
    def get_user(self, username):
        """
        Get user by ID.
        @param user_id: User ID
        """
        url = f"https://api.noted.com/api/v1/users/{username}"
        r = self.session.get(url)
        return r.json()
    
    @login_required
    def get_all_users(self):
        """
        Get all users.
        """
        page_number = 0 # Used to loop through all pages

        url = f"https://api.noted.com/api/v1/graphql"
        query = """
            query
                usersQuery ($input: UserQueryParams!) {
                users (input: $input) {
                    results {
                    id
                    authenticationDetails {
                        username
                    }
                    firstName
                    lastName
                    email
                    suspended
                    }
                    pages
                }
                }
        """
        data = {
            "query": query,
            "variables": {
                "input": {
                    "searchTerm": "",
                    "sortDir": "desc",
                    "sortAttr": "firstName",
                    "securityRole": "",
                    "activeOnly": False,
                    "size": 25,
                    "page": 100
                }
            }
        }
        r = self.session.post(url, json=data)
        if r.status_code == 200:

            # Variables
            users = r.json()['data']['users']['results']
            max_pages = r.json()['data']['users']['pages']
            
            # Loop through all pages (doesn't include the first page)
            for page_number in range(1, max_pages):
                data['variables']['input']['page'] = page_number # Update page number
                r = self.session.post(url, json=data) # Make request
                
                # Check if request was successful
                if r.status_code == 200:
                    users += r.json()['data']['users']['results']
                else:
                    return {"error": "Unknown error"}
            return users
        else:
            # Initial request returned an error
            return {"error": "Unknown error"}
    
    @login_required
    def get_users_by_email(self, email):
        """
        Get users by email.
        @param email: Email
        """
        url = f"https://api.noted.com/api/v1/graphql"
        query = """
            query
                usersQuery ($input: UserQueryParams!) {
                users (input: $input) {
                    results {
                    id
                    authenticationDetails {
                        username
                    }
                    firstName
                    lastName
                    email
                    }
                    pages
                }
                }
        """
        data = {
            "query": query,
            "variables": {
                "input": {
                    "searchTerm": email,
                    "sortDir": "desc",
                    "sortAttr": "firstName",
                    "securityRole": "",
                    "activeOnly": False,
                    "size": 25,
                    "page": 0
                }
            }
        }
        r = self.session.post(url, json=data)
        return [user for user in r.json()['data']['users']['results']
        if user['email'] == email]
    
    def get_notes_on_client(client):
        return
    
    @login_required
    def get_client(self, client_id):
        """
        Get client by ID.
        @param client_id: Client ID
        return: Client
        """
        url = f"https://api.noted.com/api/v1/clients/{client_id}"
        r = self.session.get(url)
        if r.status_code == 200:
            return Client(self, client_id)
        else:
            raise Exception("Client not found!")

    @login_required
    def search_clients(self, term:str, size=20):
        """
        Search for clients by search term.
        @param term: Search term
        @param size: Number of results to return
        """
        url = "https://api.noted.com/api/v1/clients/search"
        params = {"activeonly":False, 
        "searchAddresses":False,
        "searchterm":term,
        "size":20}
        r = self.session.get(url, params=params)
        return r.json()
    
    @login_required
    def search_clients_by_filter(self, filters, size=20, page=0):
        """
        Search for clients by filter.
        @param filter: Filter (name, matchType, tags)
        """
        url = " https://api.noted.com/api/v1/clients-search"
        data = {
            "filters":filters if isinstance(filters, list) else [filters],
            "options":{
                "size":size,
                "inactiveClients": False,
                "page": page,
                "sortattr":"created",
                "sortdir":"DESC",
                "timezone":"Pacific/Auckland",
                }
            }
        r = self.session.post(url, json=data)
        return r.json()

    @login_required
    def create_whanau(self, clients, contract_id, description, primaryContact):
        """
        Create a new whānau.
        @param clients: List of client IDs (Expected: [{'id': '123'}, {'id': '456'}])
        @param contract_id: Contract ID
        @param description: Description
        @param primaryContact: Primary contact ID (Expected: {'id': '123'})
        """
        data = {
            "clients": clients,
            "contractId": contract_id,
            "description": description,
            "primaryContact": primaryContact,
        }
        url = "https://api.noted.com/api/v1/whanau"
        r = self.session.post(url, json=data)
        return r.json()

    def get_organisations_teams(self, include_users = False):
        if include_users:
            query = "\n    query getTeams {\n  teams {\n   fragment Team on Team {\n  id\n  name\n  description\n  key\n  recordSensitivity\n  modality {\n    id\n  }\n}\n    "
        else:
            query = "query getTeams { teams { ...Team } } fragment Team on Team { id name description key recordSensitivity modality { id } }"
        res = self.query_graphql(query, None)
        return res['data']['teams']

if __name__ == "__main__":
    api = API()
    api.login("WaimateWihongi", "tTq!Mgk4yAqCyaC")
    print(api.get_organisations_teams())