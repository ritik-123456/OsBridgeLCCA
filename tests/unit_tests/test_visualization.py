import pytest
from core.visualization import plot_cost_distribution


@pytest.mark.unit
def test_plot_cost_distribution():
    data = {'Initial Cost': 500000, 'Maintenance Cost': 100000, 'Repair Cost': 50000}
    fig = plot_cost_distribution(data)

    # ✅ Check if figure object is created
    assert fig is not None
    assert len(fig.data) > 0  # ✅ Ensure it has plot data
# Placeholder for test visualization
