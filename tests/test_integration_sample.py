import pytest
from taiwan_gov_search.client import TaiwanGovClient


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
