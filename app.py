import logging
from flask import Flask, request, jsonify
import enrich
import actions

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint to receive alerts via a webhook.
    """
    try:
        alert = request.json
        logger.debug(f"Received alert: {alert}")
        
        # Enrich the alert with additional data
        enriched_alert = enrich.enrich_alert(alert)
        logger.debug(f"Enriched alert: {enriched_alert}")
        
        # Take action based on the enriched alert
        for individual_alert in enriched_alert['alerts']:
            actions.handle_pod_crash_looping_alert(individual_alert)
        
        logger.debug("Action taken successfully")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error processing alert: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Alert Manager")
    app.run(host='0.0.0.0', port=5000)
