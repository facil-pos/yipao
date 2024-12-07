import os
from langchain_groq import ChatGroq
from .customllm import CustomLLM
from typing import Dict

class GroqLLm(CustomLLM):
    """
    Class to handle interactions with Google's generative AI models.
    """
    def __init__(self, model, api_key, temperature = 0.1, **cfg):
        """
        Initialize the class with an optional config parameter.

        Parameters:
            config (any): The configuration parameter.

        Returns:
            None
        """
        self.model = ChatGroq(temperature=temperature, groq_api_key=api_key, model_name=model) 

    def invoke(self, prompt) -> str:
        """
        Submit a prompt to the model for generating a response.

        Parameters:
            prompt (str): The prompt parameter.

        Returns:
            str: The generated response from the model.
        """
        self.validate_prompt(prompt)

        response = self.model.invoke(prompt)

        return response

    #def count_tokens(self, prompt: str) -> int:
    #    """
    #    Counts the number of tokens in a prompt.

    #    Args:
    #        prompt (str): The prompt whose tokens are to be counted.

    #    Returns:
    #        int: The number of tokens in the prompt.
    #    """
    #    countTokensResp = self.model.count_tokens(prompt)
    #    return countTokensResp.total_tokens


    #def monitor(self) -> Dict[str, int]:
    #    """
    #    Provides the total count of input and output tokens processed.

    #    Returns:
    #        Dict[str, int]: A dictionary containing the total tokens counted for inputs and outputs.
    #    """
    #    return self.total
