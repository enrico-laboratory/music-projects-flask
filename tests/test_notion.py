import json

import pytest

from utils import Notion
from notion_db import config

@pytest.fixture
def notion():
    return Notion(config.NOTION_API_TOKEN)
    
def test_get_locations_status_code(notion):
    try:
        notion.get_locations()
    except Exception as e :
        pytest.fail(f"get location return a status code not 200. {e}")            

def test_get_locations_reuslts(notion):
    result_exists = "results" in notion.get_locations()
    assert result_exists

def test_get_locations_locations(notion):
    location_exists = 'Location' in notion.get_locations()["results"][0]['properties']
    assert location_exists        
       
