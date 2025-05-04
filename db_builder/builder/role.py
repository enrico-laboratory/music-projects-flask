from db_builder.builder import Builder
from db_builder.notion import RoleNotionModel


class RoleBuilder(Builder):

    def __init__(self,
                 page: dict):
        super().__init__(page)

        self.properties: RoleNotionModel = self.set_role(
            self.__set_properties(page['properties']))

    def __set_properties(self, properties: dict) -> dict:

        try:
            self.key_in_dict("Singer", properties)
            self.key_in_dict("Note", properties)
            self.key_in_dict("Status", properties)
            self.key_in_dict("Music Project", properties)
            self.key_in_dict("Role", properties)

        except ValueError as e:
            raise e

        return properties

    def set_role(self, properties: dict) -> RoleNotionModel:

        name = self.set_title(properties['Role'])
        music_project_id = self.set_relation(properties['Music Project'])
        contact_id = self.set_relation(properties['Singer'])
        note = self.set_rich_text(properties['Note'])
        status = self.set_select(properties['Status'])

        return RoleNotionModel(id=self.id,
                                  name=name,
                                  music_project_id=music_project_id,
                                  contact_id=contact_id,
                                  note=note,
                                  status=status)
