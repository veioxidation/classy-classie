# LLM-Powered Multi-Level Classification System

## Overview

This project implements a multi-level classification system for invoice line items. It is designed to work with complex, tree-like hierarchies of categories. The system supports two major approaches for classification:

- **LLM Prompt-Template Based Classification:**  
  Leverages OpenAI’s language models (via LangChain) to classify items based on a prompt template. The algorithm recursively selects the most appropriate subcategory at each level, producing a full classification path along with a confidence score and any warning messages if the decision is ambiguous.

- **Vector-Based Classification (via Chroma DB):**  
  Converts the hierarchical category tree into vector embeddings (using OpenAIEmbeddings) and stores these in a Chroma vector store. This allows similarity search with metadata filters (e.g., by category level or parent path) to find the best matching category.

Additionally, the system includes:

- **Recursive Classification:**  
  Starting at a single root category, the algorithm traverses the hierarchy level by level until it reaches a leaf node.
  
- **Hierarchical ASCII Tree Visualization:**  
  The `Category` data model includes an `ascii_tree()` method to generate an easy-to-read ASCII tree representation of the hierarchy.

## Capabilities

- **Multi-Level Recursive Classification:**  
  Automatically determines the classification path by traversing from the root ("All Categories") to the leaf nodes.
  
- **Modular Classifier Architecture:**  
  Easily switch between different classification methods (e.g., LLM-based or vector-based) by implementing a common classifier interface.
  
- **Confidence & Ambiguity Reporting:**  
  Returns a confidence score for the classification and warns when multiple candidate categories are similarly matched.
  
- **Vector Store Integration:**  
  Leverages Chroma DB and OpenAIEmbeddings to support similarity search on the hierarchical documents.
  
- **Visual Hierarchy Overview:**  
  Generate an ASCII representation of the full category tree for debugging or documentation purposes.



## Examples:
```
Hierarchy:
└─ All Categories (Code: root)
    ├─ Office Supplies (Code: 1)
    │   ├─ Paper Products (Code: 1.1)
    │   │   ├─ Standard (Code: 1.1.1)
    │   │   │   └─ Standard Variant (Code: 1.1.1.1)
    │   │   ├─ Premium (Code: 1.1.2)
    │   │   │   └─ Premium Variant (Code: 1.1.2.1)
    │   │   └─ Economy (Code: 1.1.3)
    │   │       └─ Economy Variant (Code: 1.1.3.1)
    │   ├─ Writing Instruments (Code: 1.2)
    │   │   ├─ Standard (Code: 1.2.1)
    │   │   │   └─ Standard Variant (Code: 1.2.1.1)
    │   │   ├─ Premium (Code: 1.2.2)
    │   │   │   └─ Premium Variant (Code: 1.2.2.1)
    │   │   └─ Economy (Code: 1.2.3)
    │   │       └─ Economy Variant (Code: 1.2.3.1)
    │   ├─ Desk Accessories (Code: 1.3)
    │   │   ├─ Standard (Code: 1.3.1)
    │   │   │   └─ Standard Variant (Code: 1.3.1.1)
    │   │   ├─ Premium (Code: 1.3.2)
    │   │   │   └─ Premium Variant (Code: 1.3.2.1)
    │   │   └─ Economy (Code: 1.3.3)
    │   │       └─ Economy Variant (Code: 1.3.3.1)
    │   └─ Other Office Supplies (Code: 1.4)
    │       ├─ Standard (Code: 1.4.1)
    │       │   └─ Standard Variant (Code: 1.4.1.1)
    │       ├─ Premium (Code: 1.4.2)
    │       │   └─ Premium Variant (Code: 1.4.2.1)
    │       └─ Economy (Code: 1.4.3)
    │           └─ Economy Variant (Code: 1.4.3.1)
    ├─ Electronics (Code: 2)
    │   ├─ Computers (Code: 2.1)
    │   │   ├─ Standard (Code: 2.1.1)
    │   │   │   └─ Standard Variant (Code: 2.1.1.1)
    │   │   ├─ Premium (Code: 2.1.2)
    │   │   │   └─ Premium Variant (Code: 2.1.2.1)
    │   │   └─ Economy (Code: 2.1.3)
    │   │       └─ Economy Variant (Code: 2.1.3.1)
    │   ├─ Mobile Devices (Code: 2.2)
    │   │   ├─ Standard (Code: 2.2.1)
    │   │   │   └─ Standard Variant (Code: 2.2.1.1)
    │   │   ├─ Premium (Code: 2.2.2)
    │   │   │   └─ Premium Variant (Code: 2.2.2.1)
    │   │   └─ Economy (Code: 2.2.3)
    │   │       └─ Economy Variant (Code: 2.2.3.1)
    │   ├─ Peripherals (Code: 2.3)
    │   │   ├─ Standard (Code: 2.3.1)
    │   │   │   └─ Standard Variant (Code: 2.3.1.1)
    │   │   ├─ Premium (Code: 2.3.2)
    │   │   │   └─ Premium Variant (Code: 2.3.2.1)
    │   │   └─ Economy (Code: 2.3.3)
    │   │       └─ Economy Variant (Code: 2.3.3.1)
    │   └─ Audio/Video (Code: 2.4)
    │       ├─ Standard (Code: 2.4.1)
    │       │   └─ Standard Variant (Code: 2.4.1.1)
    │       ├─ Premium (Code: 2.4.2)
    │       │   └─ Premium Variant (Code: 2.4.2.1)
    │       └─ Economy (Code: 2.4.3)
    │           └─ Economy Variant (Code: 2.4.3.1)
    ├─ Furniture (Code: 3)
    │   ├─ Office Chairs (Code: 3.1)
    │   │   ├─ Standard (Code: 3.1.1)
    │   │   │   └─ Standard Variant (Code: 3.1.1.1)
    │   │   ├─ Premium (Code: 3.1.2)
    │   │   │   └─ Premium Variant (Code: 3.1.2.1)
    │   │   └─ Economy (Code: 3.1.3)
    │   │       └─ Economy Variant (Code: 3.1.3.1)
    │   ├─ Desks (Code: 3.2)
    │   │   ├─ Standard (Code: 3.2.1)
    │   │   │   └─ Standard Variant (Code: 3.2.1.1)
    │   │   ├─ Premium (Code: 3.2.2)
    │   │   │   └─ Premium Variant (Code: 3.2.2.1)
    │   │   └─ Economy (Code: 3.2.3)
    │   │       └─ Economy Variant (Code: 3.2.3.1)
    │   ├─ Storage (Code: 3.3)
    │   │   ├─ Standard (Code: 3.3.1)
    │   │   │   └─ Standard Variant (Code: 3.3.1.1)
    │   │   ├─ Premium (Code: 3.3.2)
    │   │   │   └─ Premium Variant (Code: 3.3.2.1)
    │   │   └─ Economy (Code: 3.3.3)
    │   │       └─ Economy Variant (Code: 3.3.3.1)
    │   └─ Meeting Room Furniture (Code: 3.4)
    │       ├─ Standard (Code: 3.4.1)
    │       │   └─ Standard Variant (Code: 3.4.1.1)
    │       ├─ Premium (Code: 3.4.2)
    │       │   └─ Premium Variant (Code: 3.4.2.1)
    │       └─ Economy (Code: 3.4.3)
    │           └─ Economy Variant (Code: 3.4.3.1)
    └─ Clothing (Code: 4)
        ├─ Men's Wear (Code: 4.1)
        │   ├─ Standard (Code: 4.1.1)
        │   │   └─ Standard Variant (Code: 4.1.1.1)
        │   ├─ Premium (Code: 4.1.2)
        │   │   └─ Premium Variant (Code: 4.1.2.1)
        │   └─ Economy (Code: 4.1.3)
        │       └─ Economy Variant (Code: 4.1.3.1)
        ├─ Women's Wear (Code: 4.2)
        │   ├─ Standard (Code: 4.2.1)
        │   │   └─ Standard Variant (Code: 4.2.1.1)
        │   ├─ Premium (Code: 4.2.2)
        │   │   └─ Premium Variant (Code: 4.2.2.1)
        │   └─ Economy (Code: 4.2.3)
        │       └─ Economy Variant (Code: 4.2.3.1)
        ├─ Children's Wear (Code: 4.3)
        │   ├─ Standard (Code: 4.3.1)
        │   │   └─ Standard Variant (Code: 4.3.1.1)
        │   ├─ Premium (Code: 4.3.2)
        │   │   └─ Premium Variant (Code: 4.3.2.1)
        │   └─ Economy (Code: 4.3.3)
        │       └─ Economy Variant (Code: 4.3.3.1)
        └─ Accessories (Code: 4.4)
            ├─ Standard (Code: 4.4.1)
            │   └─ Standard Variant (Code: 4.4.1.1)
            ├─ Premium (Code: 4.4.2)
            │   └─ Premium Variant (Code: 4.4.2.1)
            └─ Economy (Code: 4.4.3)
                └─ Economy Variant (Code: 4.4.3.1)

```

## Sample results:

```
=== Test Line Items and Expected Classification Paths ===
Line Item: 'High quality standard paper reams'
  Expected Path: ['Office Supplies', 'Paper Products', 'Standard', 'Standard Variant']
  Result: ['Office Supplies', 'Paper Products', 'Premium', 'Premium Variant']
Line Item: 'Premium fountain pen'
  Expected Path: ['Office Supplies', 'Writing Instruments', 'Premium', 'Premium Variant']
  Result: ['Office Supplies', 'Writing Instruments', 'Premium', 'Premium Variant']
Line Item: 'Economy desk organizer'
  Expected Path: ['Office Supplies', 'Desk Accessories', 'Economy', 'Economy Variant']
  Result: ['Office Supplies', 'Desk Accessories', 'Economy', 'Economy Variant']
Line Item: 'Assorted office misc supplies'
  Expected Path: ['Office Supplies', 'Other Office Supplies', 'Standard', 'Standard Variant']
  Result: ['Office Supplies', 'Other Office Supplies', 'Standard', 'Standard Variant']
Line Item: 'Latest model laptop'
  Expected Path: ['Electronics', 'Computers', 'Premium', 'Premium Variant']
  Result: ['Electronics', 'Computers', 'Premium', 'Premium Variant']
Line Item: 'Budget smartphone'
  Expected Path: ['Electronics', 'Mobile Devices', 'Economy', 'Economy Variant']
  Result: ['Electronics', 'Mobile Devices', 'Economy', 'Economy Variant']
Line Item: 'High fidelity headphones'
  Expected Path: ['Electronics', 'Audio/Video', 'Premium', 'Premium Variant']
  Result: ['Electronics', 'Audio/Video', 'Premium', 'Premium Variant']
Line Item: 'USB hub for multiple devices'
  Expected Path: ['Electronics', 'Peripherals', 'Standard', 'Standard Variant']
  Result: ['Electronics', 'Peripherals', 'Standard', 'Standard Variant']
Line Item: 'Ergonomic office chair'
  Expected Path: ['Furniture', 'Office Chairs', 'Premium', 'Premium Variant']
  Result: ['Furniture', 'Office Chairs', 'Premium', 'Premium Variant']
Line Item: 'Modern standing desk'
  Expected Path: ['Furniture', 'Desks', 'Standard', 'Standard Variant']
  Result: ['Furniture', 'Desks', 'Premium', 'Premium Variant']
Line Item: 'Modular storage cabinet'
  Expected Path: ['Furniture', 'Storage', 'Economy', 'Economy Variant']
  Result: ['Furniture', 'Storage', 'Premium', 'Premium Variant']
Line Item: 'Large conference table'
  Expected Path: ['Furniture', 'Meeting Room Furniture', 'Standard', 'Standard Variant']
  Result: ['Furniture', 'Meeting Room Furniture', 'Premium', 'Premium Variant']
Line Item: 'Men's casual shirt'
  Expected Path: ['Clothing', "Men's Wear", 'Standard', 'Standard Variant']
  Result: ['Clothing', "Men's Wear", 'Standard', 'Standard Variant']
Line Item: 'Elegant women's dress'
  Expected Path: ['Clothing', "Women's Wear", 'Premium', 'Premium Variant']
  Result: ['Clothing', "Women's Wear", 'Premium', 'Premium Variant']
Line Item: 'Comfortable children's playwear'
  Expected Path: ['Clothing', "Children's Wear", 'Economy', 'Economy Variant']
  Result: ['Clothing', "Children's Wear", 'Standard', 'Standard Variant']
Line Item: 'Designer sunglasses'
  Expected Path: ['Clothing', 'Accessories', 'Premium', 'Premium Variant']
  Result: ['Clothing', 'Accessories', 'Premium', 'Premium Variant']
Line Item: 'Eco-friendly recycled paper'
  Expected Path: ['Office Supplies', 'Paper Products', 'Economy', 'Economy Variant']
  Result: ['Office Supplies', 'Paper Products', 'Standard', 'Standard Variant']
Line Item: 'Stylish ballpoint pen'
  Expected Path: ['Office Supplies', 'Writing Instruments', 'Standard', 'Standard Variant']
  Result: ['Office Supplies', 'Writing Instruments', 'Premium', 'Premium Variant']
Line Item: 'Compact desktop computer'
  Expected Path: ['Electronics', 'Computers', 'Economy', 'Economy Variant']
  Result: ['Electronics', 'Computers', 'Standard', 'Standard Variant']
Line Item: 'Wireless speaker system'
  Expected Path: ['Electronics', 'Audio/Video', 'Standard', 'Standard Variant']
  Result: ['Electronics', 'Audio/Video', 'Premium', 'Premium Variant']
```