# Summary
Automate creating JIRA issues with JSON files exported from your Trello project.

Trello fields are converted to Jira fields automatically like below,

  - one of trello cards -> one of jira issue tickets
  - trello card name -> jira issue summary
  - trello card description -> jira issue description
  - trello card url -> jira issue description and label
  - trello card attachments -> jira issue attachments
  - trello card comments -> jira issue comments
  - trello card checklists -> jira issue description
  - trello board name -> jira issue summary and label
  - trello board url -> jira issue description and label
  - trello list name -> jira issue summary and label
  - jira issue type is 'Task' by default

# HowTo
[1] Fill out properties in conf/t2j.ini

  - url : Your Jira URL, e.g. https://myproject.atlassian.net
  - project : Your Project Key
  - username : Your Login ID
  - password : Your Login Password
  
[2] Run t2jrun.py with json files

  - t2jrun.py sample1.json sample2.json sample3.json
  - Note that one json file must be matched up with one trello board.