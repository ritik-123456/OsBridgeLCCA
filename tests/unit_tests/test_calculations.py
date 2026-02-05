import pytest
from core.cost_component import *

# ✅ Test Initial Construction Cost
@pytest.mark.unit
def test_initial_construction_cost():
    cost = InitialConstructionCost(quantity=100, rate=500)
    assert cost.calculate_cost() == 50000

# ✅ Test Carbon Emission Cost
@pytest.mark.unit
def test_initial_carbon_emission_cost():
    cost = InitialCarbonEmissionCost(material_quantity=200, carbon_emission_factor=2.5, carbon_cost=50)
    assert cost.calculate_cost() == 25000

# ✅ Test Road User Cost
@pytest.mark.unit
def test_road_user_cost():
    cost = RoadUserCost(vehicles_affected=1000, vehicle_operation_cost=10, construction_time=2)
    assert cost.calculate_cost() == 20000
# Placeholder for test calculations
