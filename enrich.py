# enrich.py
from prometheus_api_client import PrometheusConnect
import logging

# Ensure the URL includes the schema (http:// or https://)
prom = PrometheusConnect(url="https://prometheus.qa.k8s.begenuin.com")

logger = logging.getLogger(__name__)

def get_cpu_utilization(namespace, pod):
    """
    Query Prometheus to get the CPU utilization percentage for a specific pod.
    """
    query = (
        f'sum(rate(container_cpu_usage_seconds_total{{namespace="{namespace}", pod="{pod}"}}[5m])) by (pod) / '
        f'sum(kube_pod_container_resource_requests{{namespace="{namespace}", pod="{pod}", resource="cpu"}}) by (pod)'
    )
    cpu_usage = prom.custom_query(query=query)
    logger.debug(f"CPU usage query result for pod {pod}: {cpu_usage}")

    if cpu_usage:
        cpu_utilization_percentage = float(cpu_usage[0]['value'][1]) * 100
        return f"{cpu_utilization_percentage:.2f}%"
    return "N/A"

def get_memory_utilization(namespace, pod):
    """
    Query Prometheus to get the memory utilization percentage for a specific pod.
    """
    query = (
        f'sum(container_memory_working_set_bytes{{namespace="{namespace}", pod="{pod}", image!=""}}) by (pod) / '
        f'sum(kube_pod_container_resource_requests{{namespace="{namespace}", pod="{pod}", resource="memory"}}) by (pod)'
    )
    memory_usage = prom.custom_query(query=query)
    logger.debug(f"Memory usage query result for pod {pod}: {memory_usage}")

    if memory_usage:
        memory_utilization_percentage = float(memory_usage[0]['value'][1]) * 100
        return f"{memory_utilization_percentage:.2f}%"
    return "N/A"

def enrich_alert(alert):
    """
    Enriches the alert with additional data (CPU and memory utilization).
    """
    for individual_alert in alert['alerts']:
        namespace = individual_alert['labels'].get('namespace', 'default')
        pod = individual_alert['labels'].get('pod', 'N/A')
        individual_alert['enriched_data'] = {
            "cpu_utilization": get_cpu_utilization(namespace, pod),
            "memory_utilization": get_memory_utilization(namespace, pod)
        }
        logger.debug(f"Enriched data for pod {pod}: {individual_alert['enriched_data']}")
    return alert
