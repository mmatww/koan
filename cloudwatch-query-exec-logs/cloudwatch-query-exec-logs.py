import boto3
import json
import os
import time

from datetime import datetime, timedelta
from urllib.parse import parse_qs

QUERY_LOG_GROUP = os.getenv('QUERY_LOG_GROUP', '/query_log_group/not/set')
QUERY_TIMESPAN_MINS = int(os.getenv('QUERY_TIMESPAN_MINS', '5'))
QUERY_SLEEP_SECS = int(os.getenv('QUERY_SLEEP_SECS', '10'))
QUERY_PRUNE_LIST = os.getenv('QUERY_PRUNE_LIST', '@ptr').split(',')

QUERY_TEXT = '''
fields @timestamp as timestamp, user.username as role, user.extra.sessionName.0 as username, objectRef.namespace as namespace, objectRef.name as pod, annotations.authorization.k8s.io/decision as decision
| filter @logStream like /^kube-apiserver-audit/
| filter objectRef.resource = "pods"
| filter objectRef.subresource = "exec"
| filter ispresent(user.extra.sessionName.0)
| parse requestURI "exec?*&container=" as command
'''

def format_record(record):
    out = { 'action': 'user-exec' }
    for item in record:
        key = item['field']
        if key == 'command':
            out['command'] = ' '.join(parse_qs(item['value']).get('command', []))
            continue
        if key not in QUERY_PRUNE_LIST:
            out[key] = item['value']
    return json.dumps(out)

now = datetime.now()
client = boto3.client('logs')
query_response = client.start_query(
    logGroupName=QUERY_LOG_GROUP,
    startTime=int((now - timedelta(minutes=QUERY_TIMESPAN_MINS)).timestamp()),
    endTime=int(now.timestamp()),
    queryString=QUERY_TEXT,
)
query_id = query_response['queryId']

results = None
while results == None or results['status'] in ('Running', 'Scheduled'):
    time.sleep(QUERY_SLEEP_SECS)
    results = client.get_query_results(queryId=query_id)

for record in results['results']:
    try:
        formatted = format_record(record)
        print(formatted)
    except Exception as ex:
        print(str(ex))
        print(record)
