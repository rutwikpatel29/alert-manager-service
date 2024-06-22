import requests
import config

def handle_pod_crash_looping_alert(alert):
    """
    Handle alerts for crash looping pods.
    This function will:
    1. Send a notification to Slack.
    2. Scale the affected deployment.
    """
    # Send a notification to Slack
    send_slack_notification(alert)
    
    # Scale the affected deployment
    # scale_deployment(alert)
    
def send_slack_notification(alert):
    slack_webhook_url = config.SLACK_WEBHOOK_URL
    message = {
        "text": f"Critical Alert: {alert['labels']['alertname']}\n"
                f"Description: {alert['annotations']['description']}\n"
                f"Pod: {alert['labels']['pod']}\n"
                f"Namespace: {alert['labels']['namespace']}\n"
                f"Severity: {alert['labels']['severity']}\n"
                f"Timestamp: {alert['startsAt']}"
    }
    requests.post(slack_webhook_url, json=message)

# def scale_deployment(alert):
#     # Extract relevant information from the alert
#     namespace = alert['labels']['namespace']
#     deployment_name = alert['labels']['pod'].rsplit('-', 2)[0]  # Assuming the pod name is formatted as 'deployment-name-randomstring'
#     # Use Kubernetes API to scale the deployment (assuming you have permissions set up)
#     api_url = f"https://kubernetes.default.svc/apis/apps/v1/namespaces/{namespace}/deployments/{deployment_name}/scale"
#     headers = {"Authorization": f"Bearer {config.KUBERNETES_API_TOKEN}"}
#     payload = {
#         "spec": {
#             "replicas": 0  # Scale down to 0 to stop the crash looping
#         }
#     }
#     response = requests.put(api_url, json=payload, headers=headers, verify=False)  # Verify=False for self-signed certs in cluster
#     if response.status_code == 200:
#         print(f"Successfully scaled down deployment {deployment_name} in namespace {namespace}")
#     else:
#         print(f"Failed to scale deployment: {response.text}")