from abc import ABC, abstractmethod
import openai
import json
from typing import List, Tuple, Optional

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from Category import Category
import numpy as np
from langchain_core.prompts import PromptTemplate


class ClassificationResult(BaseModel):
    selected_index: int = Field(description="an integer representing the chosen candidate\'s number (0-indexed)")
    confidence: int = Field(description="a float between 0 and 1 indicating your confidence level in this classification")
    warning: str = Field(description="a string containing a warning message if the classification is ambiguous, or an empty string if not")

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


class LLMClassifier(BaseClassifier):
    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.0):
        """
        Initialize with the desired model and temperature settings.
        """
        self.model = model
        self.temperature = temperature

    def classify(
            self, line_item: str, candidates: List[Category]
    ) -> Tuple[Category, float, Optional[str]]:
        # Build a numbered candidate list
        candidate_lines = []
        for idx, candidate in enumerate(candidates, start=1):
            desc = candidate.description if candidate.description else candidate.name
            candidate_lines.append(f"{idx}. Code: {candidate.code}, Name: {candidate.name}, Description: {desc}")
        candidate_text = "\n".join(candidate_lines)

        # Build the prompt for the LLM
        prompt = f"""You are a classification expert. Given the following invoice line item:

Line item: "{line_item}"

And the following candidate categories:
{candidate_text}

Please select the candidate category that best matches the invoice line item.
Output your answer in a strict JSON format with the following keys:
- "selected_index": an integer representing the chosen candidate's number (1-indexed)
- "confidence": a float between 0 and 1 indicating your confidence level in this classification
- "warning": a string containing a warning message if the classification is ambiguous, or an empty string if not.

Only output the JSON object, nothing else.
"""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that classifies invoice line items."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
            )
            # Extract the response content
            message_content = response["choices"][0]["message"]["content"].strip()
            # Parse the JSON response
            result = json.loads(message_content)

            selected_index = result.get("selected_index")
            confidence = result.get("confidence")
            warning = result.get("warning")

            if not (isinstance(selected_index, int) and 1 <= selected_index <= len(candidates)):
                raise ValueError("Invalid selected_index returned.")

            selected_candidate = candidates[selected_index - 1]
            return selected_candidate, confidence, warning if warning else None

        except Exception as e:
            # Fallback in case of any error
            print(f"Error during OpenAI classification: {e}. Falling back to default candidate.")
            return candidates[0], 0.5, "Fallback due to error."


class VectorClassifier(BaseClassifier):
    def __init__(self):
        # In a real implementation, initialize your vector database or embedding model here.
        pass

    def compute_embedding(self, text: str) -> np.ndarray:
        # In practice, replace this dummy function with your actual embedding model.
        # For example, using a pretrained sentence transformer.
        # Here we simulate by using the length of the text as a one-dimensional embedding.
        return np.array([float(len(text))])

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def classify(
            self, line_item: str, candidates: List[Category]
    ) -> Tuple[Category, float, Optional[str]]:
        line_embedding = self.compute_embedding(line_item)
        similarities = []
        for candidate in candidates:
            # Use the candidate's description if available; otherwise, fall back to the name.
            candidate_text = candidate.description if candidate.description else candidate.name
            candidate_embedding = self.compute_embedding(candidate_text)
            sim = self.cosine_similarity(line_embedding, candidate_embedding)
            similarities.append(sim)
        best_idx = np.argmax(similarities)
        best_candidate = candidates[best_idx]
        best_similarity = similarities[best_idx]
        confidence = best_similarity  # This is a dummy mapping; refine as needed.
        warning = None
        # Check if any other candidate has a similarity within a small margin (e.g. 0.05) of the best.
        similar_count = sum(
            1 for sim in similarities if abs(sim - best_similarity) < 0.05 and sim != best_similarity
        )
        if similar_count > 0:
            warning = "Multiple candidates have similar similarity scores. Manual review recommended."
        return best_candidate, confidence, warning


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
            raise e
            return candidates[0], 0.5, "Fallback due to error."
