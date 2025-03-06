from typing import List, Optional, Tuple, Dict

from Category import Category
from classifiers import BaseClassifier, LangChainLLMClassifier

from dotenv import load_dotenv

load_dotenv()

# === 1. Define the Category Data Model ===
# We use Pydantic to create a self-referencing data class for the category tree.

# === 5. Recursive Classification Function ===
def recursive_classify(
    line_item: str, category: Category, classifier: BaseClassifier
) -> List[Tuple[Category, float, Optional[str]]]:
    """
    Recursively classify the invoice line item by traversing the category tree.
    Returns a list of tuples (Category, confidence, warning) representing the classification path.
    """
    classification_path = []
    # If the current category has children, perform classification among them.
    if category.children:
        selected_category, confidence, warning = classifier.classify(line_item, category.children)
        classification_path.append((selected_category, confidence, warning))
        # Continue recursively down the tree.
        classification_path.extend(recursive_classify(line_item, selected_category, classifier))
    return classification_path


def build_full_hierarchy() -> Category:
    """
    Build a synthetic 4-level hierarchy with around 100+ categories, under a single root.

    Structure:
      - Level 0 (Root): "All Categories"
      - Level 1: 4 categories (e.g. Office Supplies, Electronics, Furniture, Clothing)
      - Level 2: For each level1, 4 subcategories.
      - Level 3: For each level2, 3 subcategories (Standard, Premium, Economy)
      - Level 4: For each level3, a single child (with a "Variant" suffix)

    Total nodes = 1 (root) + 4 + 16 + 48 + 48 = 117 categories.
    """
    # Create the top-level root category
    root = Category(code="root", name="All Categories", description="Root category for all classifications")

    # Define names for level 1
    level1_names = ["Office Supplies", "Electronics", "Furniture", "Clothing"]

    # Define level 2 names for each level 1 category
    level2_names = {
        "Office Supplies": ["Paper Products", "Writing Instruments", "Desk Accessories", "Other Office Supplies"],
        "Electronics": ["Computers", "Mobile Devices", "Peripherals", "Audio/Video"],
        "Furniture": ["Office Chairs", "Desks", "Storage", "Meeting Room Furniture"],
        "Clothing": ["Men's Wear", "Women's Wear", "Children's Wear", "Accessories"],
    }

    # Level 3 names and corresponding level 4 variants
    level3_names = ["Standard", "Premium", "Economy"]
    level4_mapping = {
        "Standard": "Standard Variant",
        "Premium": "Premium Variant",
        "Economy": "Economy Variant"
    }

    # Build the hierarchy for each level 1 category
    for i, lvl1_name in enumerate(level1_names, start=1):
        lvl1_code = f"{i}"
        lvl1_cat = Category(code=lvl1_code, name=lvl1_name, description=f"{lvl1_name} category")

        for j, lvl2_name in enumerate(level2_names[lvl1_name], start=1):
            lvl2_code = f"{lvl1_code}.{j}"
            lvl2_cat = Category(code=lvl2_code, name=lvl2_name,
                                description=f"{lvl2_name} subcategory under {lvl1_name}")

            for k, lvl3_name in enumerate(level3_names, start=1):
                lvl3_code = f"{lvl2_code}.{k}"
                lvl3_cat = Category(code=lvl3_code, name=lvl3_name, description=f"{lvl3_name} grade for {lvl2_name}")

                # Level 4: One child for each level 3 node
                lvl4_name = level4_mapping[lvl3_name]
                lvl4_code = f"{lvl3_code}.1"
                lvl4_cat = Category(code=lvl4_code, name=lvl4_name,
                                    description=f"{lvl4_name} of {lvl3_name} in {lvl2_name}")

                lvl3_cat.add_child(lvl4_cat)
                lvl2_cat.add_child(lvl3_cat)

            lvl1_cat.add_child(lvl2_cat)
        root.add_child(lvl1_cat)

    return root


# Utility function to print the hierarchy recursively.
def print_hierarchy(node: Category, level: int = 0):
    indent = "  " * level
    print(f"{indent}- {node.name} (Code: {node.code})")
    for child in node.children:
        print_hierarchy(child, level + 1)

# =============================================================================
# 3. Prepare Test Line Items with Expected Results
# =============================================================================
def get_test_line_items() -> Dict[str, List[str]]:
    """
    Return a dictionary mapping sample line item texts to their expected classification
    path (list of category names from level1 to level4).
    """
    # Here we manually define 20 test cases.
    # The expected path is defined as [Level1, Level2, Level3, Level4].
    test_cases = {
        "High quality standard paper reams": ["Office Supplies", "Paper Products", "Standard", "Standard Variant"],
        "Premium fountain pen": ["Office Supplies", "Writing Instruments", "Premium", "Premium Variant"],
        "Economy desk organizer": ["Office Supplies", "Desk Accessories", "Economy", "Economy Variant"],
        "Assorted office misc supplies": ["Office Supplies", "Other Office Supplies", "Standard", "Standard Variant"],
        "Latest model laptop": ["Electronics", "Computers", "Premium", "Premium Variant"],
        # "Budget smartphone": ["Electronics", "Mobile Devices", "Economy", "Economy Variant"],
        # "High fidelity headphones": ["Electronics", "Audio/Video", "Premium", "Premium Variant"],
        # "USB hub for multiple devices": ["Electronics", "Peripherals", "Standard", "Standard Variant"],
        # "Ergonomic office chair": ["Furniture", "Office Chairs", "Premium", "Premium Variant"],
        # "Modern standing desk": ["Furniture", "Desks", "Standard", "Standard Variant"],
        # "Modular storage cabinet": ["Furniture", "Storage", "Economy", "Economy Variant"],
        # "Large conference table": ["Furniture", "Meeting Room Furniture", "Standard", "Standard Variant"],
        # "Men's casual shirt": ["Clothing", "Men's Wear", "Standard", "Standard Variant"],
        # "Elegant women's dress": ["Clothing", "Women's Wear", "Premium", "Premium Variant"],
        # "Comfortable children's playwear": ["Clothing", "Children's Wear", "Economy", "Economy Variant"],
        # "Designer sunglasses": ["Clothing", "Accessories", "Premium", "Premium Variant"],
        # "Eco-friendly recycled paper": ["Office Supplies", "Paper Products", "Economy", "Economy Variant"],
        # "Stylish ballpoint pen": ["Office Supplies", "Writing Instruments", "Standard", "Standard Variant"],
        # "Compact desktop computer": ["Electronics", "Computers", "Economy", "Economy Variant"],
        # "Wireless speaker system": ["Electronics", "Audio/Video", "Standard", "Standard Variant"],
    }
    return test_cases


# === 6. Example Usage ===
if __name__ == "__main__":
    # For demonstration purposes, we create a small hierarchy manually.
    # In a real application, you would call load_hierarchy_from_excel("path_to_file.xlsx")
    # Example candidate categories (in practice, these would be extracted from your hierarchy)
    # Create an instance of the LangChain-based classifier
    # Build the hierarchy
    classifier = LangChainLLMClassifier(model_name="gpt-4o-mini", temperature=0.0)
    hierarchy_roots = build_full_hierarchy()

    # Prepare test line items with expected classification paths.
    test_line_items = get_test_line_items()
    print("\n=== Test Line Items and Expected Classification Paths ===")
    for line_item, expected_path in test_line_items.items():
        # Classify the line item
        result = recursive_classify(line_item=line_item,
                           category=hierarchy_roots,
                           classifier=classifier)

        result_list = [x[0].name for x in result]

        print(f"Line Item: '{line_item}'")
        print(f"  Expected Path: {expected_path}")
        print(f"  Result: {result_list}")

    # selected_category, confidence, warning = classifier.classify(line_item_text, candidates)

    # print("Selected Category:")
    # print(f"  Code: {selected_category.code}, Name: {selected_category.name}")
    # print(f"Confidence: {confidence}")
    # if warning:
    #     print(f"Warning: {warning}")
    #
