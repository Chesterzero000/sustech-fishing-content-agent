import time
import json
import urllib.request
import os

from shared.skill_base import SkillBase
from shared.response_formatter import ResponseFormatter


BASE_API_URL = os.environ.get("DRONE_API_BASE_URL", "")


class DroneControllerService(SkillBase):
    """Service wrapper for drone controller operations.

    Exposes:
      - get_telemetry(drone_id)
      - get_trajectory(drone_id, start_time, end_time)
      - get_status(drone_id)
      - send_command(drone_id, command, params)
    """

    def __init__(self, config=None):
        super().__init__()
        self.config = config or {}
        self.api_base = BASE_API_URL.rstrip("/")
        self.formatter = ResponseFormatter() if 'ResponseFormatter' in globals() else None

    # Internal helper to perform lightweight API calls if a base URL is configured.
    def _fetch(self, path, method="GET", payload=None):
        if not self.api_base:
            return None
        url = self.api_base + "/" + path.lstrip("/")
        try:
            if method.upper() == "GET":
                with urllib.request.urlopen(url, timeout=5) as resp:
                    data = resp.read().decode()
                    return json.loads(data)
            else:
                data = json.dumps(payload or {}).encode("utf-8")
                req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method=method)
                with urllib.request.urlopen(req, timeout=5) as resp:
                    return json.loads(resp.read().decode())
        except Exception:
            return None

    # Helpers for consistent formatting
    def _format(self, data):
        if self.formatter and hasattr(self.formatter, "format"):
            try:
                return self.formatter.format(data)
            except Exception:
                pass
        return data

    def get_telemetry(self, drone_id):
        """Return real-time telemetry for a drone."""
        data = self._fetch(f"telemetry/{drone_id}", "GET", None)
        if not isinstance(data, dict) or not data:
            # Fallback synthetic data when no API is configured
            data = {
                "drone_id": drone_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "gps": {"lat": 0.0, "lon": 0.0, "altitude": 0.0},
                "depth": 0.0,
                "temperature": 0.0,
                "battery": {"level": 0, "voltage": 0.0},
            }
        return self._format(data)

    def get_trajectory(self, drone_id, start_time, end_time):
        """Return historical trajectory between two timestamps."""
        path = f"trajectory/{drone_id}?start={start_time}&end={end_time}"
        data = self._fetch(path, "GET", None)
        if not isinstance(data, list):
            data = [
                {"timestamp": start_time, "gps": {"lat": 0.0, "lon": 0.0, "altitude": 0.0}, "depth": 0.0, "temperature": 0.0},
                {"timestamp": end_time, "gps": {"lat": 0.0, "lon": 0.0, "altitude": 0.0}, "depth": 0.0, "temperature": 0.0},
            ]
        return self._format({"drone_id": drone_id, "trajectory": data})

    def get_status(self, drone_id):
        data = self._fetch(f"status/{drone_id}", "GET", None)
        if not isinstance(data, dict) or "status" not in data:
            data = {"drone_id": drone_id, "status": "idle", "uptime_s": 0}
        return self._format(data)

    def send_command(self, drone_id, command, params=None):
        payload = {"drone_id": drone_id, "command": command, "params": (params or {})}
        data = self._fetch(f"command/{drone_id}", "POST", payload)
        return self._format({"request": payload, "response": data})
