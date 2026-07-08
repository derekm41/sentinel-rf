# sentinel-rf

How to start up:

source venv/bin/activate
FastAPI:  cd workspaces/sentinel-rf/backend
            uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Vite:   cd workspaces/sentinel-rf/frontend
        npm run dev

        
"https://legendary-invention-9jpr996vqg63p79q-8000.app.github.dev/advisor/ETH"


Analyzer Pipeline:

Market Data
   ↓
Indicator Engine
   ↓
Specialist Analyzers
   ├── Trend / Momentum Agent
   ├── Mean Reversion Agent
   ├── Breakout Agent
   ├── Sentiment Agent
   ├── Risk Agent
   └── Strategy Selector Agent
   ↓
AI Trade Committee / Final Analyst
   ↓
Top 3 Trade Setups
   ↓
Trade Logger
   ↓
Outcome Evaluator
   ↓
Reinforcement / Scoring Improvements

Rules calculate evidence.
AI explains, compares, ranks, and decides.