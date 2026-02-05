class BridgeLCC:
    """Main class for handling Life Cycle Cost Analysis of bridges."""
    
    def __init__(self, project_name, inputs):
        self.project_name = project_name
        self.inputs = inputs  # Dictionary of user inputs
        self.outputs = {}

    def calculate_lcc(self):
        """Calculate the total life cycle cost based on input parameters."""
        try:
            material_cost = sum(self.inputs["bill_of_quantity"].values())
            maintenance_cost = self.inputs["maintenance_cost"]
            operation_cost = self.inputs["vehicle_operating_cost"]
            discount_rate = self.inputs["discount_rate"]

            # Simple NPV calculation
            total_cost = (material_cost + maintenance_cost + operation_cost) / (1 + discount_rate)
            self.outputs["total_lcc"] = total_cost
            return total_cost
        except KeyError as e:
            raise ValueError(f"Missing input parameter: {e}")

    def get_outputs(self):
        """Return computed outputs."""
        return self.outputs
