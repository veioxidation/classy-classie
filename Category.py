from typing import Optional, List

from pydantic import BaseModel


class Category(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    children: List["Category"] = []  # recursively defined list of children

    def add_child(self, child: "Category"):
        # Avoid duplicate children
        if all(child.code != existing.code for existing in self.children):
            self.children.append(child)

    class Config:
        arbitrary_types_allowed = True

# Allow self-referencing types (Pydantic requirement)
Category.update_forward_refs()
