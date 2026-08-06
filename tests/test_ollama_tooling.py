import pytest

from preventia.agent.models import OllamaChat

TOOL = {
    "name": "registrar_checkin",
    "description": "Registra el check-in",
    "parameters": {
        "type": "object",
        "properties": {"dosis_tomadas": {"type": "integer"}},
        "required": ["dosis_tomadas"],
    },
}


class FakeClient:
    def __init__(self, response):
        self.response = response
        self.request = None

    def chat(self, **request):
        self.request = request
        return self.response


def chat_with(response):
    client = FakeClient(response)
    return OllamaChat("llama3.1:8b", "http://localhost:11434", client=client), client


def test_forcing_a_tool_sends_its_schema_as_the_response_format():
    model, client = chat_with({"message": {"content": '{"dosis_tomadas": 5}'}})

    model.send(messages=[], tools=[TOOL], force_tool="registrar_checkin")

    assert client.request["format"] == TOOL["parameters"]


def test_no_format_is_sent_when_no_tool_is_forced():
    model, client = chat_with({"message": {"content": "hola"}})

    model.send(messages=[], tools=[TOOL])

    assert "format" not in client.request


def test_a_forced_json_answer_becomes_the_tool_call():
    model, _ = chat_with({"message": {"content": '{"dosis_tomadas": 5}'}})

    reply = model.send(messages=[], tools=[TOOL], force_tool="registrar_checkin")

    assert reply.first_argument_set("registrar_checkin") == {"dosis_tomadas": 5}


def test_a_native_tool_call_is_still_honoured():
    response = {
        "message": {
            "content": "",
            "tool_calls": [
                {"function": {"name": "registrar_checkin", "arguments": {"dosis_tomadas": 3}}}
            ],
        }
    }
    model, _ = chat_with(response)

    reply = model.send(messages=[], tools=[TOOL], force_tool="registrar_checkin")

    assert reply.first_argument_set("registrar_checkin") == {"dosis_tomadas": 3}


def test_a_native_tool_call_wins_over_the_content():
    response = {
        "message": {
            "content": '{"dosis_tomadas": 99}',
            "tool_calls": [
                {"function": {"name": "registrar_checkin", "arguments": {"dosis_tomadas": 3}}}
            ],
        }
    }
    model, _ = chat_with(response)

    reply = model.send(messages=[], tools=[TOOL], force_tool="registrar_checkin")

    assert reply.first_argument_set("registrar_checkin") == {"dosis_tomadas": 3}


def test_content_that_is_not_json_yields_no_tool_call():
    model, _ = chat_with({"message": {"content": "no puedo responder eso"}})

    reply = model.send(messages=[], tools=[TOOL], force_tool="registrar_checkin")

    assert reply.first_argument_set("registrar_checkin") is None


def test_forcing_a_tool_that_was_not_offered_sends_no_format():
    model, client = chat_with({"message": {"content": "{}"}})

    model.send(messages=[], tools=[TOOL], force_tool="otra_herramienta")

    assert "format" not in client.request


def test_the_system_prompt_still_leads_the_messages():
    model, client = chat_with({"message": {"content": "{}"}})

    model.send(messages=[{"role": "user", "content": "hola"}], system="reglas")

    assert client.request["messages"][0] == {"role": "system", "content": "reglas"}
