from openai import OpenAI
from .customllm import CustomLLM
from typing import Dict

class OpenAIGPT(CustomLLM):
    """
    Class to handle interactions with OpenAI's GPT models.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 16384):
        """
        Initialize the OpenAI GPT client.

        Parameters:
            api_key (str): The OpenAI API key.
            model (str): The model name (e.g., "gpt-4", "gpt-3.5-turbo"). Default is "gpt-4".
            temperature (float): Sampling temperature to control randomness. Default is 0.7.
            max_tokens (int): The maximum number of tokens to generate. Default is 2048.

        Returns:
            None
        """

        self.client = OpenAI(
            api_key=api_key,  # This is the default and can be omitted
        )
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.total = {
            "Total_tokens_inputs": 0,
            "Total_tokens_outputs": 0,
        }

    def invoke(self, prompt: str) -> str:
        """
        Submit a prompt to the model for generating a response.

        Parameters:
            prompt (str): The prompt for the model.

        Returns:
            str: The generated response from the model.
        """
        self.validate_prompt(prompt)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                    { "role": "system", "content": "You are a helpful assistant, business intelligence and sql expert, your job is to create the best sql queries for the user's question based on the data provided in the user prompt." },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        # Extract the model's response text
        response_text = response.choices[0].message.content

        with open("response_text.txt", "w") as file:
            file.write(response_text)

        # Token usage from the response
        usage = response.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens

        self.total["Total_tokens_inputs"] += input_tokens
        self.total["Total_tokens_outputs"] += output_tokens

        return response_text, input_tokens, output_tokens

    def count_tokens(self, prompt: str) -> int:
        """
        Counts the number of tokens in a prompt. Uses OpenAI's token counting guidelines.

        Parameters:
            prompt (str): The prompt to analyze.

        Returns:
            int: Estimated token count.
        """
        # You can use a tokenizer like tiktoken to estimate token counts (optional dependency)
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(self.model)
            return len(encoding.encode(prompt))
        except ImportError:
            raise RuntimeError("tiktoken is required for token counting. Install it with 'pip install tiktoken'.")

    def monitor(self) -> Dict[str, int]:
        """
        Provides the total count of input and output tokens processed.

        Returns:
            Dict[str, int]: A dictionary containing the total tokens counted for inputs and outputs.
        """
        return self.total