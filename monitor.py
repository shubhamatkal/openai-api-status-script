import requests
import time
from datetime import datetime

# ================== CONFIGURATION ==================
COMPONENTS_URL = "https://status.openai.com/api/v2/components.json"
PROXY_URL = "https://status.openai.com/proxy/status.openai.com"
CHECK_INTERVAL = 60   # seconds between checks
TIMEOUT = 10          # HTTP request timeout
# ===================================================

last_status = {}
session = requests.Session()  # reuse TCP connections for efficiency


def fetch_json(url):
    """Fetch and return JSON data safely, or None on error."""
    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def get_incident_message(component_name, proxy_data):
    """Extract a readable issue summary for the given component."""
    incidents = proxy_data.get("summary", {}).get("ongoing_incidents", [])
    for incident in incidents:
        if component_name.lower() in incident.get("name", "").lower():
            return incident.get("summary")
    return None


def monitor():
    """Continuously check for status changes and print only new issues."""
    while True:
        components_data = fetch_json(COMPONENTS_URL)
        if not components_data:
            time.sleep(CHECK_INTERVAL)
            continue

        changed = [
            comp["name"]
            for comp in components_data.get("components", [])
            if last_status.get(comp["name"]) != comp["status"]
            and comp["status"] != "operational"
        ]

        for comp in components_data.get("components", []):
            last_status[comp["name"]] = comp["status"]

        if changed:
            proxy_data = fetch_json(PROXY_URL) or {}
            for name in changed:
                message = get_incident_message(name, proxy_data) or "Service issue detected"
                timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
                print(f"{timestamp} Product: OpenAI API - {name}")
                print(f"Status: {message}\n")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor()
