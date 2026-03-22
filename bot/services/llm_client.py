"""LLM client for intent routing.

Uses OpenRouter-compatible API to call LLM with tool definitions.
"""

import json
import httpx
from typing import Any, Optional


class LLMClient:
    """Client for calling LLM with tool definitions."""

    def __init__(self, api_base: str, api_key: str, model: str):
        self.api_base = api_base.rstrip("/")
        self.api_key = api_key
        self.model = model
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        """Get or create HTTP client with auth headers."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.api_base,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=30.0,
            )
        return self._client

    def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        max_iterations: int = 5,
    ) -> str:
        """Chat with LLM, executing tool calls and feeding results back.
        
        Args:
            messages: Conversation history with role/content
            tools: List of tool schemas
            max_iterations: Maximum tool call iterations
            
        Returns:
            Final response text
        """
        import sys
        
        for iteration in range(max_iterations):
            client = self._get_client()
            
            # Call LLM
            payload = {
                "model": self.model,
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto",
            }
            
            response = client.post("/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("choices"):
                return "LLM returned no response."
            
            choice = data["choices"][0]
            message = choice.get("message", {})
            
            # Check if LLM wants to call tools
            tool_calls = message.get("tool_calls", [])
            
            if not tool_calls:
                # LLM is done - return the response
                return message.get("content", "No response generated.")
            
            # Add the assistant's message with tool calls to history
            messages.append({
                "role": "assistant",
                "content": message.get("content"),
                "tool_calls": tool_calls,
            })
            
            # Execute each tool call
            for tool_call in tool_calls:
                func = tool_call.get("function", {})
                tool_name = func.get("name", "")
                tool_args_str = func.get("arguments", "{}")
                
                try:
                    tool_args = json.loads(tool_args_str) if tool_args_str else {}
                except json.JSONDecodeError:
                    tool_args = {}
                
                print(f"[tool] LLM called: {tool_name}({tool_args})", file=sys.stderr)
                
                # Execute the tool (will be set by caller)
                # This is a callback pattern - caller provides tool execution
        
        return "Maximum iterations reached."

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            self._client.close()
            self._client = None
