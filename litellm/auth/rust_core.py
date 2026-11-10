from datetime import datetime

from litellm.auth.core import AuthCore
from litellm.auth.host import AuthHost, ModelBudgetHost, TeamMemberModelBudgetHost
from litellm.auth.inputs import RequestFacts, Settings
from litellm.auth.outcome import Outcome


class RustCore(AuthCore):
    async def start(self, host: AuthHost, facts: RequestFacts, settings: Settings, now: datetime) -> Outcome:
        raise NotImplementedError

    async def start_resolved_key(
        self, host: AuthHost, facts: RequestFacts, settings: Settings, now: datetime
    ) -> Outcome:
        raise NotImplementedError

    async def check_model_budgets(self, host: ModelBudgetHost) -> Outcome:
        raise NotImplementedError

    async def check_user_model_budgets(self, host: ModelBudgetHost) -> Outcome:
        raise NotImplementedError

    async def check_team_member_model_budgets(self, host: TeamMemberModelBudgetHost) -> Outcome:
        raise NotImplementedError
