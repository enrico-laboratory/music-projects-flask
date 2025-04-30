from notion_db.builder import Builder
from notion_db.notion import MusicNotionModel


class MusicBuilder(Builder):

    def __init__(self,
                 page: dict):
        super().__init__(page)

        self.properties: MusicNotionModel = self.set_music(
            self.__set_music_properties(page['properties']))

    def __set_music_properties(self, properties: dict) -> dict:

        try:
            self.key_in_dict("Music", properties)
            self.key_in_dict("Composer", properties)
            self.key_in_dict("Voices", properties)
            self.key_in_dict("Instruments", properties)
            self.key_in_dict("Solo", properties)
            self.key_in_dict("Length", properties)
            self.key_in_dict("Score", properties)
            self.key_in_dict("Media", properties)
            self.key_in_dict("Recording", properties)

        except ValueError as e:
            raise e

        return properties

    def set_music(self, properties: dict) -> MusicNotionModel:

        name = self.set_title(properties['Music'])
        composer = self.set_rich_text(properties['Composer'])
        voices = self.set_select(properties['Voices'])
        instruments = self.set_multi_select(properties['Instruments'])
        solo = self.set_select(properties['Solo'])
        length = self.set_number(properties['Length'])
        score = self.set_url(properties['Score'])
        media = self.set_url(properties['Media'])
        recording = self.set_url(properties['Recording'])
        
        return MusicNotionModel(id=self.id,
                                name=name,
                                composer=composer,
                                voices=voices,
                                instruments=instruments,
                                solo=solo,
                                length=length,
                                score=score,
                                media=media,
                                recording=recording)
