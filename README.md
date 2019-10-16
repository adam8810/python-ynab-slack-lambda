# Python YNAB Slack Webhook

Receives webhook requests from slack with a search payload. We make a request to YNAB's API to retrieve list of categories which is then filtered, formatted and returned in the same request. Currently runs on a lambda with state persisted to dynamodb
