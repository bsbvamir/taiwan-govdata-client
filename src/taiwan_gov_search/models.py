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
        raw_dgbas = data.get("Dgbas", "")
        dgbas_list = []
        if raw_dgbas:
            for line in raw_dgbas.split('\n'):
                line = line.strip()
                if '\t' in line:
                    parts = line.split('\t', 1)
                    if len(parts) == 2:
                        code, name = parts
                        dgbas_list.append(DgbasEntry(code=code.strip(), name=name.strip()))
        return cls(category=data.get("Category", ""),
                   category_name=data.get("Category_Name", ""),
                   classes=data.get("Classes", ""),
                   classes_name=data.get("Classes_Name", ""),
                   subcategory=data.get("Subcategory", ""),
                   subcategories_name=data.get("Subcategories_Name", ""),
                   business_item=data.get("Business_Item", ""),
                   business_item_desc=data.get("Business_Item_Desc", ""),
                   business_item_content=data.get("Business_Item_Content", ""),
                   dgbas=dgbas_list)

