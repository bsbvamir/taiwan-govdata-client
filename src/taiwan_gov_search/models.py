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

    @classmethod
    def from_api(cls, data: Dict) -> "BusinessItem":
        raw_dgbas = data.get("DGBAS", "")
        dgbas_list = []
        if raw_dgbas:
            for entry in raw_dgbas.split(";"):
                parts = entry.strip().split(":")
                if len(parts) == 2:
                    dgbas_list.append(DgbasEntry(code=parts[0], name=parts[1]))
        return cls(category=data.get("Category", ""),
                   category_name=data.get("Category_Name", ""),
                   classes=data.get("Classes", ""),
                   classes_name=data.get("Classes_Name", ""),
                   subcategory=data.get("SubCategory", ""),
                   subcategories_name=data.get("SubCategory_Name", ""),
                   business_item=data.get("Business_Item", ""),
                   business_item_desc=data.get("Business_Item_Desc", ""),
                   business_item_content=data.get("Business_Item_Content", ""),
                   dgbas=dgbas_list)

