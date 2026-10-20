# Development guide

1. Create a virtual environment and install `pip install -e ".[dev]"`.
2. Copy `.env.example` to `.env`; never commit secrets.
3. Run `uvicorn app.main:app --reload`.
4. Run `pytest` before opening a pull request.
5. Keep domain logic independent of HTTP handlers so it can be unit-tested.
6. Add tests for malformed inputs, empty data, and dependency-unavailable cases.

## Pull request checklist

- [ ] Tests pass locally.
- [ ] New endpoints have request/response models and examples.
- [ ] README and architecture docs are updated.
- [ ] No secrets or private data are included.
- [ ] Claims about model accuracy include a reproducible evaluation.
