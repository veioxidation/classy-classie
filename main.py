from Category import Category
from classifiers import LangChainLLMClassifier, recursive_classify

from dotenv import load_dotenv

from test.hierarchy_build import build_full_hierarchy
from test.test_items import get_test_line_items

load_dotenv()

# === 6. Example Usage ===
if __name__ == "__main__":
    # For demonstration purposes, we create a small hierarchy manually.
    # In a real application, you would call load_hierarchy_from_excel("path_to_file.xlsx")
    # Example candidate categories (in practice, these would be extracted from your hierarchy)
    # Create an instance of the LangChain-based classifier
    # Build the hierarchy
    classifier = LangChainLLMClassifier(model_name="gpt-4o-mini",
                                        temperature=0.0)
    hierarchy_roots: Category = build_full_hierarchy()

    # Print the ASCII tree overview of the hierarchy.
    print("Hierarchy:")
    print(hierarchy_roots.ascii_tree(prefix="", is_last=True))


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
