import os
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import requests
from dotenv import load_dotenv
from .models import BusinessItem, DgbasEntry


class TaiwanGovClient:
    BASE_URL = "https://data.gcis.nat.gov.tw/od/data/api/FCB90AB1-E382-45CE-8D4F-394861851E28"

    def __init__(self):
        self.session = requests.Session()

    def get_business_items(self, business_item_code: Optional[str] = None,
                           top: int = 100, skip: int = 0,
                           format_: str = 'json') -> List[BusinessItem]:
        """Fetch business items from the Taiwan Government open data API."""

        params = {"$format": format_, "$top": top, "$skip": skip, }
        if business_item_code:
            params["$filter"] = f"Business_Item eq '{business_item_code}'"

        response = self.session.get(self.BASE_URL, params=params, timeout = 30)
        response.raise_for_status()
        data = response.json()

        results = []
        for entry in data:
            # Parse DGBAS agency field
            dgbas_field = entry.get("DGBAS", "")
            dgbas_entries = self._parse_dgbas_field(dgbas_field)

            item = BusinessItem(
                category = entry.get("Category", ""),
                category_name = entry.get("Category_Name", ""),
                classes = entry.get("Classes", ""),
                classes_name=entry.get("Classes_Name", ""),
                subcategory=entry.get("SubCategory", ""),
                subcategories_name=entry.get("SubCategory_Name", ""),
                business_item=entry.get("Business_Item", ""),
                business_item_desc=entry.get("Business_Item_Desc", ""),
                business_item_content=entry.get("Business_Item_Content", ""),
                dgbas=dgbas_entries
            )
            results.append(item)
        return results
