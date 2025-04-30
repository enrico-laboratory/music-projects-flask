from pprint import pprint as pp

import pytest

from utils import Notion
from notion_db.builder import LocationBuilder
from notion_db import config

@pytest.fixture
def notion():
    return Notion(config.NOTION_API_TOKEN)
    
def test_set_location(notion):
    locations = notion.get_locations()
    for location in locations['results']:
        
        location_builder = LocationBuilder(location).properties
        # pp(location_builder)
