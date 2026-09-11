from flask import Flask, jsonify, render_template, request

from simulation.risk_simulator import RiskSimulator

app = Flask(__name__)
simulator = RiskSimulator()


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/guard")
def guard():
    return render_template("guard.html")


@app.route("/citizen")
def citizen():
    return render_template("citizen.html")


@app.route("/api/status")
def get_status():
    return jsonify(simulator.update())


@app.route("/api/venue")
def venue():
    return jsonify(simulator.get_venue())


@app.route("/api/simulation", methods=["POST"])
def simulation_control():
    data = request.get_json() or {}
    scenario = data.get("scenario", "NORMAL")
    if not simulator.set_scenario(scenario):
        return jsonify({"success": False, "error": "Invalid scenario"}), 400
    return jsonify({"success": True, "scenario": scenario, "data": simulator.get_state()})


@app.route("/api/guard/acknowledge", methods=["POST"])
def guard_acknowledge():
    data = request.get_json() or {}
    guard_id = data.get("guard_id", "Guard 1")
    result = simulator.acknowledge_guard(guard_id)
    if result is False:
        return jsonify({"success": False, "error": "Unable to acknowledge alert."}), 400
    return jsonify({"success": True, "data": result})


@app.route("/api/guard/navigate", methods=["POST"])
def guard_navigate():
    data = request.get_json() or {}
    guard_id = data.get("guard_id", "Guard 1")
    result = simulator.navigate_guard(guard_id)
    if result is False:
        return jsonify({"success": False, "error": "Guard must acknowledge the alert first."}), 400
    return jsonify({"success": True, "data": result})


@app.route("/api/guards")
def guards():
    return jsonify(simulator.get_guards())


@app.route("/api/citizen/sos", methods=["POST"])
def citizen_sos():
    data = request.get_json() or {}
    emergency_type = data.get("emergency_type", "General Emergency")
    result = simulator.citizen_sos_request(
        emergency_type=emergency_type,
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )
    return jsonify({"success": True, "data": result})


@app.route("/api/emergency/call", methods=["POST"])
def call_emergency():
    data = request.get_json() or {}
    sos_id = data.get("sos_id")

    if not sos_id:
        return jsonify({"success": False, "error": "Missing SOS ID"}), 400

    result = simulator.call_emergency_service(sos_id)

    if result is False:
        return jsonify({"success": False, "error": "Emergency event not found"}), 404

    return jsonify({"success": True, "data": result})

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
