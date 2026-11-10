from collections.abc import Mapping
from typing import Final

from litellm.auth.answers import FallbackTarget, ModelBudgetScope, TeamMemberModelBudgetScope
from litellm.auth.core import ModelBudgetCore
from litellm.auth.host import ModelBudgetHost, TeamMemberModelBudgetHost
from litellm.auth.outcome import Allow, Deny, ModelBudgetExceeded, Outcome, WithinModelBudgets


class PythonModelBudgetCore(ModelBudgetCore):
    async def check_key_and_user(self, host: ModelBudgetHost) -> Outcome:
        return _within_model_budgets(await check_key_and_user_model_budgets(host))

    async def check_user(self, host: ModelBudgetHost) -> Outcome:
        return _within_model_budgets(await check_user_model_budgets(host))

    async def check_team_member(self, host: TeamMemberModelBudgetHost) -> Outcome:
        return _within_model_budgets(await check_team_member_model_budgets(host))


def _within_model_budgets(exceeded: ModelBudgetExceeded | None) -> Outcome:
    return Allow(WithinModelBudgets()) if exceeded is None else Deny(exceeded)


async def check_key_and_user_model_budgets(host: ModelBudgetHost) -> ModelBudgetExceeded | None:
    scope: Final = await host.read_model_budget_scope()
    if scope.key is None or not scope.models:
        return await _check_user_budgets(host, scope)
    exceeded: Final = await _check_key_budgets(host, scope.key.fallbacks, scope.models, scope.rewritable_model)
    if exceeded is not None:
        return exceeded
    return await _check_user_budgets(host, await host.read_model_budget_scope())


async def check_user_model_budgets(host: ModelBudgetHost) -> ModelBudgetExceeded | None:
    return await _check_user_budgets(host, await host.read_model_budget_scope())


async def check_team_member_model_budgets(host: TeamMemberModelBudgetHost) -> ModelBudgetExceeded | None:
    scope: Final = await host.read_team_member_model_budget_scope()
    if not scope.has_model_budgets:
        return None
    return await _check_team_member_budgets(host, scope, scope.models, scope.rewritable_model)


async def _check_key_budgets(
    host: ModelBudgetHost,
    fallbacks: Mapping[str, tuple[str, ...]],
    models: tuple[str, ...],
    rewritable_model: str | None,
) -> ModelBudgetExceeded | None:
    if not models:
        return None
    model: Final = models[0]
    exceeded: Final = await host.check_key_model_budget(model)
    if exceeded is None:
        return await _check_key_budgets(host, fallbacks, models[1:], rewritable_model)
    if model != rewritable_model:
        return exceeded
    fallback: Final = await _first_key_fallback_within_budget(host, fallbacks.get(model, ()))
    if fallback is None or not await host.authorize_budget_fallback(fallback):
        return exceeded
    await host.rewrite_request_model(fallback)
    return await _check_key_budgets(host, fallbacks, models[1:], fallback)


async def _first_key_fallback_within_budget(host: ModelBudgetHost, candidates: tuple[str, ...]) -> str | None:
    for candidate in candidates:
        if await host.check_key_model_budget(candidate) is None:
            return candidate
    return None


async def _check_user_budgets(host: ModelBudgetHost, scope: ModelBudgetScope) -> ModelBudgetExceeded | None:
    if not scope.user_has_model_budgets:
        return None
    for model in scope.models:
        if (exceeded := await host.check_user_model_budget(model)) is not None:
            return exceeded
    return None


async def _check_team_member_budgets(
    host: TeamMemberModelBudgetHost,
    scope: TeamMemberModelBudgetScope,
    models: tuple[str, ...],
    rewritable_model: str | None,
) -> ModelBudgetExceeded | None:
    if not models:
        return None
    model: Final = models[0]
    exceeded: Final = await host.check_team_member_model_budget(model)
    if exceeded is None:
        return await _check_team_member_budgets(host, scope, models[1:], rewritable_model)
    if model != rewritable_model or not scope.can_fall_back:
        return exceeded
    targets: Final = await host.read_team_member_fallbacks(model)
    target: Final = await _first_usable_fallback(host, tuple(target for target in targets if target.model != model))
    if target is None:
        return exceeded
    await host.reroute_team_member_request(target.model)
    return await _check_team_member_budgets(host, scope, models[1:], target.model)


async def _first_usable_fallback(
    host: TeamMemberModelBudgetHost, targets: tuple[FallbackTarget, ...]
) -> FallbackTarget | None:
    for target in targets:
        if await host.vet_team_member_fallback(target):
            return target
    return None
