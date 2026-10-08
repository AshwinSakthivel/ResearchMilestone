# Pentagram Research Milestone

An individual, interactive PySide6 prototype for the Pentagram federated-healthcare-AI simulator. It demonstrates the chosen desktop framework and package manager without requiring real patient data, cloud services, networking, or actual model training.

## What it does

1. Accepts a local display name.
2. Lets the user configure 3–5 virtual hospitals and 1–10 training rounds.
3. Optionally simulates one hospital dropping out.
4. Generates deterministic, believable mock federated-learning metrics.
5. Displays each virtual hospital's participation status and round-by-round accuracy/loss values.

The same configuration produces the same results. This is intentional: it makes the prototype easy to test and demonstrates UI/application logic rather than expensive ML training.

## Technologies researched

| Technology | Role | Why it fits Pentagram |
| --- | --- | --- |
| Python | Application and simulation logic | Accessible to the team and compatible with later data/ML libraries. |
| PySide6 | Desktop UI framework | Supports a local, multi-screen desktop app with forms, tables, and status displays. |
| uv | Package/project manager | Creates a reproducible virtual environment and lockfile for consistent teammate installs. |
| Flower (future evaluation) | Possible federated-learning simulator | Relevant if the project later needs a lightweight local FL demonstration, but not required for this mocked prototype. |

## Run it

Install [uv](https://docs.astral.sh/uv/) once, then run these commands from this project folder:

```bash
uv sync
uv run python src/main.py
```

`uv sync` installs the declared dependencies and creates `uv.lock`. Commit that lockfile to Git after it is generated.

## Project scope

This milestone prototype deliberately excludes real hospitals, PHI, cloud services, distributed networking, persistent storage, and real training. The shared capstone application can later expand the same UI patterns into experiment setup, live monitoring, results comparison, and audit-report export.

