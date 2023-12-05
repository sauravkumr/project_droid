# Project Droid
A Flask-based web app that automates the creation of detailed project tasks from minimal input. Uses GPT-3.5 queries to expand task titles into detailed scopes in Jira.

# Setup
Copy the code: `git clone https://github.com/sauravkumr/project_droid`
cd into the directory: `cd project_droid`

Set up the virtual env (not necesary):
`python -m venv venv`
`source venv/bin/activate`

Install the packages:
`pip install Flask python-dotenv requests openai`

Set up environment Variables

Create a .env file in your project root directory and add your OpenAI and Jira credentials

OPENAI_API_KEY=your_openai_api_key
JIRA_API_TOKEN=your_jira_api_token
JIRA_EMAIL=your_jira_email

# Running the app

Start the Flask server by running `flask run`
