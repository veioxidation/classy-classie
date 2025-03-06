from typing import Optional, List

from pydantic import BaseModel


class Category(BaseModel):
    code: str
    name: str
    level: int
    description: Optional[str] = None
    children: List["Category"] = []  # recursively defined list of children
    parent: Optional["Category"] = None  # recursively defined list of children

    def add_child(self, child: "Category"):
        # Avoid duplicate children
        if all(child.code != existing.code for existing in self.children):
            self.children.append(child)
            child.parent = self

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return f"{self.code} : {self.name} (L{self.level})"
    def __repr__(self):
        return f"{self.code} : {self.name} (L{self.level})"

# Allow self-referencing types (Pydantic requirement)
Category.update_forward_refs()
