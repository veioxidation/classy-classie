from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

from Category import Category
from test.hierarchy_build import build_full_hierarchy



def hierarchy_to_documents(category: Category, parent_path: List[str] = None) -> List[Document]:
    """
    Recursively traverse the Category hierarchy and convert each category to a Document.

    Metadata includes:
      - "level": the depth of the category (0 for the root)
      - "code": the category code
      - "L0", "L1", ... representing the parent category names along the path.
    """
    if parent_path is None:
        parent_path = []
    # The current level is the length of the parent path.
    current_level = len(parent_path)

    # Build metadata including parent's path
    metadata = {"level": current_level, "code": category.code, 'name': category.name}
    for i, parent in enumerate(parent_path):
        metadata[f"L{i}"] = parent

    # Create the Document for the current category.
    doc = Document(
        page_content=(
            f"Category Name: {category.name}\n"
            f"Code: {category.code}\n"
            f"Description: {category.description}"
        ),
        metadata=metadata
    )
    docs = [doc]

    # Update the parent path for children (include the current category's name)
    new_parent_path = parent_path + [category.name]
    for child in category.children:
        docs.extend(hierarchy_to_documents(child, new_parent_path))
    return docs


# ---------------------------------------------------------------------------
# 3. Load Hierarchy into a Chroma Vector Store
# ---------------------------------------------------------------------------
def get_vector_store(persist_directory: str = "./chroma_langchain_db") -> Chroma:
    # Initialize OpenAIEmbeddings (make sure OPENAI_API_KEY is set in your environment).
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    return Chroma(
        collection_name="categories",
        embedding_function=embeddings,
        persist_directory=persist_directory,  # Where to save data locally, remove if not necessary
    )


def load_hierarchy_into_chroma(root_category: Category,
                               persist_directory: str = "./chroma_langchain_db") -> Chroma:
    """
    Given the root Category, converts the entire hierarchy into a list of Documents,
    creates OpenAIEmbeddings, and initializes a Chroma vector store.

    The persist_directory parameter specifies where the Chroma DB files should be stored.
    """
    # Convert the hierarchy to Document objects.
    docs = hierarchy_to_documents(root_category)

    # Create a Chroma vector store from the documents.
    vectorstore = get_vector_store(persist_directory=persist_directory)

    vectorstore.add_documents(docs)
    return vectorstore


