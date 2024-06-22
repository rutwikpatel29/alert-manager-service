import logging
import actions

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def handle_alert(alert):
    """
    Main handler function to process alerts based on their type.
    """
    try:
        alert_name = alert['labels'].get('alertname', 'N/A')
        logger.info(f"Handling alert: {alert_name}")
        
        if alert_name == 'KubePodCrashLooping':
            logger.debug("Detected KubePodCrashLooping alert")
            actions.handle_pod_crash_looping_alert(alert)
        else:
            logger.warning(f"Unhandled alert type: {alert_name}")
        
        logger.info(f"Handled alert: {alert_name} successfully")
    except Exception as e:
        logger.error(f"Error handling alert: {e}", exc_info=True)

# Example usage:
# if __name__ == '__main__':
#     test_alert = {
#         'labels': {'alertname': 'KubePodCrashLooping', 'pod': 'example-pod', 'namespace': 'default'},
#         'annotations': {'description': 'Pod is crash looping', 'summary': 'Pod is crash looping'},
#         'startsAt': '2024-06-22T06:51:14.437Z'
#     }
#     handle_alert(test_alert)
