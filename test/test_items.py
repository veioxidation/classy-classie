# =============================================================================
# 3. Prepare Test Line Items with Expected Results
# =============================================================================
from typing import Dict, List


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
        "Budget smartphone": ["Electronics", "Mobile Devices", "Economy", "Economy Variant"],
        "High fidelity headphones": ["Electronics", "Audio/Video", "Premium", "Premium Variant"],
        "USB hub for multiple devices": ["Electronics", "Peripherals", "Standard", "Standard Variant"],
        "Ergonomic office chair": ["Furniture", "Office Chairs", "Premium", "Premium Variant"],
        "Modern standing desk": ["Furniture", "Desks", "Standard", "Standard Variant"],
        "Modular storage cabinet": ["Furniture", "Storage", "Economy", "Economy Variant"],
        "Large conference table": ["Furniture", "Meeting Room Furniture", "Standard", "Standard Variant"],
        "Men's casual shirt": ["Clothing", "Men's Wear", "Standard", "Standard Variant"],
        "Elegant women's dress": ["Clothing", "Women's Wear", "Premium", "Premium Variant"],
        "Comfortable children's playwear": ["Clothing", "Children's Wear", "Economy", "Economy Variant"],
        "Designer sunglasses": ["Clothing", "Accessories", "Premium", "Premium Variant"],
        "Eco-friendly recycled paper": ["Office Supplies", "Paper Products", "Economy", "Economy Variant"],
        "Stylish ballpoint pen": ["Office Supplies", "Writing Instruments", "Standard", "Standard Variant"],
        "Compact desktop computer": ["Electronics", "Computers", "Economy", "Economy Variant"],
        "Wireless speaker system": ["Electronics", "Audio/Video", "Standard", "Standard Variant"],
    }
    return test_cases
