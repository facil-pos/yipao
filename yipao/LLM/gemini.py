import google.generativeai as genai
from .customllm import CustomLLM
from typing import Dict

class GoogleGenAi(CustomLLM):
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
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model, **cfg)
        self.config = genai.GenerationConfig(temperature=temperature)
        self.total = {
            "Total_tokens_inputs": 0,
            "Total_tokens_outputs": 0,
        }



    def invoke(self, prompt) -> str:
        """
        Submit a prompt to the model for generating a response.

        Parameters:
            prompt (str): The prompt parameter.

        Returns:
            str: The generated response from the model.
        """
        self.validate_prompt(prompt)

        response = self.model.generate_content(prompt,
                                               generation_config=self.config)
        
        countTokensResp_input = self.count_tokens(prompt)
        self.total["Total_tokens_inputs"] += countTokensResp_input
        countTokensResp_output = self.count_tokens(response.text)
        self.total["Total_tokens_outputs"] += countTokensResp_output

        return response.text, countTokensResp_input, countTokensResp_output

    def count_tokens(self, prompt: str) -> int:
        """
        Counts the number of tokens in a prompt.

        Args:
            prompt (str): The prompt whose tokens are to be counted.

        Returns:
            int: The number of tokens in the prompt.
        """
        countTokensResp = self.model.count_tokens(prompt)
        return countTokensResp.total_tokens


    def monitor(self) -> Dict[str, int]:
        """
        Provides the total count of input and output tokens processed.

        Returns:
            Dict[str, int]: A dictionary containing the total tokens counted for inputs and outputs.
        """
        return self.total
