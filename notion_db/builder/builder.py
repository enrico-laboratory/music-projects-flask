from dateutil import parser


class Builder:

    def __init__(self,
                 page: dict):

        self.id = self.__set_id(page)

    def __set_id(self, page):

        return page['id']

    def key_in_dict(self, key: str, d: dict):

        if not key in d:
            raise ValueError(
                f'notion database property "{key}" is expected, but it was not found.')

    def set_relation(self, obj: dict) -> str:

        if obj['relation']:
            return obj['relation'][0]['id']

        return None

    def set_select(self, obj: dict) -> str:

        if obj['select']:
            return obj['select']['name']

        return None

    def set_rich_text(self, obj: dict) -> str:

        if obj['rich_text']:
            return obj['rich_text'][0]['text']['content']

        return None

    def set_number(self, obj: dict) -> int:

        if obj['number']:
            return obj['number']

        return None

    def set_title(self, obj: dict) -> str:

        if obj['title']:
            return obj['title'][0]['text']['content']

        return None

    def set_url(self, obj: dict) -> str:

        return obj['url']

    def set_phone_number(self, obj: dict) -> str:

        return obj['phone_number']

    def set_email(self, obj: dict) -> str:

        return obj['email']

    def set_checkbox(self, obj: dict) -> bool:

        return obj['checkbox']

    def set_multi_select(self, obj: dict) -> str:

        result = ""

        if obj['multi_select']:

            for i, select in enumerate(obj['multi_select']):
                result += select['name']

                if i != len(obj['multi_select']) - 1:
                    result += ', '

            return result

        return None

    def set_date(self, obj: dict) -> dict:

        if obj['date']:
            start = obj['date']['start']
            end = obj['date']['end']
            if obj['date']['start']:
                start_parsed = parser.parse(start)
            else:
                start_parsed = None
            if obj['date']['end']:
                end_parsed = parser.parse(end)
            else:
                end_parsed = None

            return {"start": start_parsed, "end": end_parsed}

        return None
