import os
import requests

class APIBackend:
    """
    Minimal LLM adapter.
    Env:
      LLM_API_BASE, LLM_API_KEY, LLM_MODEL
    """
    def __init__(self) -> None:
        self.base = os.environ.get("LLM_API_BASE", "")
        self.key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
        if not self.base or not self.key:
            raise RuntimeError("Please set LLM_API_BASE and LLM_API_KEY")

    def build_messages_and_create_chat_completion(self, user_prompt: str, system_prompt: str = "") -> str:
        payload = {
            "model": self.model,
            "messages": (
                [{"role": "system", "content": system_prompt}] if system_prompt else []
            ) + [{"role": "user", "content": user_prompt}],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {self.key}"}
        resp = requests.post(f"{self.base}/chat/completions", json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]