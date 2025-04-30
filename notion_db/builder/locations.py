from notion_db.builder import Builder
from notion_db.notion import LocationNotionModel


class LocationBuilder(Builder):

    def __init__(self,
                 page: dict):
        super().__init__(page)

        self.properties: LocationNotionModel = self.set_location(
            self.__set_location_properties(page['properties']))

    def __set_location_properties(self, location_properties: dict) -> dict:

        try:
            self.key_in_dict("Location", location_properties)
            self.key_in_dict("City", location_properties)
            self.key_in_dict("Address", location_properties)
            self.key_in_dict("Purpose", location_properties)

        except ValueError as e:
            raise e

        return location_properties

    def set_location(self, location_properties: dict) -> LocationNotionModel:

        name = self.set_title(location_properties['Location'])
        city = self.set_rich_text(location_properties['City'])
        address = self.set_rich_text(location_properties['Address'])
        purpose = self.set_multi_select(location_properties['Purpose'])

        return LocationNotionModel(id=self.id,
                                   name=name,
                                   city=city,
                                   address=address,
                                   purpose=purpose)
    
