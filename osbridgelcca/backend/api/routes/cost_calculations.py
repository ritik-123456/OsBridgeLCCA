from flask import Blueprint, request, jsonify
from core.bridge_lcc import BridgeLCC

cost_bp = Blueprint("cost", __name__)

@cost_bp.route("/calculate", methods=["POST"])
def calculate():
    """API endpoint for calculating life cycle cost."""
    try:
        data = request.json
        lcc = BridgeLCC(data["project_name"], data["inputs"])
        total_cost = lcc.calculate_lcc()
        return jsonify({"total_lcc": total_cost})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
