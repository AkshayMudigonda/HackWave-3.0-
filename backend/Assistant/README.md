# Assistant

An agentic assistant framework with pluggable tools (filesystem, terminal,
browser, applications, calculator, datetime), a safety/permissions layer, and
an autonomous multi-step workflow engine.

## Structure

- `agent/` — core reasoning, planning, and decision-making loop
- `core/` — shared data models, task/observation/response types, tool registry
- `tools/` — individual tool implementations
- `safety/` — permission policies and confirmation flows
- `input/` — input handling (e.g. text input)
- `memory/` — conversation and task history storage
- `database/` — SQLite-backed task, action, observation, metric, anomaly, and preference history
- `system/` and `analytics/` — best-effort health monitoring, analysis, and lightweight anomaly detection
- `actions/` — safety-gated action execution and action history
- `automation/` — reusable workflow definitions and scheduler seam
- `data/` — static data files (aliases, history)
- `tests/` — unit and integration tests

## Getting Started

```bash
cd Assistant
python -m pip install -r requirements.txt
python main.py
```

To run the browser API used by the React app:

```bash
python main.py --serve
```

The API listens on `http://localhost:8000` by default. It accepts `POST
/api/assist` with `{ "message": "..." }` and returns `{ "success": true,
"message": "..." }`. Configure the permitted frontend origins with
`ALLOWED_ORIGINS` in `.env`; see `.env.example`.

Optional Featherless configuration belongs in `Assistant/.env` (never commit it):

```env
FEATHERLESS_API_KEY=your_key
FEATHERLESS_MODEL=your_model
```

## Demo requests

```text
Check my system health and tell me if anything needs attention.
My computer is running slowly. Find the reason.
Organize my workday.
Plan a trip from Hyderabad to Bangalore next weekend under ₹15,000.
```

System monitoring runs locally and reports only observed values. Calendar,
email, weather, hotel, transport, and booking steps have explicit extension
points; without a configured provider they return `NOT_CONFIGURED` and never
claim that data was retrieved or an action was performed.

Run tests with:

```bash
python -m unittest discover -s tests -v
```
