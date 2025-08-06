import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock
from taiwan_gov_search.client import TaiwanGovClient


@pytest.fixture
def client():
    return TaiwanGovClient()


def test_get_business_items(client):
    mock_payload = {
        "value": [
            {
                "Category": "A",
                "Category_Name": "Agriculture",
                "Classes": "A1",
                "Classes_Name": "Crop",
                "Subcategory": "A11",
                "Subcategories_Name": "Rice",
                "Business_Item": "A1101",
                "Business_Item_Desc": "Rice planting",
                "Business_Item_Content": "Rice growing",
                "Dgbas": "0111\t稻作栽培業\n0112\t雜糧栽培業",
            }
        ]
    }

    with patch("requests.Session.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_payload
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        results = client.get_business_items(top=1)
        assert len(results) == 1
        assert results[0].business_item == "A1101"
