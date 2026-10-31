"""app.ask のトークン数表示テスト。"""

from app.ask import ask


class _FakeUsage:
    prompt_token_count = 123
    candidates_token_count = 45


class _FakeResponse:
    text = "テスト応答"
    usage_metadata = _FakeUsage()


class _FakeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    class _Models:
        def __init__(self, response):
            self._response = response

        def generate_content(self, model: str, contents: str):
            return self._response

    @property
    def models(self):
        return self._Models(_FakeResponse())


def test_ask_prints_input_and_output_tokens(monkeypatch, capsys):
    monkeypatch.setattr("app.ask.get_api_key", lambda: "dummy-key")
    monkeypatch.setattr("app.ask.genai.Client", lambda api_key: _FakeClient(api_key))

    result = ask("LoRAとは何ですか？")

    assert result == "テスト応答"
    captured = capsys.readouterr()
    assert "[input tokens] 123" in captured.out
    assert "[output tokens] 45" in captured.out
