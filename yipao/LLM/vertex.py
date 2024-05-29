import vertexai
from vertexai.generative_models import GenerativeModel
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from typing import Any, Dict, Tuple

from .customllm import CustomLLM

class VertexAiLLM(CustomLLM):
    """
    A specialized class derived from CustomLLM for interfacing with Google's Vertex AI generative models.
    Manages authentication, initialization, and interaction with the Vertex AI platform.

    Attributes:
        model (GenerativeModel): An instance of the generative model from Vertex AI.
        config (Dict[str, Any]): Configuration settings for model generation.
        safety_settings (Dict[str, Any]): Settings to ensure safe content generation.
        total (Dict[str, int]): Tracks the total input and output tokens processed.
    """

    def __init__(
        self,
        model_name: str,
        credential_path: str,
        project: str,
        config: Dict[str, Any],
        safety_settings: Dict[str, Any],
        **kwargs
    ) -> None:
        """
        Initializes the Vertex AI LLM model with necessary configurations and credentials.

        Args:
            model_name (str): The name of the model to be used.
            credential_path (str): Path to the service account JSON file.
            project (str): Google Cloud project identifier.
            config (Dict[str, Any]): Additional configuration parameters for the model.
            safety_settings (Dict[str, Any]): Safety settings to control content generation.
            kwargs: Additional keyword arguments passed to vertexai.init.
        """
        self._init_vertexai(credential_path, project, **kwargs)
        self.model = GenerativeModel(model_name)
        self.config = config
        self.safety_settings = safety_settings
        self.total = {
            "Total_tokens_inputs": 0,
            "Total_tokens_outputs": 0,
        }

    def _init_vertexai(self, credential_path: str, project: str, **kwargs):
        """
        Initializes Vertex AI with the appropriate credentials and project settings.

        Args:
            credential_path (str): Path to the Google Cloud service account JSON file.
            project (str): Google Cloud project identifier.
            kwargs: Additional keyword arguments for initialization.
        """
        credentials = Credentials.from_service_account_file(
            credential_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        if credentials.expired:
            credentials.refresh(Request())
        vertexai.init(project=project, credentials=credentials, **kwargs)
        print('VertexAI initialized')


    def invoke(self, prompt: str) -> Tuple[str, int, int]:
        """
        Generates content based on the input prompt while tracking token usage.

        Args:
            prompt (str): The input prompt for content generation.

        Returns:
            tuple: Generated text, number of tokens in the input prompt, and number of tokens in the generated response.

        Raises:
            ValueError: If the input prompt is empty.
        """
        self.validate_prompt(prompt)
        responses = self.model.generate_content(
            [prompt],
            generation_config=self.config,
            safety_settings=self.safety_settings,
            stream=False,
        )
        countTokensResp_input = self.count_tokens(prompt)
        self.total["Total_tokens_inputs"] += countTokensResp_input
        countTokensResp_output = self.count_tokens(responses.text)
        self.total["Total_tokens_outputs"] += countTokensResp_output

        return responses.text, countTokensResp_input, countTokensResp_output


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
