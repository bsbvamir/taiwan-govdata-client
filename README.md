# GCIS Business Classification API Client

A Python client for accessing Taiwan's **GCIS (Government Commercial Information System)** API, specifically designed to retrieve and parse business item classification data with proper handling of Traditional Chinese characters and government classification codes.

---


## Installation

```bash
git clone https://github.com/bsbvamir/taiwan-govdata-client.git
cd taiwan-govdata-client
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"   # editable install + development deps (pytest, etc.)
```

## Usage

```python
from taiwan_gov_search.client import TaiwanGovClient

# Initialize the GCIS client
client = TaiwanGovClient()

# Get all business items (paginated)
results = client.get_business_items(top=10)
print(f"Retrieved {len(results)} business items")

# Access business item data
for item in results:
    print(f"Code: {item.business_item}")
    print(f"Description: {item.business_item_desc}")
    print(f"Category: {item.category_name}")
    print(f"Subcategory: {item.subcategories_name}")
    print("---")
```

## Pagination

```python
# Get first 50 items
first_page = client.get_business_items(top=50, skip=0)

# Get next 50 items
second_page = client.get_business_items(top=50, skip=50)

# Get items 100-150
third_page = client.get_business_items(top=50, skip=100)
```

## Working with DGBAS Data

```python
# Get agriculture business items
agriculture_data = client.get_business_items(business_item_code="A101011")

for item in agriculture_data:
    print(f"Business Item: {item.business_item_desc}")
    print(f"Full Description: {item.business_item_content}")
    
    # DGBAS provides government classification codes
    if item.dgbas:
        print("Government Classifications:")
        for dgbas in item.dgbas:
            print(f"  Code: {dgbas.code}")
            print(f"  Name: {dgbas.name}")
    else:
        print("No DGBAS classifications available")
```

## Complete Example

```python
from taiwan_gov_search.client import TaiwanGovClient
from taiwan_gov_search.models import BusinessItem, DgbasEntry

def search_business_items(category_filter: str = None, limit: int = 10):
    """
    Search for business items with optional category filtering.
    
    Args:
        category_filter: Optional category code (e.g., "A" for agriculture)
        limit: Maximum number of results to return
    """
    client = TaiwanGovClient()
    
    # Get business items
    results = client.get_business_items(top=limit)
    
    # Filter by category if specified
    if category_filter:
        results = [item for item in results if item.category == category_filter]
    
    # Display results
    print(f"Found {len(results)} business items:")
    print("=" * 50)
    
    for item in results:
        print(f"Code: {item.business_item}")
        print(f"Description: {item.business_item_desc}")
        print(f"Category: {item.category_name}")
        print(f"Subcategory: {item.subcategories_name}")
        
        if item.dgbas:
            print("DGBAS Codes:")
            for dgbas in item.dgbas:
                print(f"  {dgbas.code}: {dgbas.name}")
        
        print("-" * 30)

# Usage examples
if __name__ == "__main__":
    # Get all business items
    search_business_items(limit=5)
    
    # Get agriculture items only
    search_business_items(category_filter="A", limit=3)
    
    # Get specific business item
    client = TaiwanGovClient()
    coal_data = client.get_business_items(business_item_code="B101010")
    
    if coal_data:
        item = coal_data[0]
        print(f"\nCoal Mining Details:")
        print(f"Code: {item.business_item}")
        print(f"Description: {item.business_item_desc}")
        print(f"Content: {item.business_item_content}")
```

## Implemented Endpoints

### Business Items Classification API

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/od/data/api/FCB90AB1-E382-45CE-8D4F-394861851E28` | GET | Retrieve business item classification data | `$format`, `$top`, `$skip`, `$filter` |

### Supported Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `$format` | string | No | `json` | Response format (json) |
| `$top` | integer | No | `100` | Number of records to retrieve (pagination limit) |
| `$skip` | integer | No | `0` | Number of records to skip (pagination offset) |
| `$filter` | string | No | - | OData filter expression (e.g., `Business_Item eq 'B101010'`) |
