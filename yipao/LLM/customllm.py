class CustomLLM:
    """
    Base class for interacting with generative LLMs.
    """

    def invoke(self, prompt: str) -> str:
        """
        Method to submit a prompt to the model for generating a response. This method
        should be implemented by all subclasses.

        Parameters:
            prompt (str): The prompt for the LLM.

        Returns:
            str: The generated response from the model.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def validate_prompt(self, prompt: str) -> str:
        """
        Validates the prompt to ensure it is not empty.

        Parameters:
            prompt (str): The prompt to validate.

        Raises:
            ValueError: If the prompt is empty.
        """
        if prompt is None or len(prompt.strip()) == 0:
            raise ValueError("Prompt cannot be empty.")


    def count_tokens(self, prompt: str) -> int:
        """
        Counts the number of tokens used in a string.

        Parameters:
            prompt (str): The prompt whose tokens are to be counted.

        Returns:
            int: The number of tokens in the string prompt.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")


    def monitor(self):
        """
        Method to monitor the LLM's token usage.
        """
        raise NotImplementedError("Subclasses must implement this method.")