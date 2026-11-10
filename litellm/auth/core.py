from datetime import datetime
from typing import Protocol

from litellm.auth.host import KeyHost, ModelBudgetHost, TeamMemberModelBudgetHost
from litellm.auth.inputs import RequestFacts, Settings
from litellm.auth.outcome import Outcome


class ModelBudgetCore(Protocol):
    async def check_key_and_user(self, host: ModelBudgetHost) -> Outcome: ...

    async def check_user(self, host: ModelBudgetHost) -> Outcome: ...

    async def check_team_member(self, host: TeamMemberModelBudgetHost) -> Outcome: ...


class AuthCore(Protocol):
    async def start(self, host: KeyHost, facts: RequestFacts, settings: Settings, now: datetime) -> Outcome: ...

    async def start_resolved_key(
        self, host: KeyHost, facts: RequestFacts, settings: Settings, now: datetime
    ) -> Outcome: ...

    def model_budgets(self) -> ModelBudgetCore: ...
