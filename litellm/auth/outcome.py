from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class NoMasterKey:
    token: str | None


@dataclass(frozen=True, slots=True)
class UserAuthRoute:
    pass


@dataclass(frozen=True, slots=True)
class MasterKey:
    pass


@dataclass(frozen=True, slots=True)
class CachedAdminKey:
    pass


@dataclass(frozen=True, slots=True)
class VirtualKey:
    budget_throttle_pct: float | None


@dataclass(frozen=True, slots=True)
class WithinModelBudgets:
    pass


Grant: TypeAlias = NoMasterKey | UserAuthRoute | MasterKey | CachedAdminKey | VirtualKey | WithinModelBudgets


@dataclass(frozen=True, slots=True)
class MissingKey:
    pass


@dataclass(frozen=True, slots=True)
class MalformedKey:
    pass


@dataclass(frozen=True, slots=True)
class UserAuthDisabled:
    pass


@dataclass(frozen=True, slots=True)
class ExpiredKey:
    expires: datetime
    now: datetime
    key_label: str


@dataclass(frozen=True, slots=True)
class MasterKeyOnlyRoute:
    pass


@dataclass(frozen=True, slots=True)
class NoDatabase:
    pass


@dataclass(frozen=True, slots=True)
class NotAVirtualKey:
    pass


@dataclass(frozen=True, slots=True)
class KeyBlocked:
    pass


@dataclass(frozen=True, slots=True)
class OwnerDeactivated:
    user_id: str


@dataclass(frozen=True, slots=True)
class TeamMemberBudgetExceeded:
    user_id: str
    team_id: str
    spend: float
    max_budget: float


@dataclass(frozen=True, slots=True)
class KeyBudgetExceeded:
    spend: float
    max_budget: float


@dataclass(frozen=True, slots=True)
class KeyWithoutToken:
    pass


@dataclass(frozen=True, slots=True)
class ModelBudgetExceeded:
    message: str
    current_cost: float
    max_budget: float
    entity_type: str | None
    entity_id: str | None


Denial: TypeAlias = (
    MissingKey
    | MalformedKey
    | UserAuthDisabled
    | ExpiredKey
    | MasterKeyOnlyRoute
    | NoDatabase
    | NotAVirtualKey
    | KeyBlocked
    | OwnerDeactivated
    | TeamMemberBudgetExceeded
    | KeyBudgetExceeded
    | KeyWithoutToken
    | ModelBudgetExceeded
)


@dataclass(frozen=True, slots=True)
class Allow:
    grant: Grant


@dataclass(frozen=True, slots=True)
class Deny:
    denial: Denial


Outcome: TypeAlias = Allow | Deny
