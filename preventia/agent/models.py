import json
import os
from dataclasses import dataclass, field


class ModelUnavailable(RuntimeError):
    pass


class MissingModelToken(ModelUnavailable):
    pass


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict


@dataclass(frozen=True)
class Reply:
    text: str = ""
    tool_calls: tuple = field(default_factory=tuple)

    def first_argument_set(self, tool_name):
        for call in self.tool_calls:
            if call.name == tool_name:
                return call.arguments
        return None


DEFAULT_MODEL_IDS = {
    "anthropic": "claude-sonnet-5",
    "kimi": "kimi-k3",
    "ollama": "llama3.1:8b",
}

DEFAULT_BASE_URLS = {
    "kimi": "https://api.moonshot.ai/v1",
    "ollama": "http://localhost:11434",
}

LEGACY_TOKEN_VARS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "kimi": "MOONSHOT_API_KEY",
}

MAX_TOKENS = 1024


def _setting(name, provider_default=None):
    value = os.environ.get(name, "").strip()
    return value or provider_default


def resolve_provider():
    return _setting("PREVENTIA_MODEL_PROVIDER", "anthropic").lower()


def resolve_model_id(provider):
    return _setting("PREVENTIA_MODEL_ID", DEFAULT_MODEL_IDS.get(provider))


def resolve_base_url(provider):
    return _setting("PREVENTIA_MODEL_BASE_URL", DEFAULT_BASE_URLS.get(provider))


def resolve_token(provider):
    token = _setting("PREVENTIA_MODEL_TOKEN")
    if token:
        return token
    legacy = LEGACY_TOKEN_VARS.get(provider)
    return _setting(legacy) if legacy else None


class AnthropicChat:
    provider = "anthropic"

    def __init__(self, model_id, token):
        import anthropic

        self._errors = anthropic
        self._client = anthropic.Anthropic(api_key=token)
        self.model_id = model_id

    def send(self, messages, tools=None, system=None, force_tool=None):
        request = {
            "model": self.model_id,
            "max_tokens": MAX_TOKENS,
            "messages": messages,
            "thinking": {"type": "disabled"},
        }
        if system:
            request["system"] = system
        if tools:
            request["tools"] = [
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "input_schema": tool["parameters"],
                }
                for tool in tools
            ]
        if force_tool:
            request["tool_choice"] = {"type": "tool", "name": force_tool}

        try:
            response = self._client.messages.create(**request)
        except self._errors.APIStatusError as exc:
            raise ModelUnavailable(_describe(exc)) from exc
        except self._errors.APIConnectionError as exc:
            raise ModelUnavailable("no se pudo conectar con el proveedor del modelo") from exc

        text = "".join(block.text for block in response.content if block.type == "text")
        calls = tuple(
            ToolCall(block.name, dict(block.input))
            for block in response.content
            if block.type == "tool_use"
        )
        return Reply(text=text, tool_calls=calls)


class OpenAIChat:
    provider = "kimi"

    def __init__(self, model_id, token, base_url):
        import openai

        self._errors = openai
        self._client = openai.OpenAI(api_key=token, base_url=base_url)
        self.model_id = model_id

    def send(self, messages, tools=None, system=None, force_tool=None):
        payload = list(messages)
        if system:
            payload = [{"role": "system", "content": system}] + payload

        request = {
            "model": self.model_id,
            "max_tokens": MAX_TOKENS,
            "messages": payload,
        }
        if tools:
            request["tools"] = [{"type": "function", "function": tool} for tool in tools]
        if force_tool:
            request["tool_choice"] = {"type": "function", "function": {"name": force_tool}}

        try:
            response = self._client.chat.completions.create(**request)
        except self._errors.APIStatusError as exc:
            raise ModelUnavailable(_describe(exc)) from exc
        except self._errors.APIConnectionError as exc:
            raise ModelUnavailable("no se pudo conectar con el proveedor del modelo") from exc

        choice = response.choices[0].message
        calls = tuple(
            ToolCall(call.function.name, json.loads(call.function.arguments or "{}"))
            for call in (choice.tool_calls or [])
        )
        return Reply(text=choice.content or "", tool_calls=calls)


class OllamaChat:
    provider = "ollama"

    def __init__(self, model_id, host, client=None):
        if client is None:
            import ollama

            client = ollama.Client(host=host)
        self._client = client
        self.model_id = model_id

    def send(self, messages, tools=None, system=None, force_tool=None):
        payload = list(messages)
        if system:
            payload = [{"role": "system", "content": system}] + payload

        request = {"model": self.model_id, "messages": payload}
        if tools:
            request["tools"] = [{"type": "function", "function": tool} for tool in tools]

        forced = _forced_schema(tools, force_tool)
        if forced:
            request["format"] = forced

        try:
            response = self._client.chat(**request)
        except Exception as exc:
            raise ModelUnavailable(str(exc)) from exc

        message = response.get("message", {})
        calls = tuple(
            ToolCall(call["function"]["name"], _as_dict(call["function"].get("arguments")))
            for call in message.get("tool_calls", []) or []
        )
        text = message.get("content", "") or ""

        if not calls and forced:
            arguments = _parse_object(text)
            if arguments is not None:
                calls = (ToolCall(force_tool, arguments),)

        return Reply(text=text, tool_calls=calls)


def _forced_schema(tools, force_tool):
    if not force_tool:
        return None
    for tool in tools or ():
        if tool.get("name") == force_tool:
            return tool.get("parameters")
    return None


def _parse_object(text):
    try:
        parsed = json.loads(text)
    except (TypeError, ValueError):
        return None
    return parsed if isinstance(parsed, dict) else None


def _as_dict(arguments):
    if isinstance(arguments, dict):
        return arguments
    if not arguments:
        return {}
    return json.loads(arguments)


def _describe(exc):
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        detail = body.get("error", {}).get("message")
        if detail:
            return detail
    return f"el proveedor respondio {getattr(exc, 'status_code', 'un error')}"


def build_model():
    provider = resolve_provider()
    model_id = resolve_model_id(provider)

    if provider == "ollama":
        return OllamaChat(model_id, resolve_base_url(provider))

    token = resolve_token(provider)
    if not token:
        raise MissingModelToken(
            "falta el token del modelo: defina PREVENTIA_MODEL_TOKEN "
            f"o {LEGACY_TOKEN_VARS.get(provider, 'la credencial del proveedor')} en .env"
        )

    if provider == "anthropic":
        return AnthropicChat(model_id, token)
    if provider == "kimi":
        return OpenAIChat(model_id, token, resolve_base_url(provider))

    raise ModelUnavailable(f"proveedor de modelo desconocido: {provider}")


def describe_runtime():
    provider = resolve_provider()
    return {
        "provider": provider,
        "model_id": resolve_model_id(provider),
        "configured": bool(resolve_token(provider)) or provider == "ollama",
    }
