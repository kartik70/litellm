from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestFacts:
    route: str
    token: str | None
    is_llm_api_route: bool


@dataclass(frozen=True, slots=True)
class Settings:
    master_key: str | None
    allow_user_auth: bool
    has_db: bool
    master_key_only_routes: frozenset[str]
    proxy_max_budget: float
