from Category import Category


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
    root = Category(code="root",
                    level=0,
                    name="All Categories",
                    description="Root category for all classifications")

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
        lvl1_cat = Category(code=lvl1_code,
                            name=lvl1_name,
                            level=1,
                            description=f"{lvl1_name} category")

        for j, lvl2_name in enumerate(level2_names[lvl1_name], start=1):
            lvl2_code = f"{lvl1_code}.{j}"
            lvl2_cat = Category(code=lvl2_code,
                                name=lvl2_name,
                                level=2,
                                description=f"{lvl2_name} subcategory under {lvl1_name}")

            for k, lvl3_name in enumerate(level3_names, start=1):
                lvl3_code = f"{lvl2_code}.{k}"
                lvl3_cat = Category(code=lvl3_code,
                                    name=lvl3_name,
                                    level=3,
                                    description=f"{lvl3_name} grade for {lvl2_name}")

                # Level 4: One child for each level 3 node
                lvl4_name = level4_mapping[lvl3_name]
                lvl4_code = f"{lvl3_code}.1"
                lvl4_cat = Category(code=lvl4_code,
                                    name=lvl4_name,
                                    level=4,
                                    description=f"{lvl4_name} of {lvl3_name} in {lvl2_name}")

                lvl3_cat.add_child(lvl4_cat)
                lvl2_cat.add_child(lvl3_cat)

            lvl1_cat.add_child(lvl2_cat)
        root.add_child(lvl1_cat)

    return root
