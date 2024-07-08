from atlassian import Jira
import json

import uuid

# Jira connection details
USER = "YOUR_USER_ID"
TOKEN = "YOUR_API_TOKEN"
DOMAIN = "YOUR_INSTANCE_URL"

def extract_issues_and_create_data_models(domain: str, user: str, token: str):
    # Connect to Jira
    jira = Jira(
        url=domain,
        username=user,
        password=token
    )

    # Initialize a list to store the data models
    data_models = []
    issue_index = 0  # Initialize issue index
    start_at = 0
    max_results = 100

    while True:
        jql_query = 'project = GENAIKB8'

        # Fetch the issues
        issues = jira.jql(jql_query, start=start_at, limit=max_results)
        if not issues['issues']:
            break

        for issue in issues['issues']:
            issue_index += 1  # Increment issue index
            if issue_index > 601:
                break
            fields = issue['fields']
            assignee = fields.get('assignee')
            assignee_name = assignee['displayName'] if assignee else 'Unassigned'
            priority = fields.get('priority', {})
            priority_name = priority.get('name', 'None')
            issue_type = fields['issuetype']['name']
            issue_link = f"{domain}/browse/{issue['key']}"
            feature=fields.get('customfield_10065', 'N/A'),
            sprint=fields.get('customfield_10020', 'N/A'),
            acceptance_criteria=fields.get('customfield_10066', 'N/A')
            issue_data = {
                'ID': str(issue['id']),
                'Key': str(issue['key']),
                'Summary': str(fields['summary']),
                'Description': str(fields.get('description', '')),
                'Assignee': assignee_name,
                'Feature':feature,
                'Sprint':sprint,
                'Acceptance criteria': acceptance_criteria,
                'Status': str(fields['status']['name']),
                'Created': str(fields['created']),
                'Updated': str(fields['updated']),
                'Priority': str(priority_name),
                'Issue Type': str(issue_type),
                'Issue Link': str(issue_link)
            }
            # print(issue_data)
            issue_json = json.dumps(issue_data)
            print(issue_json)
            if issue_index > 601:
                break
        start_at += max_results
    with open('data_model4.txt', 'w') as f:
        for model in data_models:
            f.write(f'{model.json()}\n')
    return data_models


data_models = extract_issues_and_create_data_models(DOMAIN, USER, TOKEN)
print(data_models)

