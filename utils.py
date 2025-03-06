from Category import Category


def print_hierarchy(node: Category, level: int = 0):
    indent = "  " * level
    print(f"{indent}- {node.name} (Code: {node.code})")
    for child in node.children:
        print_hierarchy(child, level + 1)
