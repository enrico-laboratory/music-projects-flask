from notion_db.builder import Builder
from notion_db.notion import MusicProjectNotionModel


class MusicProjectBuilder(Builder):

    def __init__(self,
                 page: dict):
        super().__init__(page)

        self.properties: MusicProjectNotionModel = self.set_music_project(
            self.__set_music_project_properties(page['properties']))

    def __set_music_project_properties(self, music_project_properties: dict) -> dict:

        try:
            self.key_in_dict("Year", music_project_properties)
            self.key_in_dict("Status", music_project_properties)
            self.key_in_dict("Description", music_project_properties)
            self.key_in_dict("Excerpt", music_project_properties)
            self.key_in_dict("Choir", music_project_properties)
            self.key_in_dict("Title", music_project_properties)

        except ValueError as e:
            raise e

        return music_project_properties

    def set_music_project(self, music_project_properties: dict) -> MusicProjectNotionModel:

        name = self.set_title(music_project_properties['Title'])
        year = self.set_number(music_project_properties['Year'])
        choir_id = self.set_relation(music_project_properties['Choir'])
        status = self.set_select(music_project_properties['Status'])
        excerpt = self.set_rich_text(music_project_properties['Excerpt'])
        description = self.set_rich_text(
            music_project_properties['Description'])

        return MusicProjectNotionModel(id=self.id,
                                       name=name,
                                       year=year,
                                       choir_id=choir_id,
                                       status=status,
                                       excerpt=excerpt,
                                       description=description)
