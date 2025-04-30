from notion_db.builder import Builder
from notion_db.notion import TasksNotionModel


class TaskBuilder(Builder):

    def __init__(self,
                 page: dict):
        super().__init__(page)

        self.properties: TasksNotionModel = self.set_model_properties(
            self.__set_properties(page['properties']))

    def __set_properties(self, properties: dict) -> dict:

        try:
            self.key_in_dict("Task", properties)
            self.key_in_dict("Type", properties)
            self.key_in_dict("Do Date", properties)
            self.key_in_dict("Music Project", properties)
            self.key_in_dict("Location", properties)

        except ValueError as e:
            raise e

        return properties

    def set_model_properties(self, properties: dict) -> TasksNotionModel:

        name = self.set_title(properties['Task'])
        type = self.set_select(properties['Type'])
        start_date_time = self.set_date(properties['Do Date'])['start']
        end_date_time = self.set_date(properties['Do Date'])['end']
        music_project_id = self.set_relation(properties['Music Project'])
        location_id = self.set_relation(properties['Location'])

        return TasksNotionModel(id=self.id,
                                name=name,
                                type=type,
                                start_date_time=start_date_time,
                                end_date_time=end_date_time,
                                music_project_id=music_project_id,
                                location_id=location_id)
