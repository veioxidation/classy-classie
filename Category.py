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

    def ascii_tree(self, prefix: str = "", is_last: bool = True) -> str:
        """
        Recursively generate an ASCII tree overview of the hierarchy.

        Parameters:
          - prefix: a string used to format the tree structure (for recursion).
          - is_last: a boolean indicating if this node is the last child of its parent.

        Returns:
          A string representing the ASCII tree starting from this Category.
        """
        # Determine the branch marker for the current node.
        branch = "└─ " if is_last else "├─ "
        tree_str = f"{prefix}{branch}{self.name} (Code: {self.code})\n"
        # Prepare the prefix for the children.
        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            tree_str += child.ascii_tree(child_prefix, is_last_child)
        return tree_str

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return f"{self.code} : {self.name} (L{self.level})"
    def __repr__(self):
        return f"{self.code} : {self.name} (L{self.level})"

# Allow self-referencing types (Pydantic requirement)
Category.update_forward_refs()
