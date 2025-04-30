from notion_db.builder import Builder
from notion_db.notion import ChoirNotionModel


class ChoirBuilder(Builder):

    def __init__(self,
                 page: dict):

        super().__init__(page)
        self.properties: ChoirNotionModel = self.set_choir(
            self.__set_choir_properties(page['properties']))

    def __set_choir_properties(self, choir_properties: dict) -> dict:

        try:
            self.key_in_dict("Choir", choir_properties)

        except ValueError as e:
            raise e

        return choir_properties

    def set_choir(self, choir_properties: dict) -> ChoirNotionModel:

        name = self.set_title(choir_properties['Choir'])

        return ChoirNotionModel(id=self.id,
                                name=name)
