"""Deterministic provider boundary used by the Phase 0 foundation."""

from __future__ import annotations

import json
import logging
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast

LOGGER = logging.getLogger(__name__)
_SECRET_PATTERN = re.compile(
    r"(?i)(?:api[_ -]?key|authorization|token|password|secret)\s*[:=]\s*"
    r"(?:Bearer\s+)?\S+"
    r"|sk-[A-Za-z0-9_-]+"
    r"|-----BEGIN [^-]+ PRIVATE KEY-----.*?-----END [^-]+ PRIVATE KEY-----",
    re.DOTALL,
)


class ProviderError(RuntimeError):
    """Raised when a provider call cannot produce a response."""


class BudgetExceededError(RuntimeError):
    """Raised before a provider call when a configured local cap is exceeded."""


@dataclass(frozen=True)
class ProviderRequest:
    prompt: str
    max_output_tokens: int = 256


@dataclass(frozen=True)
class ProviderResponse:
    text: str
    input_tokens: int
    output_tokens: int


@dataclass(frozen=True)
class BudgetLimits:
    max_requests: int = 10
    max_input_tokens: int = 10_000
    max_output_tokens: int = 4_000
    max_estimated_usd: float = 1.0
    input_usd_per_million_tokens: float = 0.0
    output_usd_per_million_tokens: float = 0.0

    @classmethod
    def from_env(cls, environ: dict[str, str]) -> BudgetLimits:
        """Build limits from environment-style values with explicit validation."""

        def integer(name: str, default: int) -> int:
            value = int(environ.get(name, str(default)))
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
            return value

        def number(name: str, default: float) -> float:
            value = float(environ.get(name, str(default)))
            if value < 0 or not math.isfinite(value):
                raise ValueError(f"{name} must be a finite non-negative number")
            return value

        return cls(
            max_requests=integer("RELIABILITYGRAPH_MAX_REQUESTS", 10),
            max_input_tokens=integer("RELIABILITYGRAPH_MAX_INPUT_TOKENS", 10_000),
            max_output_tokens=integer("RELIABILITYGRAPH_MAX_OUTPUT_TOKENS", 4_000),
            max_estimated_usd=number("RELIABILITYGRAPH_MAX_ESTIMATED_USD", 1.0),
            input_usd_per_million_tokens=number(
                "RELIABILITYGRAPH_INPUT_USD_PER_MILLION_TOKENS", 0.0
            ),
            output_usd_per_million_tokens=number(
                "RELIABILITYGRAPH_OUTPUT_USD_PER_MILLION_TOKENS", 0.0
            ),
        )


@dataclass
class BudgetUsage:
    requests: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_usd: float = 0.0


class BudgetAccountant:
    """Enforces local pre-call limits and records estimated usage."""

    def __init__(self, limits: BudgetLimits) -> None:
        self.limits = limits
        self.usage = BudgetUsage()

    def check_before_call(self, request: ProviderRequest, input_tokens: int) -> None:
        """Reject a call before invocation if its worst-case estimate exceeds a cap."""

        if input_tokens < 0 or request.max_output_tokens < 0:
            raise ValueError("token counts must be non-negative")
        projected_requests = self.usage.requests + 1
        projected_input = self.usage.input_tokens + input_tokens
        projected_output = self.usage.output_tokens + request.max_output_tokens
        projected_cost = self.usage.estimated_usd + self.estimate_cost(
            input_tokens, request.max_output_tokens
        )
        checks = (
            (projected_requests > self.limits.max_requests, "request limit"),
            (projected_input > self.limits.max_input_tokens, "input token limit"),
            (projected_output > self.limits.max_output_tokens, "output token limit"),
            (projected_cost > self.limits.max_estimated_usd, "estimated USD limit"),
        )
        for exceeded, name in checks:
            if exceeded:
                raise BudgetExceededError(f"local {name} exceeded")

    def record(self, response: ProviderResponse) -> None:
        """Record actual fixture/provider usage and its estimated cost."""

        self.usage.requests += 1
        self.usage.input_tokens += response.input_tokens
        self.usage.output_tokens += response.output_tokens
        self.usage.estimated_usd += self.estimate_cost(
            response.input_tokens, response.output_tokens
        )

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost from configured rates; this is not a provider charge."""

        return (
            input_tokens * self.limits.input_usd_per_million_tokens
            + output_tokens * self.limits.output_usd_per_million_tokens
        ) / 1_000_000


class Provider(Protocol):
    """Minimal replaceable provider contract."""

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        """Return a deterministic or provider-backed completion."""
        ...


class MockProvider:
    """A provider that never performs network I/O."""

    def __init__(
        self,
        response: ProviderResponse | None = None,
        failure: str | None = None,
    ) -> None:
        self.response = response or ProviderResponse("mock response", 1, 2)
        self.failure = failure
        self.invocations = 0

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        self.invocations += 1
        if self.failure is not None:
            raise ProviderError(self.failure)
        return self.response


class ReplayProvider:
    """Replays a response fixture and never performs network I/O."""

    def __init__(self, fixture_path: Path) -> None:
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("replay fixture must contain a JSON object")
        values = cast(dict[str, object], payload)
        try:
            text = values["text"]
            input_tokens = values["input_tokens"]
            output_tokens = values["output_tokens"]
        except KeyError as error:
            raise ValueError(f"replay fixture is missing {error.args[0]}") from error
        if (
            not isinstance(text, str)
            or not isinstance(input_tokens, int)
            or not isinstance(output_tokens, int)
        ):
            raise ValueError("replay fixture has invalid response fields")
        self.response = ProviderResponse(text, input_tokens, output_tokens)
        self.invocations = 0

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        self.invocations += 1
        return self.response


class ProviderClient:
    """Applies local accounting around a provider implementation."""

    def __init__(self, provider: Provider, accountant: BudgetAccountant) -> None:
        self.provider = provider
        self.accountant = accountant

    def complete(self, request: ProviderRequest) -> ProviderResponse:
        input_tokens = estimate_tokens(request.prompt)
        self.accountant.check_before_call(request, input_tokens)
        try:
            response = self.provider.complete(request)
        except ProviderError:
            LOGGER.exception("provider call failed")
            raise
        self.accountant.record(response)
        LOGGER.info(
            "provider call completed: requests=%d estimated_usd=%.6f",
            self.accountant.usage.requests,
            self.accountant.usage.estimated_usd,
        )
        return response


def estimate_tokens(text: str) -> int:
    """Provide a deterministic local estimate without a tokenizer dependency."""

    return max(1, math.ceil(len(text) / 4))


def redact_secrets(message: str) -> str:
    """Redact common credential-shaped values before they reach logs."""

    return _SECRET_PATTERN.sub("[REDACTED]", message)
