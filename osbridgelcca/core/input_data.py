class MaterialData:
    def __init__(self, material_type, description, quantity, unit, unit_rate, rate_source,
                 embodied_energy, carbon_emission_factor, data_source, scrap_value, scrap_recovery):
        self.material_type = material_type
        self.description = description
        self.quantity = quantity
        self.unit = unit
        self.unit_rate = unit_rate
        self.rate_source = rate_source
        self.embodied_energy = embodied_energy
        self.carbon_emission_factor = carbon_emission_factor
        self.data_source = data_source
        self.scrap_value = scrap_value
        self.scrap_recovery = scrap_recovery

class FinanceData:
    def __init__(self, discount_rate, interest_rate, investment_ratio):
        self.discount_rate = discount_rate
        self.interest_rate = interest_rate
        self.investment_ratio = investment_ratio

class CarbonEmissionData:
    def __init__(self, ssp_scenario, rcp_scenario, social_cost_of_carbon):
        self.ssp_scenario = ssp_scenario  # e.g., SSP1, SSP2, etc.
        self.rcp_scenario = rcp_scenario  # e.g., RCP4.5, RCP6, etc.
        self.social_cost_of_carbon = social_cost_of_carbon  # INR/kg CO2e

class TrafficData:
    def __init__(self, re_route_distance, road_roughness, road_rf, road_type, annual_traffic_increase, vehicle_composition):
        self.re_route_distance = re_route_distance
        self.road_roughness = road_roughness
        self.road_rf = road_rf  # Rise and Fall
        self.road_type = road_type  # Urban/Rural
        self.annual_traffic_increase = annual_traffic_increase
        self.vehicle_composition = vehicle_composition  # Dict with vehicle type breakdown

class MaintenanceData:
    def __init__(self, periodic_maintenance_rate, routine_inspection_rate, repair_cost_rate,
                 periodic_maintenance_freq, routine_inspection_freq):
        self.periodic_maintenance_rate = periodic_maintenance_rate
        self.routine_inspection_rate = routine_inspection_rate
        self.repair_cost_rate = repair_cost_rate
        self.periodic_maintenance_freq = periodic_maintenance_freq
        self.routine_inspection_freq = routine_inspection_freq

class RepairData:
    def __init__(self, details):
        self.details = details  # Detailed repair methodologies per component

class DemolitionData:
    def __init__(self, demolition_cost_rate):
        self.demolition_cost_rate = demolition_cost_rate

class RecycleData:
    def __init__(self, material_recovery_potential, associated_costs, carbon_savings):
        self.material_recovery_potential = material_recovery_potential
        self.associated_costs = associated_costs
        self.carbon_savings = carbon_savings

class Input:
    def __init__(self, material_data, finance_data, carbon_emission_data, traffic_data,
                 maintenance_data, repair_data, demolition_data, recycle_data):
        self.material_data = material_data
        self.finance_data = finance_data
        self.carbon_emission_data = carbon_emission_data
        self.traffic_data = traffic_data
        self.maintenance_data = maintenance_data
        self.repair_data = repair_data
        self.demolition_data = demolition_data
        self.recycle_data = recycle_data

    def display_inputs(self):
        """Display input data for debugging or report generation."""
        print("Material Data:", vars(self.material_data))
        print("Finance Data:", vars(self.finance_data))
        print("Carbon Emission Data:", vars(self.carbon_emission_data))
        print("Traffic Data:", vars(self.traffic_data))
        print("Maintenance Data:", vars(self.maintenance_data))
        print("Repair Data:", vars(self.repair_data))
        print("Demolition Data:", vars(self.demolition_data))
        print("Recycle Data:", vars(self.recycle_data))

# Example Usage:
if __name__ == "__main__":
    material = MaterialData("Steel", "Reinforcement bars", 5000, "kg", 60, "Govt Schedule", 32, 2.5, "EPD Source", 5, 90)
    finance = FinanceData(5.0, 7.5, 1.2)
    carbon = CarbonEmissionData("SSP2", "RCP6", 1200)
    traffic = TrafficData(15, 4000, "Plain", "Urban", 10, {"Car": 50, "Truck": 30, "Bus": 20})
    maintenance = MaintenanceData(0.55, 1.0, 10, 5, 1)
    repair = RepairData("Component-wise repair details")
    demolition = DemolitionData(10)
    recycle = RecycleData(80, 10000, 5000)

    project_input = Input(material, finance, carbon, traffic, maintenance, repair, demolition, recycle)
    project_input.display_inputs()
