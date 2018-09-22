# curl -D- -X GET -H "Authorization: Basic ZnJlZDpmcmVk" -H "Content-Type: application/json" "http://localhost:8080/rest/api/2/issue/QA-31"
import requests

def create_issue(jira_server, jira_user, jira_pw, data):
    print('creating new Jira issue')
    url = 'https://' + jira_server + '/rest/api/2/issue/'

    headers = {'Content-type': 'application/json'}

    try:
        req = requests.post(url, auth=(jira_user, jira_pw), data=data, headers=headers, verify=False)

        # check return
        if not req.status_code in range(200,206):
            print('Error connecting to Jira.. check config file')
            sys.exit()
        jira = req.json()
        return jira['key']
    except requests.exceptions.Timeout:
        print('A timeout has occurred.')
    except requests.exceptions.RequestException as exep:
        print('error connecting to jira. stacktrace follows: ' + str(exep))
    except:
        print('Jira ticket')
        print(req.status_code)
        print(req.text)

def log_security_ticket(project, summary, description, issuetype, component, affected_version, priority, username, password):
    json_body = ("{"
        "\"fields\": {"
        "   \"project\":"
        "   {"
        "     \"key\": \"" + project + "\""
        "   },"
        "   \"priority\":"
        "   {"
        "       \"name\": \"" + priority + "\""
        "   },"
        "   \"summary\": \"" + summary + "\","
        "   \"description\": \"" + description + "\","
        "   \"issuetype\":"
        "   {"
        "       \"name\": \"" + issuetype + "\""
        "   },"
        "   \"components\":"
        "   [{"
        "       \"name\": \"" + component + "\""
        "   }],"
        "   \"versions\":"
        "   [{"
        "       \"name\": \"" + affected_version + "\""
        "   }]"
        "   }"
        "}")
    key = create_issue('backbase.atlassian.net', username, password, json_body)
    return key


key = log_security_ticket("BACKLOG", "Test Issue", "Test for creating a ticket through the Jira API", "Bug", "Component Name", "8.0.17", "Minor", 'YOUR_USERNAME', 'YOUR_PASSWORD')
print(key)
print("Done")