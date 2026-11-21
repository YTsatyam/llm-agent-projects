# Python tips
- Create a virtual environment with python -m venv .venv, then activate it before pip install.
- Never hardcode API keys; keep them in a .env file and load them with python-dotenv.
- Use pathlib for file paths instead of string concatenation.
- Wrap risky code in try/except and log errors instead of ignoring them.