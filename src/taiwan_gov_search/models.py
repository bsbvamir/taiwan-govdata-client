from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import json

@dataclass
class DgbasEntry:
    code: str
    name: str

@dataclass
class BusinessItem:
    category: str
    category_name: str
    classes: str
    classes_name: str
    subcategory: str
    subcategories_name: str
    business_item: str
    business_item_desc: str
    business_item_content: str
    dgbas: List[DgbasEntry]
