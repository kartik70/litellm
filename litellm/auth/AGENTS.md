# litellm/auth

This package decides who a request comes from and whether it may proceed. It holds the decisions only. The proxy does every cache, DB and Redis read, sends every alert, and turns the result into its own types and errors. A core written in another language and exposed through pyo3 implements the same interface, so callers never change when the core does.

## The core is pure

`AuthCore` in `core.py` is the interface every core implements. `PythonCore` and `RustCore` (the pyo3-backed core) both subclass it. A core method takes a host plus `RequestFacts`, `Settings` and the current time, and returns an `Outcome` (`Allow` or `Deny`). It does no IO itself, reads no globals and keeps no state between calls, so the same inputs and the same host answers always give the same outcome. The package imports only the standard library and itself.

## The host carries the IO

`AuthHost`, `ModelBudgetHost` and `TeamMemberModelBudgetHost` in `host.py` list every read, write and alert a core may ask for, as typed async methods. A core is plain async code that awaits those methods, the same shape as the Rust core over its `AuthHost` trait.

A host performs IO and returns data. Anything that compares, chooses or denies belongs in the core. When a decision needs data the core doesn't have, add a host method that returns that data instead of letting the host decide.

## Model the data, not flags

The values that cross the boundary live in one module per direction. `inputs.py` holds what a caller passes in (`RequestFacts`, `Settings`), `outcome.py` holds what a core returns (`Allow` with its grants, `Deny` with its denials), and `answers.py` holds what host methods return. Each is a frozen dataclass, and each choice is a union of them. Express "absent" as `None` on a typed value (a key without a team membership has `team_member=None`) instead of a boolean next to optional fields.

## Order is behavior

The order in which a core calls host methods is part of its contract. It decides which denial wins when several apply and which reads and alerts happen before a request is refused. Reordering checks or host calls is a behavior change. Two cores are equivalent only when they reach the same outcome through the same sequence of host calls.

## Projection stays outside

Nothing here knows about `UserAPIKeyAuth`, HTTP status codes or the proxy's exception types. The proxy turns `Allow` into its token object and maps every `Denial` to the public error contract in one place, `litellm/proxy/auth/auth_denial.py`. A new denial needs a case there.

## Credentials

`credential.py` picks the key from the presented headers, query and WebSocket values and owns the precedence between those sources. `key.py` hashes tokens and compares the master key in constant time. Code that needs either goes through these two modules instead of parsing headers or comparing keys itself.

## Tests

`tests/unit/auth` runs a core against a host that answers from a script and records each call. Tests assert both the outcome and the host calls in order, never core internals.
