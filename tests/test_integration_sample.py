import pytest
from taiwan_gov_search.client import TaiwanGovClient
from taiwan_gov_search.models import BusinessItem, DgbasEntry


def test_real_api_response_structure():
    """Test that the client correctly handles the actual API response structure."""

    # Simulate the actual API response structure from the analysis
    mock_api_response = {
        "value": [
            {
                "Category": "A",
                "Category_Name": "農、林、漁、牧業",
                "Classes": "A1",
                "Classes_Name": "農業",
                "Subcategory": "A101",  # Correct API field name
                "Subcategories_Name": "農藝及園藝業",  # Correct API field name
                "Business_Item": "A101011",
                "Business_Item_Desc": "種苗業",
                "Business_Item_Content": "依植物品種及種苗法規定，從事繁殖、輸出入、銷售種苗之事業者。",
                "Dgbas": "0119\t其他農作物栽培業"
                # Correct API field name and format
            },
            {
                "Category": "B",
                "Category_Name": "礦業及土石採取業",
                "Classes": "B1",
                "Classes_Name": "礦業",
                "Subcategory": "B101",
                "Subcategories_Name": "煤礦業",
                "Business_Item": "B101010",
                "Business_Item_Desc": "煤礦業",
                "Business_Item_Content": "從事煤炭之探勘、開採、選洗及相關活動。",
                "Dgbas": "0111\t稻作栽培業\n0112\t雜糧栽培業\n0113\t特用作物栽培業"
            }
        ]
    }

    client = TaiwanGovClient()

    # Mock the API response with filtering logic
    def mock_get(*args, **kwargs):
        params = kwargs.get('params', {})
        filter_param = params.get('$filter', '')

        # Create a proper mock response object
        class MockResponse:
            def __init__(self, data):
                self._data = data

            def raise_for_status(self):
                pass

            def json(self):
                return self._data

        # If there's a filter, apply it to the response
        if filter_param and "Business_Item eq 'A101011'" in filter_param:
            # Return only the first item
            filtered_response = {"value": [mock_api_response["value"][0]]}
            return MockResponse(filtered_response)
        elif filter_param and "Business_Item eq 'B101010'" in filter_param:
            # Return only the second item
            filtered_response = {"value": [mock_api_response["value"][1]]}
            return MockResponse(filtered_response)
        else:
            # Return all items
            return MockResponse(mock_api_response)

    with pytest.MonkeyPatch().context() as m:
        m.setattr(client.session, 'get', mock_get)

        # Test filtering by business item code
        results = client.get_business_items(business_item_code="A101011")

        assert len(results) == 1
        item = results[0]

        # Verify all fields are correctly mapped
        assert item.category == "A"
        assert item.category_name == "農、林、漁、牧業"
        assert item.classes == "A1"
        assert item.classes_name == "農業"
        assert item.subcategory == "A101"  # Should now work with correct field name
        assert item.subcategories_name == "農藝及園藝業"  # Should now work with correct field name
        assert item.business_item == "A101011"
        assert item.business_item_desc == "種苗業"
        assert item.business_item_content == "依植物品種及種苗法規定，從事繁殖、輸出入、銷售種苗之事業者。"

        # Verify DGBAS parsing works correctly
        assert len(item.dgbas) == 1
        assert item.dgbas[0].code == "0119"
        assert item.dgbas[0].name == "其他農作物栽培業"

        # Test the second item with multiple DGBAS entries
        results = client.get_business_items(business_item_code="B101010")
        assert len(results) == 1
        item = results[0]

        # Verify multiple DGBAS entries are parsed correctly
        assert len(item.dgbas) == 3
        assert item.dgbas[0].code == "0111"
        assert item.dgbas[0].name == "稻作栽培業"
        assert item.dgbas[1].code == "0112"
        assert item.dgbas[1].name == "雜糧栽培業"
        assert item.dgbas[2].code == "0113"
        assert item.dgbas[2].name == "特用作物栽培業"


def test_dgbas_parsing_edge_cases():
    """Test DGBAS parsing with various edge cases."""
    client = TaiwanGovClient()

    # Test empty DGBAS field
    assert client._parse_dgbas_field("") == []
    assert client._parse_dgbas_field(None) == []

    # Test single entry
    result = client._parse_dgbas_field("0119\t其他農作物栽培業")
    assert len(result) == 1
    assert result[0].code == "0119"
    assert result[0].name == "其他農作物栽培業"

    # Test multiple entries with newlines
    result = client._parse_dgbas_field("0111\t稻作栽培業\n0112\t雜糧栽培業")
    assert len(result) == 2
    assert result[0].code == "0111"
    assert result[0].name == "稻作栽培業"
    assert result[1].code == "0112"
    assert result[1].name == "雜糧栽培業"

    # Test malformed entries (should be ignored)
    result = client._parse_dgbas_field(
        "0111\t稻作栽培業\nmalformed_entry\n0112\t雜糧栽培業")
    assert len(result) == 2  # Only valid entries should be parsed


@pytest.mark.integration
def test_get_business_items_live():
    client = TaiwanGovClient()
    results = client.get_business_items(top=5)
    assert len(results) > 0

    for item in results:
        assert item.business_item != ""
        assert isinstance(item.dgbas, list)


@pytest.mark.integration
def test_keyword_search_returns_results():
    """Ensure live keyword query returns at least one result."""
    client = TaiwanGovClient()
    results = client.get_business_items()  # Or add a business_item_code you know exists
    assert results, "Expected at least one result from live business item query"


@pytest.mark.integration
def test_known_business_item_returns_results():
    """Query known business item and check its presence."""
    client = TaiwanGovClient()
    results = client.get_business_items(business_item_code="B101010", top=5)

    assert results, "Expected results for business_item_code='B101010'"
    assert any("煤炭" in item.business_item_content for item in results), \
        "Expected '煤炭' to appear in business_item_content"
