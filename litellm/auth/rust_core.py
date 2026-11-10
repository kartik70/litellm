from datetime import datetime

from litellm.auth.core import AuthCore, ModelBudgetCore
from litellm.auth.host import KeyHost
from litellm.auth.inputs import RequestFacts, Settings
from litellm.auth.outcome import Outcome


class RustCore(AuthCore):
    async def start(self, host: KeyHost, facts: RequestFacts, settings: Settings, now: datetime) -> Outcome:
        raise NotImplementedError

    async def start_resolved_key(
        self, host: KeyHost, facts: RequestFacts, settings: Settings, now: datetime
    ) -> Outcome:
        raise NotImplementedError

    def model_budgets(self) -> ModelBudgetCore:
        raise NotImplementedError
