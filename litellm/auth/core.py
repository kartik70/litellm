from datetime import datetime
from typing import Protocol

from litellm.auth.host import AuthHost, ModelBudgetHost, TeamMemberModelBudgetHost
from litellm.auth.inputs import RequestFacts, Settings
from litellm.auth.outcome import Outcome


class AuthCore(Protocol):
    async def start(self, host: AuthHost, facts: RequestFacts, settings: Settings, now: datetime) -> Outcome: ...

    async def start_resolved_key(
        self, host: AuthHost, facts: RequestFacts, settings: Settings, now: datetime
    ) -> Outcome: ...

    async def check_model_budgets(self, host: ModelBudgetHost) -> Outcome: ...

    async def check_user_model_budgets(self, host: ModelBudgetHost) -> Outcome: ...

    async def check_team_member_model_budgets(self, host: TeamMemberModelBudgetHost) -> Outcome: ...
