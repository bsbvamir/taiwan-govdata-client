import os
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import requests
from dotenv import load_dotenv
from .models import BusinessItem, DgbasEntry


class TaiwanGovClient:
    """Client for accessing Taiwan Government Open Data API.

    Client handles HTTP requests to retrieve business item classification data
    and optionally filters them by business item code.

    Attributes:
        BASE_URL (str): The API endpoint for querying business item data.
        session (requests.Session): Reusable HTTP session for API requests.
    """

    BASE_URL = "https://data.gcis.nat.gov.tw/od/data/api/"
    BUSINESS_ITEMS_ENDPOINT = "FCB90AB1-E382-45CE-8D4F-394861851E28"

    def __init__(self):
        """
        Initialize a new TaiwanGovClient instance.

        Sets up a persistent requests.Session object with appropriate headers
        for querying the government API.
        """
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "taiwan-govdata-client/0.1.0",
            "Accept": "application/json",
        })

    def get_business_items(self, business_item_code: Optional[str] = None,
                           top: int = 100, skip: int = 0,
                           format_: str = 'json') -> List[BusinessItem]:
        """
        Fetch business items from the Taiwan Government open data API.
        Args:
            business_item_code (Optional[str]): Specific business item code to filter by.
            top (int): Number of records to retrieve (pagination limit).
            skip (int): Number of records to skip (pagination offset).
            format_ (str): Response format (default is 'json').

        Returns:
            List[BusinessItem]: Parsed list of BusinessItem objects from API results.
        """

        params = {"$format": format_, "$top": top, "$skip": skip, }

        if business_item_code:
            params["$filter"] = f"Business_Item eq '{business_item_code}'"

        url = f"{self.BASE_URL}{self.BUSINESS_ITEMS_ENDPOINT}"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        entries = data.get("value", data) if isinstance(data, dict) else data

        results = []
        for entry in entries:
            dgbas_field = entry.get("DGBAS", [])
            dgbas = [DgbasEntry(code=item["Code"], name=item["Name"]) for item
                     in dgbas_field]

            results.append(BusinessItem(
                    category=entry.get("Category", ""),
                    category_name=entry.get("Category_Name", ""),
                    classes=entry.get("Classes", ""),
                    classes_name=entry.get("Classes_Name", ""),
                    subcategory=entry.get("SubCategory", ""),
                    subcategories_name=entry.get("SubCategories_Name", ""),
                    business_item=entry.get("Business_Item", ""),
                    business_item_desc=entry.get("Business_Item_Desc", ""),
                    business_item_content=entry.get("Business_Item_Content", ""),
                    dgbas=dgbas,
                )
            )
        return results
