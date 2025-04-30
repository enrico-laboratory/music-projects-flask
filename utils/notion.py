import json

import requests


class Notion:

    BASE_URL = 'https://api.notion.com/v1'
    API_VERSION = '2022-06-28'
    DATABASE_MUSIC_PROJECTS = "a290b3f737f242b697959acb9f18283e"
    DATABASE_CHOIRS = "97be022740354a03b71a6e10da34fcb6"
    DATABASE_TASKS = "b25b103631b34fc2a8804eec0b2b3813"
    DATABASE_LOCATIONS = "264aecbf12ec4d439a306d3360a70001"
    DATABASE_MUSIC = "eccd5c44d17b4c97b28ae358f8801063"
    DATABASE_CONTACTS = "d644d3c1cf214104bebd58e128551c75"
    DATABASE_CAST = "065066b1d60a478a9d8a2725b2fee660"
    DATABASE_REPERTOIRE = "aaff3c7cc9fd4c49a9d0cead3d51f75b"

    def __init__(self,
                 token: str,
                 notion_api_version: str = None):

        self.notion_api_version = notion_api_version or self.API_VERSION
        self.token = token

    def __set_headers(self) -> dict:

        return {"Authorization": f"Bearer {self.token}",
                "Notion-Version": self.notion_api_version,
                "Content-Type": "application/json"}

    def __make_request(self, database: str, body: dict) -> dict:

        headers = self.__set_headers()
        url = f'{self.BASE_URL}/databases/{database}/query'

        if body:
            data = json.dumps(body)
        else:
            data = None
            
        response = requests.post(
            url=url, headers=headers, data=data)

        if response.status_code != 200:
            raise Exception(
                f'Notion api responded with a {response.status_code} status code. Error: {response.text}')

        response_dict = json.loads(response.text)

        has_more = response_dict['has_more']
        next_cursor = response_dict['next_cursor']
        while has_more:

            body = {"start_cursor": next_cursor}
            response_has_more = requests.post(
                url=url, headers=headers, data=json.dumps(body))
            response_has_more_dict = json.loads(response_has_more.text)
            for page in response_has_more_dict['results']:
                response_dict['results'].append(page)

            has_more = response_has_more_dict['has_more']
            next_cursor = response_has_more_dict['next_cursor']

        return response_dict

    def get_choirs(self) -> dict:

        return self.__make_request(self.DATABASE_CHOIRS, None)

    def get_music_projects(self) -> dict:

        return self.__make_request(self.DATABASE_MUSIC_PROJECTS, None)

    def get_music(self) -> dict:

        return self.__make_request(self.DATABASE_MUSIC, None)

    def get_contacts(self) -> dict:

        return self.__make_request(self.DATABASE_CONTACTS, None)

    def get_cast(self) -> dict:

        return self.__make_request(self.DATABASE_CAST, None)

    def get_repertoire(self) -> dict:

        return self.__make_request(self.DATABASE_REPERTOIRE, None)
                
    def get_tasks(self) -> dict:

        # body = {"filter": {
        #     "or": [
        #         {
        #             "property": "Type",
        #             "select": {
        #                 "equals": "Rehearsal"
        #             }
        #         },
        #         {
        #             "property": "Type",
        #             "select": {
        #                 "equals": "Concert"
        #             }
        #         }
        #     ]}}

        return self.__make_request(self.DATABASE_TASKS, None)
    
    def get_locations(self) -> dict:
        return self.__make_request(self.DATABASE_LOCATIONS, None)
