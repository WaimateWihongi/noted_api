from .base import Base

class Users(Base):
    def __init__(self):
        super().__init__()
    
    def me(self):
        """Get information about the currently logged in user"""
        response = self.get('users/me')
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not get user information," + response.text)
    
    def create_user(self, user_details: dict):
        """Create a user"""
        # Check if all required fields are present
        required_fields = ["firstName", "lastName", "username", "email", "password"]
        
        for field in required_fields:
            if field not in user_details:
                raise Exception(f"Field '{field}' is required to create a user")
        
        # Create user
        user = {
            "title": "",
            "firstName": user_details["firstName"],
            "lastName": user_details["lastName"],
            "registrationNumber": "",
            "shortCode": user_details["firstName"][0] + user_details["lastName"][0],
            "username": user_details["username"],
            "phone": "",
            "email": user_details["email"],
            "suspended": False,
            "isAdminUser": False,
            "password": user_details["password"],
            "privileges": [],
            "teamIds": user_details["teamIds"]
        }

        json_data = {
            "query": "\n    mutation createUser($user: CreateUserInput!) {\n  createUser(input: $user) {\n    user {\n      id\n    }\n  }\n}\n    ",
            "variables": {
                "user": user
            }
        }

        response = self.post('graphql', json=json_data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not create user," + response.text)
        
    
    def get_all_users(self):
        """Get information about all users"""
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
                    "size": 100000, # 100000 just to be sure!
                    "page": 0
                }
            }
        }
        
        # Get all users
        response = self.post('graphql', json=data)
        
        if response.status_code == 200:
            return response.json()["data"]["users"]["results"]
        else:
            raise Exception("Could not get user information," + response.text)
        
    def get_user(self, user_id:str) -> dict:
        """Get information about a user"""
        # Get user
        json_data = {
            "query": '\n    query getUser($id: Long!) {\n  user(id: $id) {\n    ...UserDetails\n  }\n}\n    \n    fragment UserDetails on User {\n  id\n  authenticationDetails {\n    username\n  }\n  title\n  firstName\n  lastName\n  name\n  registrationNumber\n  phone\n  email\n  shortCode\n  suspended\n  isAdminUser\n  securityRoles {\n    id\n    name\n    key\n  }\n  services {\n    id\n    name\n  }\n  privileges {\n    id\n    name\n    key\n  }\n  deleted\n}\n    ',
            "variables":{"id": user_id}
        }
        
        response = self.post('graphql', json=json_data, return_error=True)
        data = response.json()

        if response.status_code == 200:
            user = data["data"]["user"]
            return user
    
    def get_user_teams(self, user_id:int):
        json_data = {
            "query": "\n    query getUserWithTeam($id: Long!) {\n  user(id: $id) {\n    ...UserWithTeams\n  }\n}\n    \n    fragment UserWithTeams on User {\n  id\n  teams {\n    id\n    name\n    description\n    key\n  }\n  defaultTeams {\n    id\n    name\n    description\n    key\n  }\n}\n    ",
            "variables":{"id": user_id}
        }
        
        response = self.post('graphql', json=json_data, return_error=True)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            raise Exception("Could not get user," + response.text)

    def get_user_last_activity(self, user_id:int):
        """
            Get the last activity of a user
        """
        json_data = {
            "query": "\n    query auditTrailEntrySearch($input: AuditTrailEntitySearchParams!) {\n  auditTrailEntrySearch(input: $input) {\n    entries {\n      id\n      name\n      type\n      timestamp\n      email\n      dob\n    }\n  }\n}\n    ",
            "variables": {
                "input": {
                "actionsBy": True,
                "id": user_id,
                "type": "USER",
                "sortAttr": "timestamp",
                "sortDir": "DESC"
                }
            }
        }
        response = self.post('graphql', json=json_data, return_error=True)
        if response.status_code == 200:
            if len(response.json()["data"]["auditTrailEntrySearch"]["entries"]) == 0 \
                or response.json()["data"]["auditTrailEntrySearch"]["entries"][0]["timestamp"] == None:
                return 0
            return sorted(response.json()["data"]["auditTrailEntrySearch"]["entries"], key=lambda x: x["timestamp"], reverse=True)[0]["timestamp"]

    def remove_user_team(self, user_id:int, team_id:int):
        json_data = {
            "query": '\n    mutation unassignTeamsFromUser($input: AssignTeamsToUserInput!) {\n  unassignTeamsFromUser(input: $input) {\n    ...UserWithTeams\n  }\n}\n    \n    fragment UserWithTeams on User {\n  id\n  teams {\n    id\n    name\n    description\n    key\n  }\n  defaultTeams {\n    id\n    name\n    description\n    key\n  }\n}\n    ',
            "variables": {
                "input": {
                    "userId": user_id,
                    "teamIds": [team_id]
                }
            }
        }

        response = self.post('graphql', json=json_data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Could not remove user from team," + response.text)
    
    def add_user_team(self, user_id:int, team_id:int):
        pass

    def suspend_user(self, user_id:str):
        """Suspend a user"""
        user_details = self.get_user(user_id)
        user_details["suspended"] = True

        user_details = user_details#['data']['user']
        user_details = {
            "email": user_details["email"],
            "firstName": user_details["firstName"],
            "id": user_details["id"],
            'isAdminUser': user_details['isAdminUser'],
            'lastName': user_details['lastName'],
            'phone': user_details['phone'],
            "privileges": [{"id": 4}, {"id": 9}],
            'registrationNumber': "",
            "shortCode": user_details["shortCode"],
            'suspended': True,
            'title': user_details['title'],
            'username': user_details['authenticationDetails']['username'],
        }

        json_data = {
            "query": '\n    mutation userUpdate($user: UpdateUserInput!) {\n  updateUser(input: $user) {\n    user {\n      ...UserDetails\n    }\n  }\n}\n    \n    fragment UserDetails on User {\n  id\n  authenticationDetails {\n    username\n  }\n  title\n  firstName\n  lastName\n  name\n  registrationNumber\n  phone\n  email\n  shortCode\n  suspended\n  isAdminUser\n  securityRoles {\n    id\n    name\n    key\n  }\n  services {\n    id\n    name\n  }\n  privileges {\n    id\n    name\n    key\n  }\n  deleted\n}\n    ',
            "variables": {
                "user": user_details
            }
        }
        
        response = self.post('graphql', json=json_data)
        if response.status_code == 200 and not response.json().get("errors"):
            return response.json()
        else:
            raise Exception("Could not suspend user," + response.json().get("errors", response.text))