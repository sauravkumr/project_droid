from flask import Flask, render_template, request
import openai


import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from flask import redirect

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
jira_api_token = os.getenv('JIRA_API_TOKEN')
jira_email = os.getenv('JIRA_EMAIL')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_title = request.form.get('task_title')
        prompt = f"Expand this task title into a detailed project scope: '{task_title}'."
        # Query GPT to generate the data for the Attlasian Document Format
        task_details = query_gpt(prompt)
        print("TASK", task_details)

        # Create a jira ticket using the API
        jira_response = create_jira_ticket(task_title, task_details)
        # if jira_response:
        #     return redirect(jira_response)  # Redirect to the Jira issue
        # else:
        #     pass

        return render_template('result.html', task_title=task_title, task_details=task_details, jira_response=jira_response)
    return render_template('index.html')
        
def create_jira_ticket(task_title, task_details):
    url = "https://saurav-workboard.atlassian.net/rest/api/3/issue"
    auth = HTTPBasicAuth(jira_email, jira_api_token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Convert description to the Atlassian Document Format
    adf_description = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": task_details
                    }
                ]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {"key": "DROID"},
            "summary": task_title,
            "description": adf_description,
            "issuetype": {"name": "Task"}
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth)
        print(response.json())
        # return response.json()
        issue_key = response.json()['key']
        jira_issue_url = f"https://saurav-workboard.atlassian.net/browse/{issue_key}"
        print(jira_issue_url)
        return jira_issue_url
    except Exception as e:
        print(f"Error creating Jira ticket: {e}")
        return None

# QUERY GPT 3.5 to develop the 
def query_gpt(prompt):
    openai.api_key = openai_api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant at a software engineering company. Your job is to take under developed tasks and output a completed scope for the task that could include descriptions, acceptance criteria, sub-tasks, assumptions, and any other relevant details."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
