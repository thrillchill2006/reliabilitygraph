import logging
from contextlib import AbstractContextManager
from typing import Protocol

from reliabilitygraph.provider import redact_secrets


class LogCapture(Protocol):
    text: str

    def at_level(self, level: int) -> AbstractContextManager[None]:
        ...


def test_secret_redaction_removes_key_and_authorization_values() -> None:
    message = "api_key=sk-test-secret authorization=Bearer secret-token"

    redacted = redact_secrets(message)

    assert "sk-test-secret" not in redacted
    assert "secret-token" not in redacted
    assert "[REDACTED]" in redacted


def test_provider_logs_do_not_include_prompt_or_credentials(
    caplog: LogCapture,
) -> None:
    with caplog.at_level(logging.INFO):
        logging.getLogger("reliabilitygraph.provider").info(
            redact_secrets("api_key=sk-test-secret")
        )

    assert "sk-test-secret" not in caplog.text
