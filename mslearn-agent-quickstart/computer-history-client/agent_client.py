"""
Agent Client - Handles interaction with the Microsoft Foundry agent.

This module contains the core logic for connecting to and communicating with
the agent published in Microsoft Foundry. It uses the OpenAI Responses API
to submit prompts and handle responses.
"""

import os
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

# Import Azure Identity and OpenAI client libraries
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class AgentClient:
    """Client for interacting with a Microsoft Foundry agent."""
    
    def __init__(self):
        """Initialize the agent client with authentication and endpoint."""
        self.agent_endpoint = os.getenv("AGENT_ENDPOINT")
        if not self.agent_endpoint:
            raise ValueError("AGENT_ENDPOINT not found in environment variables")

        # Ensure endpoint uses HTTPS and remove any trailing /v1/responses
        if not self.agent_endpoint.startswith("https://"):
            self.agent_endpoint = f"https://{self.agent_endpoint}"
        # self.agent_endpoint = self.agent_endpoint.replace("/v1/responses", "").rstrip("/")
        self.agent_endpoint = os.getenv("AGENT_ENDPOINT").replace("/v1/responses", "")

        logger.info(f"Using agent endpoint: {self.agent_endpoint}")

        # Create OpenAI client authenticated with Azure credentials 
        try:
            self.client = OpenAI(
                api_key=get_bearer_token_provider(
                    DefaultAzureCredential(),
                    "https://ai.azure.com/.default"
                ),
                base_url=self.agent_endpoint,
                default_query={"api-version": "2025-11-15-preview"}
            )
        except Exception as e:
            logger.exception("Failed to initialize OpenAI client.")
            raise e
        
        # Maintain conversation history (last 3 exchanges)
        self.conversation_history: List[Dict[str, Any]] = []
        self.max_history = 3
    
    def send_message(self, user_message: str) -> str:
        """
        Send a message to the agent and return the response.
        
        Args:
            user_message: The text message from the user
            
        Returns:
            The agent's response text
        """
        self.conversation_history.append({"role": "user", "content": user_message})
        
        try:
            logger.info(f"Sending message to agent: {user_message}")
            response = self.client.responses.create(input=self.conversation_history)
            assistant_message = response.output_text

            logger.info(f"Agent response: {assistant_message}")

            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            # Enforce max_history limit
            user_message_count = sum(1 for msg in self.conversation_history if msg.get("role") == "user")
            while user_message_count > self.max_history:
                for i, msg in enumerate(self.conversation_history):
                    if msg.get("role") == "user":
                        self.conversation_history.pop(i)
                        if i < len(self.conversation_history) and self.conversation_history[i].get("role") == "assistant":
                            self.conversation_history.pop(i)
                        user_message_count -= 1
                        break

            return assistant_message

        except Exception as e:
            logger.exception("Error communicating with agent.")
            return "An internal error occurred while communicating with the agent."
    
    def reset_conversation(self):
        """Clear the conversation history."""
        logger.info("Conversation history reset.")
        self.conversation_history = []
