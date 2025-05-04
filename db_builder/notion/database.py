import json
from pathlib import Path
from typing import Callable

class NotionDatabase:
    
    def __init__(self,
                 notion_get_func: Callable,
                 database_name: str,
                 path_to_json_folder: str,
                 generate_from_file=True):
        
        self.data = self.__get_notion_database_from_file_or_api(
            notion_get_func, 
            database_name,
            path_to_json_folder,
            generate_from_file
        )
         

    def __get_notion_database_from_file_or_api(self, notion_get_func: Callable, database_name: str, path_to_json_folder: str, from_file=False) -> dict:
        
        database_filename = Path(database_name).with_suffix('.json')
        if from_file:

            Path(path_to_json_folder).mkdir(exist_ok=True)

            path = Path(path_to_json_folder, database_filename)
            if path.is_file():

                with open(path, 'r') as f:
                    database_dict = json.loads(f.read())

                return database_dict

            else:

                with open(path, 'w') as f:
                    database_dict = notion_get_func()
                    f.write(json.dumps(database_dict))

                return database_dict

        return notion_get_func()
    