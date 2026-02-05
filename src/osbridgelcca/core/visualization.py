import plotly.graph_objects as go

class Visualization:
    """Handles plotting and visualization of LCCA results."""
    
    @staticmethod
    def plot_lcc_distribution(lcc_data):
        """Generate a pie chart showing the cost distribution."""
        labels = list(lcc_data.keys())
        values = list(lcc_data.values())

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_layout(title_text="Life Cycle Cost Distribution")
        return fig
