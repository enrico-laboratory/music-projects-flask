from notion_db.builder import Builder
from notion_db.notion import PartAllocationNotionModel


class PartAllocationBuilder(Builder):

    def __init__(self,
                 page: dict):
        super().__init__(page)

        self.properties: PartAllocationNotionModel = self.set_part_allocation(
            self.__set_music_properties(page['properties']))

    def __set_music_properties(self, properties: dict) -> dict:

        try:
            self.key_in_dict("2", properties)
            self.key_in_dict("3", properties)
            self.key_in_dict("4", properties)
            self.key_in_dict("5", properties)
            self.key_in_dict("6", properties)
            self.key_in_dict("7", properties)
            self.key_in_dict("8", properties)
            self.key_in_dict("9", properties)
            self.key_in_dict("10", properties)
            self.key_in_dict("11", properties)
            self.key_in_dict("12", properties)
            self.key_in_dict("Music", properties)
            self.key_in_dict("1 - Top Voice", properties)
            self.key_in_dict("Selected", properties)
            self.key_in_dict("Order", properties)
            self.key_in_dict("Notes Divisi", properties)

        except ValueError as e:
            raise e

        return properties

    def set_part_allocation(self, properties: dict) -> PartAllocationNotionModel:

        name = self.set_title(properties['Order'])
        music_id = self.set_relation(properties['Music'])
        music_project_id = self.set_relation(properties['Music Project'])
        staff_1 = self.set_rich_text(properties['1 - Top Voice'])
        staff_2 = self.set_rich_text(properties['2'])
        staff_3 = self.set_rich_text(properties['3'])
        staff_4 = self.set_rich_text(properties['4'])
        staff_5 = self.set_rich_text(properties['5'])
        staff_6 = self.set_rich_text(properties['6'])
        staff_7 = self.set_rich_text(properties['7'])
        staff_8 = self.set_rich_text(properties['8'])
        staff_9 = self.set_rich_text(properties['9'])
        staff_10 = self.set_rich_text(properties['10'])
        staff_11 = self.set_rich_text(properties['11'])
        staff_12 = self.set_rich_text(properties['12'])
        notes = self.set_rich_text(properties['Notes Divisi'])
        selected = self.set_checkbox(properties['Selected'])

        return PartAllocationNotionModel(id=self.id,
                                name=name,
                                music_id=music_id,
                                music_project_id=music_project_id,
                                staff_1=staff_1,
                                staff_2=staff_2,
                                staff_3=staff_3,
                                staff_4=staff_4,
                                staff_5=staff_5,
                                staff_6=staff_6,
                                staff_7=staff_7,
                                staff_8=staff_8,
                                staff_9=staff_9,
                                staff_10=staff_10,
                                staff_11=staff_11,
                                staff_12=staff_12,
                                notes=notes,
                                selected=selected)
