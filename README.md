# Alert Manager Service
## Overview
A system to manage alerts programmatically with defined actions. 


alert_manager/
├── app.py
├── enrich.py
├── actions.py
├── handlers/
│   ├── __init__.py
│   └── handler.py
├── requirements.txt
├── README.md
└── config.py

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python app.py`
4. Run Docker Build command with the use of Dockfile
5. Build the Image and push to repository
6. To Deploy in K8s use `kubectl create -f Flask-deployment/flask-deployment.yml`, `kubectl create -f Flask-deployment/flask-service.yml`
7. Please update the promethues and alertmanager config files which are given in alertmanager-configuration

## Extending the System
To add new handling pipelines, create a new module in the `handlers` directory and implement the handling logic. Ensure the new handler is invoked appropriately in the `app.py` or `actions.py`.
