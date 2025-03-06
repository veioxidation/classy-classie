from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from Category import Category
from langchain_core.prompts import PromptTemplate


class ClassificationResult(BaseModel):
    selected_index: int = Field(description="an integer representing the chosen candidate\'s number (0-indexed)")
    confidence: int = Field(
        description="a float between 0 and 1 indicating your confidence level in this classification")
    warning: str = Field(
        description="a string containing a warning message if the classification is ambiguous, or an empty string if not")


class BaseClassifier(ABC):
    @abstractmethod
    def classify(
            self, line_item: str, candidates: List[Category]
    ) -> Tuple[Category, float, Optional[str]]:
        """
        Given the invoice line item text and a list of candidate categories, return:
          - The selected category,
          - A confidence score between 0 and 1,
          - A warning message if multiple candidates are similarly likely.
        """
        pass


class VectorClassifier(BaseClassifier):
    def __init__(self, vectorstore: Chroma):
        # In a real implementation, initialize your vector database or embedding model here.
        self.vectorstore = vectorstore

    def classify(
            self, line_item: str, candidates: List[Category]
    ) -> Tuple[Category, float, Optional[str]]:
        target_level = candidates[0].level
        parent_item = candidates[0].parent
        parent_level = parent_item.level
        try:
            results = self.vectorstore.similarity_search_with_score(query=line_item,
                                                                    k=1,
                                                                    filter={"$and":
                                                                        [
                                                                            {f"L{parent_level}": {
                                                                                "$eq": parent_item.name}},
                                                                            {f"level": {"$eq": target_level}}]
                                                                    })

            # Document result
            best_candidate = results[0][0].metadata['name']
            result_idx = [x.name == best_candidate for x in candidates].index(True)
            confidence = 1.0
            warning = ""
        except Exception as e:
            best_candidate = None
            result_idx = -1
            warning = str(e)
            confidence = 0.0

        # TODO: Implement mechanism as a next step.
        # Check if any other candidate has a similarity within a small margin (e.g. 0.05) of the best.
        # similar_count = sum(
        #     1 for sim in similarities if abs(sim - best_similarity) < 0.05 and sim != best_similarity
        # )
        # if similar_count > 0:
        #     warning = "Multiple candidates have similar similarity scores. Manual review recommended."
        return candidates[result_idx], confidence, warning


# === LangChain-based LLM Prompt Template Classifier ===
class LangChainLLMClassifier(BaseClassifier):
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0.0):
        """
        Initialize with a specific LLM via LangChain.
        """
        self.model = init_chat_model(model_name, model_provider="openai")
        self.parser = JsonOutputParser(pydantic_object=ClassificationResult)
        self.prompt_template = PromptTemplate(
            input_variables=["line_item", "candidates_text"],

            template=(
                "You are a classification expert. Given the following invoice line item:\n\n"
                "Line item: \"{line_item}\"\n\n"
                "And the following candidate categories:\n"
                "{candidates_text}\n\n"
                "Please select the candidate category that best matches the invoice line item.\n"
                "{format_instructions}"
            ),
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )

    def classify(
            self, line_item: str, candidates: List[Category]
    ) -> Tuple[Category, float, Optional[str]]:
        # Build a numbered candidate list
        candidate_lines = []
        for idx, candidate in enumerate(candidates, start=1):
            desc = candidate.description if candidate.description else candidate.name
            candidate_lines.append(f"{idx}. Code: {candidate.code}, Name: {candidate.name}, Description: {desc}")
        candidates_text = "\n".join(candidate_lines)

        try:
            chain = self.prompt_template | self.model | self.parser
            response = chain.invoke(input=dict(line_item=line_item,
                                               candidates_text=candidates_text))

            selected_index = response.get("selected_index")
            confidence = response.get("confidence")
            warning = response.get("warning")

            if not (isinstance(selected_index, int) and 0 <= selected_index <= len(candidates)):
                raise ValueError("Invalid selected_index returned by the LLM.")

            selected_candidate = candidates[selected_index]
            return selected_candidate, confidence, warning if warning else None

        except Exception as e:
            # Fallback in case of error
            print(f"Error during LangChain classification: {e}. Falling back to default candidate.")
            return candidates[0], 0.5, "Fallback due to error."


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
