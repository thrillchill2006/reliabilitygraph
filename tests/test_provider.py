from pathlib import Path

import pytest

from reliabilitygraph.provider import (
    BudgetAccountant,
    BudgetExceededError,
    BudgetLimits,
    MockProvider,
    ProviderClient,
    ProviderError,
    ProviderRequest,
    ReplayProvider,
)

FIXTURE = Path(__file__).parent / "fixtures" / "replay_response.json"


def test_mock_provider_is_deterministic_and_offline() -> None:
    provider = MockProvider()
    client = ProviderClient(provider, BudgetAccountant(BudgetLimits()))

    response = client.complete(ProviderRequest("test prompt"))

    assert response.text == "mock response"
    assert provider.invocations == 1


def test_replay_provider_returns_fixture() -> None:
    provider = ReplayProvider(FIXTURE)

    response = provider.complete(ProviderRequest("ignored by replay"))

    assert response.text == "A deterministic replay response."
    assert response.input_tokens == 4
    assert provider.invocations == 1


def test_budget_rejection_happens_before_provider_invocation() -> None:
    provider = MockProvider()
    limits = BudgetLimits(max_requests=0)
    client = ProviderClient(provider, BudgetAccountant(limits))

    with pytest.raises(BudgetExceededError):
        client.complete(ProviderRequest("test prompt"))

    assert provider.invocations == 0


def test_mock_exception_is_explicit() -> None:
    provider = MockProvider(failure="fixture failure")
    client = ProviderClient(provider, BudgetAccountant(BudgetLimits()))

    with pytest.raises(ProviderError, match="fixture failure"):
        client.complete(ProviderRequest("test prompt"))


def test_budget_limits_are_configurable_from_environment() -> None:
    limits = BudgetLimits.from_env(
        {
            "RELIABILITYGRAPH_MAX_REQUESTS": "2",
            "RELIABILITYGRAPH_MAX_INPUT_TOKENS": "20",
            "RELIABILITYGRAPH_MAX_OUTPUT_TOKENS": "30",
            "RELIABILITYGRAPH_MAX_ESTIMATED_USD": "0.50",
            "RELIABILITYGRAPH_INPUT_USD_PER_MILLION_TOKENS": "2.0",
            "RELIABILITYGRAPH_OUTPUT_USD_PER_MILLION_TOKENS": "4.0",
        }
    )

    assert limits.max_requests == 2
    assert limits.max_estimated_usd == 0.5
    assert limits.output_usd_per_million_tokens == 4.0


def test_estimated_usd_cap_is_checked_before_provider_invocation() -> None:
    provider = MockProvider()
    limits = BudgetLimits(
        max_estimated_usd=0.001,
        input_usd_per_million_tokens=1_000.0,
    )
    client = ProviderClient(provider, BudgetAccountant(limits))

    with pytest.raises(BudgetExceededError, match="estimated USD"):
        client.complete(ProviderRequest("test prompt"))

    assert provider.invocations == 0
