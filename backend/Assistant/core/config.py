"""
Configuration management: loads environment variables and assistant settings.
"""
import os
from pathlib import Path


def load_env(env_path: str = None):
    """Simple .env parser without external dependencies."""
    if env_path is None:
        env_path = Path(__file__).resolve().parent.parent / ".env"
    else:
        env_path = Path(env_path)

    if not env_path.exists():
        return

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip().strip("\"'")
                if key and key not in os.environ:
                    os.environ[key] = val
    except Exception:
        pass


# Automatically load env on import
load_env()

FEATHERLESS_API_KEY = os.environ.get(
    "FEATHERLESS_API_KEY",
    "",
)
FEATHERLESS_BASE_URL = os.environ.get(
    "FEATHERLESS_BASE_URL",
    "https://api.featherless.ai/v1",
)
FEATHERLESS_MODEL = os.environ.get(
    "FEATHERLESS_MODEL",
    "deepseek-ai/DeepSeek-V3.2",
)

# -------------------------------------------------------------------------
# Featherless AI — Available Models Catalogue
# These models are all accessible via the same API endpoint.
# The assistant will use FEATHERLESS_MODEL by default, then fall back
# through FEATHERLESS_FALLBACK_MODELS if the primary model fails.
# -------------------------------------------------------------------------
FEATHERLESS_AVAILABLE_MODELS = [
    # === DeepSeek family (reasoning & coding) ===
    "deepseek-ai/DeepSeek-V3.2",
    "deepseek-ai/DeepSeek-V3",
    "deepseek-ai/DeepSeek-R1",
    "deepseek-ai/DeepSeek-R1-Zero",
    "deepseek-ai/DeepSeek-Coder-V2-Instruct",
    "deepseek-ai/DeepSeek-V2.5",
    # === Qwen family (multilingual & general) ===
    "Qwen/Qwen2.5-72B-Instruct",
    "Qwen/Qwen2.5-32B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "Qwen/QwQ-32B",
    # === Mistral / Mixtral family ===
    "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mistral-Nemo-Instruct-2407",
    # === Meta Llama family ===
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3-70B-Instruct",
    "meta-llama/Llama-3.2-90B-Vision-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct",
    # === Nous Research ===
    "NousResearch/Hermes-3-Llama-3.1-70B",
    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
    # === Google Gemma ===
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
    # === Microsoft Phi ===
    "microsoft/Phi-3-medium-128k-instruct",
    "microsoft/phi-4",
]

# Ordered fallback list — tried in sequence if the primary model fails
FEATHERLESS_FALLBACK_MODELS = os.environ.get(
    "FEATHERLESS_FALLBACK_MODELS",
    "Qwen/Qwen2.5-72B-Instruct,meta-llama/Meta-Llama-3.1-70B-Instruct,mistralai/Mixtral-8x22B-Instruct-v0.1",
).split(",")

# Default system persona for the assistant
ASSISTANT_SYSTEM_PROMPT = os.environ.get(
    "ASSISTANT_SYSTEM_PROMPT",
    (
        "You are a smart, helpful, and friendly AI assistant. "
        "Understand the user's intent fully — whether it is casual conversation, "
        "technical questions, creative tasks, or factual queries — and always provide "
        "a clear, accurate, and complete response. "
        "Never refuse to respond; always give your best answer."
    ),
)

