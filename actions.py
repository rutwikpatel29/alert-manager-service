import requests
import config
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s')
logger = logging.getLogger(__name__)

def handle_pod_crash_looping_alert(alert):
    """
    Handle alerts for crash looping pods.
    This function will send a notification to Slack.
    """
    try:
        logger.info(f"Handling pod crash looping alert for pod: {alert['labels']['pod']} in namespace: {alert['labels']['namespace']}")
        send_slack_notification(alert)
        logger.info("Handled pod crash looping alert successfully")
    except Exception as e:
        logger.error(f"Error handling pod crash looping alert: {e}", exc_info=True)

def send_slack_notification(alert):
    """
    Send a notification to Slack with alert details.
    """
    try:
        slack_webhook_url = config.SLACK_WEBHOOK_URL
        message = {
            "text": f"Critical Alert: {alert['labels']['alertname']}\n"
                    f"Description: {alert['annotations']['description']}\n"
                    f"Pod: {alert['labels']['pod']}\n"
                    f"Namespace: {alert['labels']['namespace']}\n"
                    f"Severity: {alert['labels']['severity']}\n"
                    f"Timestamp: {alert['startsAt']}"
        }
        response = requests.post(slack_webhook_url, json=message)
        if response.status_code == 200:
            logger.info("Sent Slack notification successfully")
        else:
            logger.error(f"Failed to send Slack notification: {response.text}")
    except Exception as e:
        logger.error(f"Error sending Slack notification: {e}", exc_info=True)
