from notion_db.builder import Builder
from notion_db.notion import ContactNotionModel


class ContactBuilder(Builder):

    def __init__(self,
                 page: dict):
        super().__init__(page)

        self.properties: ContactNotionModel = self.set_contact(
            self.__set_properties(page['properties']))

    def __set_properties(self, properties: dict) -> dict:

        try:
            self.key_in_dict("Role", properties)
            self.key_in_dict("Address 1 - City", properties)
            self.key_in_dict("Phone 1 - Value", properties)
            self.key_in_dict("E-mail", properties)
            self.key_in_dict("E-mail 2 - Value", properties)
            self.key_in_dict("Notes", properties)
            self.key_in_dict("Voice", properties)
            self.key_in_dict("\ufeffName", properties)

        except ValueError as e:
            raise e

        return properties

    def set_contact(self, properties: dict) -> ContactNotionModel:

        name = self.set_title(properties['\ufeffName'])
        role = self.set_multi_select(properties['Role'])
        email1 = self.set_email(properties['E-mail'])
        email2 = self.set_email(properties['E-mail 2 - Value'])
        address = self.set_rich_text(properties['Address 1 - City'])
        phone = self.set_phone_number(properties['Phone 1 - Value'])
        notes = self.set_rich_text(properties['Notes'])
        voice = self.set_multi_select(properties['Voice'])

        return ContactNotionModel(id=self.id,
                                  name=name,
                                  role=role,
                                  email1=email1,
                                  email2=email2,
                                  address=address,
                                  phone=phone,
                                  notes=notes,
                                  voice=voice)
