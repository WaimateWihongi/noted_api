import logging
from requests import Session

class Base:
    API_URL = 'https://api.noted.com/api/v1/'

    def __init__(self):
        self.session = Session()
        self.session.hooks['response'].append(self.response_hook) # This is a hook that will be called on every response
        self.logged_in = False
        self.login_info = None

    def response_hook(self, response, *args, **kwargs):
        if response.status_code == 401:
            logging.error("Unauthorized")
            raise Exception("Unauthorized")
        return response
    
    def login(self, username:str, password:str):
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
    
    def get(self, url:str):
        request =  self.session.get(self.API_URL + url)
        if request.status_code == 200:
            return request
        else:
            raise Exception(f"Could not get {url}: {request.text}")
    
    def post(self, url:str, json:dict):
        request =  self.session.post(self.API_URL + url, json=json)
        if request.status_code == 200:
            return request
        else:
            raise Exception(f"Could not post {url}: {request.text}")