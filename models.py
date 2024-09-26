from typing import Dict, List, Union
from config import config

from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_models import BedrockChat
import os
from dotenv import load_dotenv
import boto3
load_dotenv('../env.env')

class ChatModel:
    def __init__(self, model_name: str, model_kwargs: Dict):
        self.model_config = config["models"][model_name]
        self.model_id = self.model_config["model_id"]
        self.model_kwargs = model_kwargs
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name = 'us-west-2',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.llm = BedrockChat(client = self.client, model_id=self.model_id, model_kwargs=model_kwargs, streaming=True)

    def format_prompt(self, prompt: str) -> Union[str, List[Dict]]:
        """
        Format the input prompt according to the model's requirements.
        """
        model_config = self.model_config
        if model_config.get("input_format") == "text":
            return prompt
        elif model_config.get("input_format") == "list_of_dicts":
            prompt_text = {"type": "text", "text": prompt}
            return [prompt_text]
        else:
            raise ValueError(f"Unsupported input format for model: {self.model_id}")
