# actions.py
import requests
import config

def take_action(alert):
    """
    Processes each alert and sends a notification to Slack with enriched data.
    """
    for individual_alert in alert['alerts']:
        # Send a Slack notification for each individual alert
        send_slack_notification(individual_alert, individual_alert.get('enriched_data', {}))

def send_slack_notification(individual_alert, enriched_data):
    """
    Sends a formatted notification to Slack with alert details and enriched data.
    """
    slack_webhook_url = config.SLACK_WEBHOOK_URL
    labels = individual_alert['labels']
    annotations = individual_alert['annotations']
    
    # Construct the message with alert details and enriched data
    message = {
        "text": (
            f"Alert: {labels.get('alertname', 'N/A')}\n"
            f"Description: {annotations.get('description', 'N/A')}\n"
            f"Pod: {labels.get('pod', 'N/A')}\n"
            f"Namespace: {labels.get('namespace', 'N/A')}\n"
            f"Cluster: {labels.get('cluster', 'N/A')}\n"
            f"Severity: {labels.get('severity', 'N/A')}\n"
            f"Timestamp: {individual_alert.get('startsAt', 'N/A')}\n"
            f"Enriched Data: CPU: {enriched_data.get('cpu_utilization', 'N/A')}, Memory: {enriched_data.get('memory_utilization', 'N/A')}"
        )
    }
    # Send the message to Slack
    requests.post(slack_webhook_url, json=message)
