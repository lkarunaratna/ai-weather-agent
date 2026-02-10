# Weather Agent

Small demo showing how to combine an LLM with a local tool that fetches
real weather data.

Files:
- `weather_agent/tools.py` - pure Python weather fetching logic
- `weather_agent/model.py` - model creation helpers
- `weather_agent/cli.py` - CLI runner that wires model + tools
- `run.py` - simple project entrypoint

Run:

```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
.venv\Scripts\python.exe run.py "Parker"
```

You can also call `run.py` without arguments; it defaults to `San Francisco`.

## Git / Publish

1. Initialize a local git repo and make the initial commit:

```bash
git init
git add .
git commit -m "Initial commit: weather agent refactor"
```

2. Create a GitHub repository and push (choose one):

- Using the GitHub website: create a new repository and follow the instructions to add the remote and push.

- Using GitHub CLI (`gh`):

```bash
gh auth login
gh repo create your-username/weather-agent --public --source=. --remote=origin --push
```

3. Or add remote manually and push:

```bash
git remote add origin https://github.com/you/weather-agent.git
git branch -M main
git push -u origin main
```

Notes:
- `.gitignore` is included to avoid committing virtual environments and editor files.
- Consider adding a license file and CI (GitHub Actions) later.
