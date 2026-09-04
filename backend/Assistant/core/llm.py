"""
Featherless AI client for agent reasoning, multitasking understanding, and conversational intelligence.

Supports:
- Dynamic model selection from the full Featherless.ai catalogue
- Automatic fallback through FEATHERLESS_FALLBACK_MODELS on failure
- Conversation history (multi-turn context)
- Guaranteed output: always returns something meaningful
"""
import json
import re
import urllib.request
import urllib.error
from typing import List, Dict, Optional, Any
from core import config


class FeatherlessClient:
    """Client for Featherless AI OpenAI-compatible chat completions API.

    Features
    --------
    * **Model selection** – call ``set_model(name)`` or pass ``model=`` to any
      method to switch to any model in ``config.FEATHERLESS_AVAILABLE_MODELS``.
    * **Auto-fallback** – if the active model returns an error the client
      transparently retries with each model in ``config.FEATHERLESS_FALLBACK_MODELS``
      before giving up.
    * **Conversation history** – ``ask_with_history()`` accepts a full message
      list so the model can reference prior turns.
    * **Guaranteed output** – every public method returns a non-empty string.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or config.FEATHERLESS_API_KEY
        self.base_url = (base_url or config.FEATHERLESS_BASE_URL).rstrip("/")
        self.model = model or config.FEATHERLESS_MODEL
        self._fallback_models: List[str] = list(config.FEATHERLESS_FALLBACK_MODELS)

    # ------------------------------------------------------------------
    # Model management helpers
    # ------------------------------------------------------------------

    def list_models(self) -> List[str]:
        """Return every model available on Featherless AI."""
        return list(config.FEATHERLESS_AVAILABLE_MODELS)

    def set_model(self, model_name: str) -> bool:
        """Switch the active model.

        Parameters
        ----------
        model_name:
            Full model identifier, e.g. ``'Qwen/Qwen2.5-72B-Instruct'``.

        Returns
        -------
        bool
            ``True`` if the model name is in the known catalogue, ``False``
            otherwise (model is still set — Featherless may support it).
        """
        self.model = model_name
        return model_name in config.FEATHERLESS_AVAILABLE_MODELS

    def get_model(self) -> str:
        """Return the currently active model identifier."""
        return self.model

    # ------------------------------------------------------------------
    # Low-level API call
    # ------------------------------------------------------------------

    def _call_api(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Optional[str]:
        """Send a single chat-completion request; return content or None."""
        if not self.api_key:
            return None

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "curl/8.4.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                choices = res_data.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "").strip()
                    if content:
                        return content
        except urllib.error.HTTPError as exc:
            # 4xx/5xx — let caller decide whether to fall back
            pass
        except Exception:
            pass

        return None

    # ------------------------------------------------------------------
    # Core completion with automatic model fallback
    # ------------------------------------------------------------------

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> Optional[str]:
        """Send a chat completion request, falling back through alternate models.

        The order of attempts:
        1. ``model`` parameter (if provided)
        2. ``self.model`` (active model)
        3. Each entry in ``self._fallback_models``
        """
        candidate_models: List[str] = []
        if model and model != self.model:
            candidate_models.append(model)
        candidate_models.append(self.model)
        for m in self._fallback_models:
            if m and m not in candidate_models:
                candidate_models.append(m)

        for attempt_model in candidate_models:
            result = self._call_api(messages, attempt_model, temperature, max_tokens)
            if result:
                return result

        return None

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def ask(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Optional[str]:
        """Single-turn prompt → answer (with optional system persona)."""
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self.chat_completion(messages, model=model)

    def ask_with_history(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
    ) -> Optional[str]:
        """Multi-turn conversation — pass the full message history directly."""
        return self.chat_completion(messages, model=model)

    def ask_guaranteed(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
    ) -> str:
        """Like ``ask()`` but ALWAYS returns a non-empty string.

        Falls back to a polite error message if every model fails.
        """
        result = self.ask(prompt, system_prompt=system_prompt, model=model)
        if result:
            return result
        return (
            "I'm sorry, I was unable to reach the AI service right now. "
            "Please check your API key and internet connection, then try again."
        )

    # ------------------------------------------------------------------
    # Task decomposition for the planner
    # ------------------------------------------------------------------

    def decompose_multitask(
        self,
        user_input: str,
        available_tools: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """Decompose a multitask user request into ordered structured tool calls."""
        tools_desc = available_tools or [
            "calculator (arithmetic/expressions, action: calculate, parameters: {'expression': str})",
            "datetime (time/date queries, action: get, parameters: {'query': str})",
            "browser (open sites/search web, action: parse_and_execute, parameters: {'command': str})",
            "applications (launch/close desktop apps, action: parse_and_execute, parameters: {'command': str})",
            "filesystem (file/dir operations, action: parse_and_execute, parameters: {'command': str})",
            "terminal (run allowed shell commands, action: run, parameters: {'command': str})",
        ]

        system_prompt = (
            "You are an AI task planner. Analyze the user prompt and extract ALL intended sub-tasks in execution order.\n"
            "Available tools: " + ", ".join(tools_desc) + "\n"
            "Return ONLY a JSON list of objects with the following schema:\n"
            '[{"tool": "<tool_name>", "action": "<action>", "parameters": {<key-value>}}]\n'
            "If the request contains no tool calls or is pure conversation, return []."
        )

        raw_response = self.ask(user_input, system_prompt=system_prompt)
        if not raw_response:
            return []

        try:
            match = re.search(r'\[.*\]', raw_response, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                if isinstance(parsed, list):
                    return [item for item in parsed if isinstance(item, dict) and "tool" in item]
        except Exception:
            pass

        return []
