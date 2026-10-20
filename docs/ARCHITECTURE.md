# Architecture — OmniDoc AI

## Components

- **API layer:** FastAPI validates requests and returns typed responses.
- **Domain services:** deterministic and testable Python modules hold core logic.
- **Persistence:** local files/demo data by default; optional model/vector adapters are configured explicitly.
- **Observability:** standard Python logging; do not log raw sensitive documents, credentials, or secrets.

## Request flow

1. Validate request and input limits.
2. Normalize input into a typed internal representation.
3. Run domain logic with explicit confidence/limitations.
4. Return a structured result and log metadata only.

See source modules for project-specific flow.
