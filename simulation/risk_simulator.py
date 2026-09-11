import time
from datetime import datetime
from simulation.risk_engine import calculate_risk


class RiskSimulator:

    def __init__(self):
        self.scenario = "NORMAL"

        self.data = {
            "crowd_count": 400,
            "crowd_density": 20,
            "movement_intensity": 15,
            "directional_change": 10,
            "temporal_prediction": 15,
            "xgboost_score": 15,
            "bayesian_probability": 15,

            "affected_zone": "Zone A",
            "latitude": 13.0827,
            "longitude": 80.2707,

            "risk_score": 0,
            "risk_level": "LOW",
            "emergency": False,

            "incident_status": "MONITORING",
            "acknowledged_by": None,
            "incident_message": "No active emergency.",

            "guard_status": "STANDBY",
            "guard_acknowledged": False,
            "guard_location": "Security Post",
            "guard_target_zone": None,
            "guard_navigation": False,
            "guard_navigation_message": None,

            "digital_twin_status": "NORMAL",

            # A list is used so simultaneous SOS requests are never overwritten.
            "citizen_sos": False,
            "citizen_sos_events": [],
            "completed_emergency_calls": [],
        }

        self.last_update = time.time()

        self.guards = [
            {"id": "Guard 1", "status": "STANDBY", "location": "North Gate", "x": 240, "y": 125},
            {"id": "Guard 2", "status": "STANDBY", "location": "East Gate", "x": 820, "y": 300},
            {"id": "Guard 3", "status": "STANDBY", "location": "West Gate", "x": 180, "y": 360},
            {"id": "Guard 4", "status": "STANDBY", "location": "South Gate", "x": 700, "y": 520},
        ]

        self.venue = {
            "name": "CrowdGuard Concert Venue",
            "map_units_per_meter": 1.0,
            "safe_exit_min_distance": 500,
            "critical_zone": {"name": "Critical Zone", "x": 500, "y": 330, "radius": 105},
            "citizen_position": {"x": 280, "y": 430},
            "exits": [
                {"name": "Exit A", "x": 90, "y": 320},
                {"name": "Exit B", "x": 910, "y": 320},
                {"name": "Exit C", "x": 500, "y": 590},
            ],
            "facilities": [
                {"name": "Stage", "x": 500, "y": 145},
                {"name": "Main Crowd Area", "x": 500, "y": 350},
            ],
            "drones": [
                {"id": "Drone 1", "x": 300, "y": 145, "location": "North-West sector", "battery": 87, "status": "ACTIVE"},
                {"id": "Drone 2", "x": 700, "y": 180, "location": "North-East sector", "battery": 64, "status": "ACTIVE"},
                {"id": "Drone 3", "x": 760, "y": 470, "location": "South-East sector", "battery": 42, "status": "STANDBY"},
            ],
        }

        self.calculate()

    def set_scenario(self, scenario):
        scenario = scenario.upper()

        if scenario not in ["NORMAL", "BUILDUP", "CRITICAL"]:
            return False

        self.scenario = scenario

        self.data.update({
            "guard_status": "STANDBY",
            "guard_acknowledged": False,
            "guard_location": "Security Post",
            "guard_target_zone": None,
            "guard_navigation": False,
            "guard_navigation_message": None,
            "acknowledged_by": None,
            "incident_status": "MONITORING",
        })

        for guard in self.guards:
            guard["status"] = "STANDBY"

        if scenario == "NORMAL":
            self.data.update({
                "crowd_count": 400,
                "crowd_density": 20,
                "movement_intensity": 15,
                "directional_change": 10,
                "temporal_prediction": 15,
                "xgboost_score": 15,
                "bayesian_probability": 15,
                "affected_zone": "Zone A",
                "latitude": 13.0827,
                "longitude": 80.2707,
                "digital_twin_status": "NORMAL",
                "incident_message": "Crowd conditions normal.",
            })

        elif scenario == "BUILDUP":
            self.data.update({
                "crowd_count": 900,
                "crowd_density": 55,
                "movement_intensity": 55,
                "directional_change": 45,
                "temporal_prediction": 55,
                "xgboost_score": 55,
                "bayesian_probability": 55,
                "affected_zone": "Zone A",
                "latitude": 13.0827,
                "longitude": 80.2707,
                "digital_twin_status": "HIGH CROWD DENSITY",
                "incident_message": "Crowd buildup detected in Zone A.",
            })

        else:
            self.data.update({
                "crowd_count": 1220,
                "crowd_density": 79,
                "movement_intensity": 83,
                "directional_change": 69,
                "temporal_prediction": 83,
                "xgboost_score": 83,
                "bayesian_probability": 83,
                "affected_zone": "Zone B",
                "latitude": 13.0840,
                "longitude": 80.2750,
                "digital_twin_status": "CRITICAL CROWD DENSITY",
                "incident_message": "Critical crowd situation detected in Zone B.",
            })

        self.calculate()

        if self.data["emergency"]:
            self.data["incident_status"] = "CRITICAL"
            self.data["incident_message"] = (
                "Emergency crowd situation detected in "
                + self.data["affected_zone"]
            )

        return True

    def calculate(self):
        risk = calculate_risk(
            crowd_density=self.data["crowd_density"],
            movement_intensity=self.data["movement_intensity"],
            directional_change=self.data["directional_change"],
            temporal_prediction=self.data["temporal_prediction"],
            xgboost_score=self.data["xgboost_score"],
            bayesian_probability=self.data["bayesian_probability"],
        )
        self.data.update(risk)

    def update(self):
        current_time = time.time()

        if self.scenario != "NORMAL":
            return self.data

        if current_time - self.last_update < 1:
            return self.data

        self.last_update = current_time

        self.data["crowd_count"] += 80
        self.data["crowd_density"] = min(100, self.data["crowd_density"] + 6)
        self.data["movement_intensity"] = min(100, self.data["movement_intensity"] + 7)
        self.data["directional_change"] = min(100, self.data["directional_change"] + 6)
        self.data["temporal_prediction"] = min(100, self.data["temporal_prediction"] + 7)
        self.data["xgboost_score"] = min(100, self.data["xgboost_score"] + 7)
        self.data["bayesian_probability"] = min(100, self.data["bayesian_probability"] + 7)

        self.calculate()

        if self.data["emergency"]:
            self.data["affected_zone"] = "Zone B"
            self.data["latitude"] = 13.0840
            self.data["longitude"] = 80.2750
            self.data["digital_twin_status"] = "CRITICAL CROWD DENSITY"
            self.data["incident_status"] = "CRITICAL"
            self.data["incident_message"] = "Emergency crowd situation detected in Zone B."

        return self.data

    def acknowledge_guard(self, guard_id="Guard 1"):
        selected_guard = next(
            (guard for guard in self.guards if guard["id"] == guard_id),
            None,
        )

        if selected_guard is None:
            return False

        if not self.data["emergency"]:
            return False

        if self.data["acknowledged_by"]:
            return self.data

        self.data["guard_acknowledged"] = True
        self.data["acknowledged_by"] = guard_id
        self.data["guard_status"] = "RESPONDING"
        self.data["guard_location"] = "Moving to incident"
        self.data["guard_target_zone"] = self.data["affected_zone"]
        self.data["incident_status"] = "ACKNOWLEDGED"
        self.data["incident_message"] = "Alert acknowledged by " + guard_id

        selected_guard["status"] = "RESPONDING"
        selected_guard["location"] = "Moving to " + self.data["affected_zone"]

        return self.data

    def navigate_guard(self, guard_id="Guard 1"):
        if self.data["acknowledged_by"] != guard_id:
            return False

        self.data["guard_navigation"] = True
        self.data["guard_status"] = "NAVIGATING"
        self.data["guard_navigation_message"] = (
            guard_id + " is moving towards " + self.data["affected_zone"]
        )
        self.data["incident_status"] = "GUARD RESPONDING"

        for guard in self.guards:
            if guard["id"] == guard_id:
                guard["status"] = "NAVIGATING"
                guard["location"] = "Moving towards " + self.data["affected_zone"]

        return self.data

    def citizen_sos_request(
        self,
        emergency_type,
        latitude=None,
        longitude=None,
    ):
        event_lat = (
            float(latitude)
            if latitude is not None
            else float(self.data["latitude"])
        )
        event_lon = (
            float(longitude)
            if longitude is not None
            else float(self.data["longitude"])
        )

        event_number = (
            len(self.data["citizen_sos_events"])
            + len(self.data["completed_emergency_calls"])
            + 1
        )

        event = {
            "id": f"SOS-{event_number:03d}",
            "emergency_type": emergency_type or "General Emergency",
            "timestamp": datetime.now().strftime("%d %b %Y, %I:%M:%S %p"),
            "location": {
                "latitude": event_lat,
                "longitude": event_lon,
                "zone": self.data["affected_zone"],
            },
            "status": "NEW",
        }

        self.data["citizen_sos_events"].append(event)
        self.data["citizen_sos"] = True

        return event

    def call_emergency_service(self, sos_id):
        events = self.data["citizen_sos_events"]

        event = next(
            (item for item in events if item.get("id") == sos_id),
            None,
        )

        if event is None:
            return False

        events.remove(event)

        event["status"] = "EMERGENCY SERVICES CONTACTED"
        event["called_at"] = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")

        self.data["completed_emergency_calls"].append(event)
        self.data["citizen_sos"] = len(events) > 0

        return event

    def get_state(self):
        return self.data

    def get_guards(self):
        return self.guards

    def get_venue(self):
        return self.venue
