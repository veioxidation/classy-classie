from dotenv import load_dotenv

from classifiers import VectorClassifier, recursive_classify
from test.hierarchy_build import build_full_hierarchy
from test.test_items import get_test_line_items
from vector_embedding import load_hierarchy_into_chroma, get_vector_store

load_dotenv()

# === 6. Example Usage ===
if __name__ == "__main__":
    # For demonstration purposes, we create a small hierarchy manually.
    # In a real application, you would call load_hierarchy_from_excel("path_to_file.xlsx")
    # Example candidate categories (in practice, these would be extracted from your hierarchy)
    # Create an instance of the LangChain-based classifier
    # Build the hierarchy
    # getting hierarchy
    hierarchy_roots = build_full_hierarchy()
    BUILD_HIERARCHY = True
    if BUILD_HIERARCHY:
        # hierarchy_to_documents
        vectorstore = load_hierarchy_into_chroma(hierarchy_roots)
    else:
        vectorstore = get_vector_store()

    classifier = VectorClassifier(vectorstore=vectorstore)

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


    # results = vectorstore.similarity_search_with_score(
    #     query = "A4 white paper ream",
    #     k=1,
    #     filter = {'level':1}
    # )

    print("Documents at level 1:")

