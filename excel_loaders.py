# === Excel Loader for Hierarchical Levels ===
import math
import pandas as pd
from typing import List, Tuple, Dict

from Category import Category

def load_hierarchy_from_excel_levels(file_path: str) -> List[Category]:
    """
    Loads an Excel file where each row contains columns L1, L2, L3, ... Ln representing
    a full path in the hierarchy. Returns a list of root Category objects.
    """
    df = pd.read_excel(file_path)

    # Identify all columns that represent levels, e.g., L1, L2, L3, etc.
    level_columns = sorted([col for col in df.columns if col.startswith("L")],
                           key=lambda x: int(x[1:]) if x[1:].isdigit() else math.inf)

    # Dictionary to hold nodes keyed by the tuple representing the path
    tree_dict: Dict[Tuple[str, ...], Category] = {}
    # Dictionary to track root nodes (first-level keys)
    roots: Dict[str, Category] = {}

    for _, row in df.iterrows():
        path = []
        parent = None
        for level in level_columns:
            cell = row[level]
            if pd.isna(cell):
                # Stop at the first missing value: path ended.
                break
            cell_value = str(cell).strip()
            path.append(cell_value)
            key = tuple(path)

            if key not in tree_dict:
                # For simplicity, we use the cell value for both code and name.
                new_cat = Category(code=cell_value, name=cell_value, children=[])
                tree_dict[key] = new_cat

                if parent:
                    parent.add_child(new_cat)
                else:
                    # This is a root node (first level)
                    roots[cell_value] = new_cat
            # Update the parent for the next level down
            parent = tree_dict[key]

    # Return the list of root categories
    return list(roots.values())


def load_hierarchy_from_excel(file_path: str) -> List[Category]:
    df = pd.read_excel(file_path)
    # Create a mapping from code to Category
    categories: Dict[str, Category] = {}
    for _, row in df.iterrows():
        code = row["Code"]
        name = row["Name"]
        description = row.get("Description", None)
        categories[code] = Category(code=code, name=name, description=description, children=[])
    # Build the tree by linking children to their parents.
    roots = []
    for _, row in df.iterrows():
        code = row["Code"]
        parent_code = row["ParentCode"]
        if pd.isna(parent_code):
            roots.append(categories[code])
        else:
            parent = categories.get(parent_code)
            if parent:
                parent.children.append(categories[code])
            else:
                # If the parent is not found, treat this category as a root.
                roots.append(categories[code])
    return roots
