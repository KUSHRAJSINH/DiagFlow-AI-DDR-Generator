import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your .env file.\n"
                "Example: GROQ_API_KEY=gsk-..."
            )
        _client = Groq(api_key=api_key)
    return _client


def call_llm_json(prompt: str, model: str = "llama-3.1-8b-instant", temperature: float = 0.2) -> dict:
    """
    Call the LLM with a prompt that expects a JSON response.
    Returns parsed dict. Raises ValueError if parsing fails.
    """
    client = get_client()

    print(f"  [LLM] Calling {model} via Groq... (prompt length: {len(prompt)} chars)")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert property diagnostics analyst. "
                    "Always respond with valid JSON only. No markdown, no extra text."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        response_format={"type": "json_object"},
        max_tokens=4096,
    )

    raw = response.choices[0].message.content.strip()
    print(f"  [LLM] Response received ({len(raw)} chars)")

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  [LLM] JSON parse error: {e}")
        print(f"  [LLM] Raw response (first 500 chars): {raw[:500]}")
        raise ValueError(f"LLM returned invalid JSON: {e}")


def call_llm_text(prompt: str, model: str = "llama-3.1-8b-instant", temperature: float = 0.2) -> str:
    """
    Call the LLM and return plain text response.
    """
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful property diagnostics assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=2048,
    )

    return response.choices[0].message.content.strip()
