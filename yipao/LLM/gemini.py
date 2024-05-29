import google.generativeai as genai
from .customllm import CustomLLM

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
        
        return response.text
    
