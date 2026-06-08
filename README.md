Computing History Agent
A conversational AI agent built with Microsoft Foundry, deployed locally via a Flask web app, and integrated with Azure Entra ID authentication. This project demonstrates how to create, configure, and consume a Foundry agent using the OpenAI Responses API.

🚀 Project Overview
Created a Foundry project in Microsoft Azure.

Built a custom agent (computing-historian) using the GPT‑4.1‑mini model.

Configured the agent with instructions to act as an expert in the history of computing and AI.

Integrated the Web Search tool for enriched responses.

Developed a Flask client app to interact with the agent.

Connected via Azure Entra ID using DefaultAzureCredential.

Debugged and fixed endpoint issues (/responses/responses → /protocols/openai/responses).

Successfully tested locally at http://127.0.0.1:5000.

Pushed the project to GitHub for version control and collaboration.

📂 Project Structure
Code
computing-history-agent/
│
├── computer-history-client/
│   ├── app.py                # Flask web app
│   ├── agent_client.py       # Handles agent communication
│   ├── requirements.txt      # Python dependencies
│   ├── static/               # CSS & JS for UI
│   ├── templates/            # HTML templates
│   └── .env                  # Environment variables (not committed)
│
├── README.md                 # Project documentation
└── .gitignore                # Excludes .env, __pycache__, .venv
⚙️ Setup Instructions
Clone the repo

bash
git clone https://github.com/S-S-Jayashree/computing-history-agent.git
cd computing-history-agent/computer-history-client
Create virtual environment

bash
python -m venv .venv
source .venv/Scripts/activate   # Windows
Install dependencies

bash
pip install -r requirements.txt
Configure .env

Code
AGENT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<project-name>/agents/computing-historian/endpoint/protocols/openai
Run Flask app

bash
python app.py
Access at: http://localhost:5000
