from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QFormLayout, QCheckBox, QGroupBox
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal, QStringListModel
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, 
                               QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame, QMessageBox, QCompleter)
from PySide6.QtGui import QIcon, QDoubleValidator, QIntValidator
from osbridgelcca.desktop_app.widgets.utils.data import *
import sys

# --- UPDATED: MATERIAL INPUT POPUP WITH COMPONENT-SPECIFIC FILTERING ---
class MaterialInputPopup(QDialog):
    def __init__(self, material_data_source, component_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Material Details")
        self.setFixedWidth(550)
        self.material_data_source = material_data_source  # Custom/Existing DB from data.py
        self.component_name = component_name 
        self.result_data = None
        
        # --- 1. MASTER DATABASE (Categorized by Component) ---
        # This structure allows showing different options based on the component selected.
        self.master_db = {
            
                "Excavation": {
                    "All type(manual) (0 to 1.5m)": {
                        "unit": "cum", "rate": "239", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1", 
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(manual) (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "262.9", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(manual) (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "286.8", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(manual) (4.5 to 6)": {
                        "unit": "cum", "rate": "310.7", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(manual) (Above 6 m)": {
                        "unit": "cum", "rate": "310.7", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(Mechanical) (0 to 1.5m)": {
                        "unit": "cum", "rate": "90", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(Mechanical) (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "99", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(Mechanical) (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "108", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(Mechanical) (4.5 to 6)": {
                        "unit": "cum", "rate": "117", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "All type(Mechanical) (Above 6 m)": {
                        "unit": "cum", "rate": "117", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum (0 to 1.5m)": {
                        "unit": "cum", "rate": "241", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "265.1", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "289.2", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum (4.5 to 6)": {
                        "unit": "cum", "rate": "313.3", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum (Above 6 m)": {
                        "unit": "cum", "rate": "313.3", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum and Boulders (0 to 1.5m)": {
                        "unit": "cum", "rate": "286", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum and Boulders (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "314.6", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum and Boulders (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "343.2", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum and Boulders (4.5 to 6)": {
                        "unit": "cum", "rate": "371.8", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Murrum and Boulders (Above 6 m)": {
                        "unit": "cum", "rate": "371.8", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Soft Rock (0 to 1.5m)": {
                        "unit": "cum", "rate": "557", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Soft Rock (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "612.7", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Soft Rock (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "668.4", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Soft Rock (4.5 to 6)": {
                        "unit": "cum", "rate": "724.1", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Soft Rock (Above 6 m)": {
                        "unit": "cum", "rate": "724.1", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Blasting) (0 to 1.5m)": {
                        "unit": "cum", "rate": "1232", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Blasting) (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "1355.2", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Blasting) (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "1478.4", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Blasting) (4.5 to 6)": {
                        "unit": "cum", "rate": "1601.6", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Blasting) (Above 6 m)": {
                        "unit": "cum", "rate": "1601.6", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Controlled Blasting) (0 to 1.5m)": {
                        "unit": "cum", "rate": "1328", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Controlled Blasting) (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "1460.8", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Controlled Blasting) (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "1593.6", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Controlled Blasting) (4.5 to 6)": {
                        "unit": "cum", "rate": "1726.4", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard Rock (Controlled Blasting) (Above 6 m)": {
                        "unit": "cum", "rate": "1726.4", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard rock (Chiselling and Wedging or Line drilling) (0 to 1.5m)": {
                        "unit": "cum", "rate": "1932", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard rock (Chiselling and Wedging or Line drilling) (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "2125.2", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard rock (Chiselling and Wedging or Line drilling) (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "2318.4", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard rock (Chiselling and Wedging or Line drilling) (4.5 to 6)": {
                        "unit": "cum", "rate": "2511.6", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Hard rock (Chiselling and Wedging or Line drilling) (Above 6 m)": {
                        "unit": "cum", "rate": "2511.6", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Laterite Rock (0 to 1.5m)": {
                        "unit": "cum", "rate": "1771", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Laterite Rock (1.5 to 3.0m)": {
                        "unit": "cum", "rate": "1948.1", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Laterite Rock (3.0 to 4.5m)": {
                        "unit": "cum", "rate": "2125.2", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Laterite Rock (4.5 to 6)": {
                        "unit": "cum", "rate": "2302.3", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    },
                    "Laterite Rock (Above 6 m)": {
                        "unit": "cum", "rate": "2302.3", "source": "Maha PWD SOR",
                        "carbon": "NA", "carbon_unit": "NA", "conv": "1",
                        "c_source": "NA", "recyclable": False, "grades": ["Standard"]
                    }
                },
                        
            
            "Pile": {
                "Steel Rebar (Fe500)": {
                    "unit": "MT", "rate": "88341", "source": "Maha PWD SOR",
                    "carbon": "2.6", "carbon_unit": "kgCO₂e/kg", "conv": "1000",
                    "c_source": "IFC", "recyclable": True, "grades": ["Fe500"]
                },
                "Concreting of bored pile (M30) (450mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "2914", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (450mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "3788.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (450mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4079.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (450mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "4662.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (450mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "5828", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (475mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3060", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (475mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "3978", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (475mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4284", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (475mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "4896", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (475mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "6120", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (500mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3182", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (500mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "4136.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (500mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4454.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (500mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "5091.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (500mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "6364", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (525mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3309", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (525mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "4301.7", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (525mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4632.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (525mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "5294.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (525mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "6618", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (550mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3443", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (550mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "4475.9", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (550mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4820.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (550mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "5508.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (550mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "6886", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (600mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "5027", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (600mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "6535.1", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (600mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "7037.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (600mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "8043.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (600mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "10054", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (625mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "5180", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (625mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "6734", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (625mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "7252", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (625mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "8288", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (625mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "10360", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (650mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "5340", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (650mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "6942", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (650mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "7476", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (650mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "8544", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (650mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "10680", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (750mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "7779", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (750mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "10112.7", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (750mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "10890.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (750mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "12446.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (750mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "15558", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (800mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "8197", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (800mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "10656.1", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (800mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "11475.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (800mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "13115.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (800mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "16394", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (825mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "8535", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (825mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "11095.5", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (825mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "11949", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (825mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "13656", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (825mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "17070", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (900mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "9277", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (900mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "12060.1", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (900mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "12987.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (900mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "14843.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (900mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "18554", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (975mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "10070", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (975mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "13091", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (975mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "14098", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (975mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "16112", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (975mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "20140", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1000mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "12352", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1000mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "16057.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1000mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "17292.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1000mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "19763.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1000mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "24704", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1050mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "13380", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1050mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "17394", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1050mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "18732", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1050mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "21408", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1050mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "26760", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1100mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "14462", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1100mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "18800.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1100mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "20246.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1100mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "23139.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1100mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "28924", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1200mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "17082", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1200mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "22206.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1200mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "23914.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1200mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "27331.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1200mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "34164", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1500mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "26701", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1500mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "34711.3", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1500mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "37381.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1500mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "42721.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M30) (1500mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "53402", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M30"]
                },
                "Concreting of bored pile (M35) (450mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3021", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (450mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "3927.3", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (450mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4229.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (450mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "4833.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (450mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "6042", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (475mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3178", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (475mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "4131.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (475mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4449.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (475mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "5084.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (475mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "6356", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (500mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3311", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (500mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "4304.3", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (500mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4635.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (500mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "5297.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (500mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "6622", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (525mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3452", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (525mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "4487.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (525mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "4832.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (525mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "5523.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (525mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "6904", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (550mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "3606", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (550mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "4687.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (550mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "5048.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (550mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "5769.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (550mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "7212", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (600mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "5217", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (600mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "6782.1", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (600mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "7303.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (600mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "8347.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (600mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "10434", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (625mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "5387", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (625mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "7003.1", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (625mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "7541.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (625mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "8619.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (625mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "10774", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (650mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "5563", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (650mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "7231.9", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (650mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "7788.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (650mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "8900.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (650mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "11126", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (750mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "8075", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (750mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "10497.5", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (750mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "11305", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (750mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "12920", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (750mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "16150", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (800mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "8536", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (800mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "11096.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (800mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "11950.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (800mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "13657.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (800mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "17072", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (825mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "8806", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (825mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "11447.8", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (825mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "12328.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (825mm) (15 to 20m)": {
                    "unit": "Rmt", "rate": "14089.6", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (825mm) (Above 20m)": {
                    "unit": "Rmt", "rate": "17612", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (900mm) (0 to 5m)": {
                    "unit": "Rmt", "rate": "9598", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (900mm) (5 to 10m)": {
                    "unit": "Rmt", "rate": "12477.4", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                },
                "Concreting of bored pile (M35) (900mm) (10 to 15m)": {
                    "unit": "Rmt", "rate": "13437.2", "source": "Maha PWD SOR",
                    "carbon": "0.11", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": False, "grades": ["M35"]
                }
            },

            "Pile Cap": {
                "Steel Rebar (Fe500)": {
                    "unit": "MT", "rate": "88341", "source": "Maha PWD SOR",
                    "carbon": "2.6", "carbon_unit": "kgCO₂e/kg", "conv": "1000",
                    "c_source": "IFC", "recyclable": True, "grades": ["Fe500", "Fe500D", "Fe550"]
                },
                "Concreting of Pile cap M20": {
                    "unit": "cum", "rate": "7050", "source": "Maha PWD SOR",
                    "carbon": "2.6", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": True, "grades": ["M20"]
                },
                "Concreting of Pile cap M25": {
                    "unit": "cum", "rate": "7263", "source": "Maha PWD SOR",
                    "carbon": "2.6", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": True, "grades": ["M25"]
                },
                "Concreting of Pile cap M30": {
                    "unit": "cum", "rate": "7381", "source": "Maha PWD SOR",
                    "carbon": "2.6", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": True, "grades": ["M30"]
                },
                "Concreting of Pile cap M35": {
                    "unit": "cum", "rate": "7853", "source": "Maha PWD SOR",
                    "carbon": "2.6", "carbon_unit": "kgCO₂e/kg", "conv": "2400",
                    "c_source": "IFC", "recyclable": True, "grades": ["M35"]
                }
            },
            
            "PCC": {
                 "Plain Cement Concrete M10": {
                    "unit": "cum", "rate": "5500", "source": "Maha PWD SOR",
                    "carbon": "2.4", "carbon_unit": "kgCO₂e/kg", "conv": "2300",
                    "c_source": "IFC", "recyclable": True, "grades": ["M10"]
                },
                "Plain Cement Concrete M15": {
                    "unit": "cum", "rate": "5800", "source": "Maha PWD SOR",
                    "carbon": "2.5", "carbon_unit": "kgCO₂e/kg", "conv": "2300",
                    "c_source": "IFC", "recyclable": True, "grades": ["M15"]
                }
            }
        }

        # --- 2. SELECT RELEVANT DATA ---
        # Get data specific to the component. If not found, look for "General" or fallback to empty.
        self.standard_db = self.master_db.get(self.component_name, {})
        
        # Merge keys: Component-Specific Standard DB + Existing Data.py keys
        self.all_keys = sorted(list(set(list(self.material_data_source.keys()) + list(self.standard_db.keys()))))
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header - Dynamic Component Name
        header_text = QLabel(f"Region: India, Selected SOR: Bihar SOR 2025\nAdding in Foundation > {self.component_name} Component")
        header_text.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 10px;")
        layout.addWidget(header_text)
        
        # Form Layout
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(10)
        self.form_layout.setLabelAlignment(Qt.AlignLeft)
        
        # -- Fields --
        
        # 1. Material Searchable Combo
        self.material_combo = QComboBox()
        self.material_combo.setEditable(True)
        self.material_combo.setInsertPolicy(QComboBox.NoInsert) 
        self.material_combo.setPlaceholderText("Search or type new custom material...")
        self.material_combo.addItems(self.all_keys)
        self.material_combo.setCurrentIndex(-1)
        
        # Setup Professional Completer
        completer = self.material_combo.completer()
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        
        self.material_combo.currentTextChanged.connect(self.on_material_changed)
        self.form_layout.addRow("Material", self.material_combo)

        # Status Label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-size: 11px; margin-left: 2px;")
        self.form_layout.addRow("", self.status_label)

        # Grade
        self.grade_combo = QComboBox()
        self.grade_combo.setEditable(True) 
        self.form_layout.addRow("Grade", self.grade_combo)
        
        # Quantity
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setValidator(QDoubleValidator(0.001, 9999999.99, 3))
        self.form_layout.addRow("Quantity (Unit_A) *", self.quantity_edit)
        
        # Unit
        self.unit_combo = QComboBox()
        self.unit_combo.setEditable(True) 
        self.form_layout.addRow("Unit_A *", self.unit_combo)
        
        # Rate
        self.rate_edit = QLineEdit()
        self.rate_edit.setValidator(QDoubleValidator(0.0, 9999999.99, 2))
        self.form_layout.addRow("Rupees/Unit_A *", self.rate_edit)
        
        # Rate Source
        self.rate_source_edit = QLineEdit()
        self.form_layout.addRow("Rate source *", self.rate_source_edit)
        
        # Carbon Emission
        self.carbon_edit = QLineEdit()
        self.carbon_edit.setPlaceholderText("Optional (or NA)")
        self.form_layout.addRow("Carbon emission (kgCO₂e/Unit_B)", self.carbon_edit)
        
        # Carbon Units
        self.carbon_unit_edit = QLineEdit()
        self.form_layout.addRow("Carbon emission units", self.carbon_unit_edit)
        
        # Conversion Factor
        self.conv_factor_edit = QLineEdit()
        self.conv_factor_edit.setValidator(QDoubleValidator(0.001, 9999999.99, 4))
        self.form_layout.addRow("Conversion factor (Unit_A → Unit_B) *", self.conv_factor_edit)
        
        # Carbon Source
        self.carbon_source_edit = QLineEdit()
        self.form_layout.addRow("Carbon factor source", self.carbon_source_edit)
        
        layout.addLayout(self.form_layout)
        
        # Inline Error Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-weight: bold; font-size: 11px;")
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)

        # Checkboxes
        self.recyclable_check = QCheckBox("Recyclable")
        layout.addWidget(self.recyclable_check)
        
        # Edit Checkbox
        self.edit_check = QCheckBox("Edit")
        self.edit_check.toggled.connect(self.on_edit_toggled)
        self.edit_check.setVisible(False) 
        layout.addWidget(self.edit_check)
        
        # Save DB Checkbox
        self.save_db_check = QCheckBox("Save to database")
        self.save_db_check.setVisible(False)
        layout.addWidget(self.save_db_check)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("+ Add Material")
        self.add_btn.setStyleSheet("background-color: #007BFF; color: white; padding: 6px; border-radius: 4px;")
        self.add_btn.clicked.connect(self.validate_and_accept)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setStyleSheet("background-color: #DC3545; color: white; padding: 6px; border-radius: 4px;")
        self.exit_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.exit_btn)
        
        layout.addLayout(btn_layout)
        
        self.on_material_changed(self.material_combo.currentText())

    def on_material_changed(self, text):
        self.error_label.setText("") 
        
        std_data = None
        exact_key = ""
        
        # 1. Check Component-Specific Standard DB
        for key, val in self.standard_db.items():
            if key.lower() == text.lower():
                std_data = val
                exact_key = key
                break
        
        # 2. Check Data.py
        data_py_data = None
        if not std_data:
            for key, val in self.material_data_source.items():
                if key.lower() == text.lower():
                    data_py_data = val
                    exact_key = key
                    break
        
        if std_data:
            # Found in Standard DB (Fully Defined)
            self.status_label.setText(f"✅ Found standard material: {exact_key}")
            self.status_label.setStyleSheet("color: green; font-size: 11px; margin-left: 2px;")
            
            self.edit_check.setVisible(True)
            self.edit_check.setChecked(False)
            self.save_db_check.setVisible(False)
            
            self.grade_combo.blockSignals(True)
            self.grade_combo.clear()
            self.grade_combo.addItems(std_data.get("grades", []))
            self.grade_combo.blockSignals(False)
            
            self.unit_combo.clear()
            self.unit_combo.addItem(std_data.get("unit", ""))
            
            self.rate_edit.setText(str(std_data.get("rate", "")))
            self.rate_source_edit.setText(std_data.get("source", ""))
            self.carbon_edit.setText(str(std_data.get("carbon", "")))
            self.carbon_unit_edit.setText(std_data.get("carbon_unit", ""))
            self.conv_factor_edit.setText(str(std_data.get("conv", "")))
            self.carbon_source_edit.setText(std_data.get("c_source", ""))
            self.recyclable_check.setChecked(std_data.get("recyclable", False))
            
            self.set_fields_readonly(True)
            
        elif data_py_data:
            # Found in Data.py (Partially Defined)
            self.status_label.setText(f"✅ Found standard material: {exact_key}")
            self.status_label.setStyleSheet("color: green; font-size: 11px; margin-left: 2px;")
            
            self.edit_check.setVisible(True)
            self.edit_check.setChecked(False)
            self.save_db_check.setVisible(False)
            
            grades = data_py_data.get(KEY_GRADE, [])
            units = data_py_data.get(KEY_UNITS, [])
            
            self.grade_combo.blockSignals(True)
            self.grade_combo.clear()
            self.grade_combo.addItems(grades)
            self.grade_combo.blockSignals(False)
            
            self.unit_combo.clear()
            self.unit_combo.addItems(units)
            
            self.set_fields_readonly(True)
            
            self.rate_edit.clear()
            self.rate_source_edit.clear()
            self.carbon_edit.clear()
            self.carbon_unit_edit.clear()
            self.conv_factor_edit.clear()
            self.carbon_source_edit.clear()
            self.recyclable_check.setChecked(False)
            
        else:
            # Custom Material
            if text.strip():
                self.status_label.setText("✏️ Creating new custom material")
                self.status_label.setStyleSheet("color: #007BFF; font-size: 11px; margin-left: 2px;")
            else:
                self.status_label.setText("")

            self.edit_check.setVisible(False)
            self.save_db_check.setVisible(True)
            self.set_fields_readonly(False)
            
            if self.grade_combo.count() == 0:
                self.grade_combo.setEditable(True)

    def on_edit_toggled(self, checked):
        if checked:
            self.set_fields_readonly(False)
            self.rate_source_edit.clear()
            self.carbon_source_edit.clear()
            self.save_db_check.setVisible(True)
            self.save_db_check.setChecked(False)
            self.edit_check.setVisible(False) 
        else:
            self.set_fields_readonly(True)
            self.save_db_check.setVisible(False)

    def set_fields_readonly(self, readonly):
        self.unit_combo.setEnabled(not readonly)
        self.grade_combo.setEnabled(not readonly)
        self.rate_edit.setReadOnly(readonly)
        self.rate_source_edit.setReadOnly(readonly)
        self.carbon_edit.setReadOnly(readonly)
        self.carbon_unit_edit.setReadOnly(readonly)
        self.conv_factor_edit.setReadOnly(readonly)
        self.carbon_source_edit.setReadOnly(readonly)
        self.recyclable_check.setEnabled(not readonly)
        
        style = "background-color: #E0E0E0;" if readonly else "background-color: #FFFFFF;"
        for widget in [self.rate_edit, self.rate_source_edit, self.carbon_edit, 
                       self.carbon_unit_edit, self.conv_factor_edit, self.carbon_source_edit]:
            widget.setStyleSheet(style)
        self.unit_combo.setStyleSheet(style)
        self.grade_combo.setStyleSheet(style)

    def validate_and_accept(self):
        self.error_label.setText("")
        
        name = self.material_combo.currentText().strip()
        if not name:
            self.error_label.setText("Error: Material name is required.")
            return

        errors = []
        
        # Quantity
        try:
            qty = float(self.quantity_edit.text())
            if qty <= 0: errors.append("Quantity must be > 0.")
        except ValueError:
            errors.append("Quantity must be a valid number.")

        # Unit
        if not self.unit_combo.currentText().strip():
            errors.append("Unit cannot be empty.")

        # Price
        try:
            price = float(self.rate_edit.text())
            if price < 0: errors.append("Price must be a valid number.")
        except ValueError:
            errors.append("Price must be a valid number.")

        # Rate Source
        if not self.rate_source_edit.text().strip():
            errors.append("Rate Source is required.")

        # Conversion Factor
        try:
            conv = float(self.conv_factor_edit.text())
            if conv <= 0: errors.append("Conversion Factor must be > 0.")
        except ValueError:
            errors.append("Conversion Factor must be a valid number.")

        # Carbon Emission
        c_text = self.carbon_edit.text().strip()
        if c_text and c_text.lower() != "na":
            try:
                c_val = float(c_text)
                if c_val < 0: errors.append("Carbon Emission must be ≥ 0.")
            except ValueError:
                errors.append("Carbon Emission must be a number or 'NA'.")

        # Duplicate Name Check
        if self.save_db_check.isChecked():
            existing_keys = [k.lower() for k in self.material_data_source.keys()]
            std_keys = [k.lower() for k in self.standard_db.keys()]
            if name.lower() in existing_keys or name.lower() in std_keys:
                errors.append(f"Material '{name}' already exists in the database.")

        if errors:
            self.error_label.setText("\n".join(errors))
            return

        # Prepare Result
        is_custom = True
        for key in self.standard_db.keys():
            if key.lower() == name.lower():
                is_custom = False; break
        if is_custom:
            for key in self.material_data_source.keys():
                if key.lower() == name.lower():
                    is_custom = False; break

        self.result_data = {
            KEY_TYPE: name,
            KEY_GRADE: self.grade_combo.currentText(),
            KEY_QUANTITY: self.quantity_edit.text(),
            KEY_UNIT_M3: self.unit_combo.currentText(),
            KEY_RATE: self.rate_edit.text(),
            KEY_RATE_DATA_SOURCE: self.rate_source_edit.text(),
            "carbon_emission": self.carbon_edit.text(),
            "carbon_unit": self.carbon_unit_edit.text(),
            "conversion_factor": self.conv_factor_edit.text(),
            "carbon_source": self.carbon_source_edit.text(),
            "recyclable": self.recyclable_check.isChecked(),
            "save_to_db": self.save_db_check.isChecked(),
            "is_custom": is_custom
        }
        self.accept()

    def get_data(self):
        return self.result_data

# --- COMPONENT WIDGET ---
class ComponentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self._initializing = True
        self.data = construction_materials.get(KEY_FOUNDATION)
        self.material_rows = []
        self.current_material_row_idx = 1

        self.init_ui()
        self._initializing = False

    def init_ui(self):
        self.component_first_scroll_content_layout = QVBoxLayout(self)
        self.component_first_scroll_content_layout.setContentsMargins(10, 10, 10, 10)
        self.component_first_scroll_content_layout.setSpacing(10)

        component_header_layout = QHBoxLayout()
        component_label = QLabel("Component:")
        component_label.setContentsMargins(0, 5, 0, 5)
        component_header_layout.addWidget(component_label)

        self.component_combobox = QComboBox()
        self.component_combobox.currentTextChanged.connect(self.update_comp_material)
        
        comp_items = list(self.data.keys())
        if "PCC" not in comp_items:
            comp_items.append("PCC")
        self.component_combobox.addItems(comp_items)

        self.component_combobox.currentTextChanged.connect(self._on_value_changed)
        self.component_combobox.setContentsMargins(0, 5, 0, 5)
        component_header_layout.addWidget(self.component_combobox)

        self.remove_component_button = QPushButton("x")
        self.remove_component_button.setFixedSize(24, 24)
        self.remove_component_button.setStyleSheet("""
            QPushButton {
                background-color: #FFCCCC;
                border: 1px solid #FF9999;
                border-radius: 12px;
                font-weight: bold;
                line-height:12px;
                padding: 0px;
                color: #CC0000;
            }
            QPushButton:hover {
                background-color: #FF9999;
                color: white;
            }
            QPushButton:pressed {
                background-color: #FF6666;
            }
        """)
        component_header_layout.addWidget(self.remove_component_button)
        component_header_layout.addStretch(1)

        self.component_first_scroll_content_layout.addLayout(component_header_layout)

        self.material_grid_layout = QGridLayout()
        self.material_grid_layout.setHorizontalSpacing(10)
        self.material_grid_layout.setVerticalSpacing(5)

        headers = ["Type of Material", "Grade", "Quantity", "Unit", "Rate", "Rate Data Source"]
        for col, header_text in enumerate(headers):
            label = QLabel(header_text)
            label.setAlignment(Qt.AlignCenter)
            label.setObjectName("MaterialGridLabel")
            self.material_grid_layout.addWidget(label, 0, col)

        self.component_first_scroll_content_layout.addLayout(self.material_grid_layout)

        self.add_material_row()
        self.add_material_row()

        self.update_comp_material(self.component_combobox.currentText())

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.add_material_button = QPushButton("+ Add Material")
        self.add_material_button.setObjectName("add_material_button")
        self.add_material_button.clicked.connect(self.open_add_material_popup)
        buttons_layout.addWidget(self.add_material_button)
        
        buttons_layout.addStretch()
        
        self.component_first_scroll_content_layout.addLayout(buttons_layout)
        
    def set_locked(self, locked):
        self.component_combobox.setEnabled(not locked)
        self.add_material_button.setEnabled(not locked)
        self.remove_component_button.setEnabled(not locked)
        
        for row in self.material_rows:
            row[KEY_TYPE].setEnabled(not locked)
            row[KEY_GRADE].setEnabled(not locked)
            row[KEY_QUANTITY].setEnabled(not locked)
            row[KEY_UNIT_M3].setEnabled(not locked)
            row[KEY_RATE].setEnabled(not locked)
            row[KEY_RATE_DATA_SOURCE].setEnabled(not locked)
            row['remove_button'].setEnabled(not locked)
    
    def collect_data(self):
        rows_data = []
        for row in self.material_rows:
            component = self.component_combobox.currentText()
            
            widget_type = row[KEY_TYPE]
            if isinstance(widget_type, QComboBox):
                material_type = widget_type.currentText()
            else:
                material_type = widget_type.text()

            widget_grade = row[KEY_GRADE]
            if isinstance(widget_grade, QComboBox):
                material_grade = widget_grade.currentText()
            else:
                material_grade = widget_grade.text()

            widget_unit = row[KEY_UNIT_M3]
            if isinstance(widget_unit, QComboBox):
                unit_m3 = widget_unit.currentText()
            else:
                unit_m3 = widget_unit.text()

            quantity = row[KEY_QUANTITY].text()
            rate = row[KEY_RATE].text()
            rate_data_source = row[KEY_RATE_DATA_SOURCE].text()
            
            row_dict = { KEY_COMPONENT: component,
                         KEY_TYPE: material_type,
                         KEY_GRADE: material_grade,
                         KEY_QUANTITY: quantity if quantity.strip() else "0",
                         KEY_UNIT_M3: unit_m3,
                         KEY_RATE: rate if rate.strip() else "0.00",
                         KEY_RATE_DATA_SOURCE: rate_data_source,
                         "carbon_emission": row.get("carbon_emission", ""),
                         "carbon_unit": row.get("carbon_unit", ""),
                         "conversion_factor": row.get("conversion_factor", ""),
                         "carbon_source": row.get("carbon_source", ""),
                         "recyclable": row.get("recyclable", False),
                         "save_to_db": row.get("save_to_db", False)
                        }
            rows_data.append(row_dict)
        return rows_data

    def _on_value_changed(self, *_args):
        if getattr(self, "_initializing", False):
            return
        if self.parent_widget and hasattr(self.parent_widget, "mark_state_changed"):
            self.parent_widget.mark_state_changed()

    def _on_type_material_changed(self, text, grade_widget, unit_widget):
        self.update_comp_grades(text, grade_widget)
        self.update_comp_units(text, unit_widget)
        self._on_value_changed()

    def update_comp_material(self, selected_component):
        comp_data = self.data.get(selected_component, {})
        materials = comp_data.keys()

        for i in range(len(self.material_rows)):
            material_combo = self.material_rows[i][KEY_TYPE]
            
            if not isinstance(material_combo, QComboBox):
                continue

            grade_combo = self.material_rows[i][KEY_GRADE]
            unit_combo = self.material_rows[i][KEY_UNIT_M3]
            material_combo.clear()
            material_combo.addItems(materials)
            current_text = material_combo.currentText()
            if current_text:
                self.update_comp_grades(current_text, grade_combo)
                self.update_comp_units(current_text, unit_combo)
        self._on_value_changed()
    
    def update_comp_grades(self, selected_material, widget):
        selected_component = self.component_combobox.currentText()
        grades = self.data.get(selected_component,{}).get(selected_material,{}).get(KEY_GRADE,[])
        widget.clear()
        widget.addItems(grades)
    
    def update_comp_units(self, selected_material, widget):
        selected_component = self.component_combobox.currentText()
        units = self.data.get(selected_component,{}).get(selected_material,{}).get(KEY_UNITS,[])
        widget.clear()
        widget.addItems(units)

    def open_add_material_popup(self):
        selected_component = self.component_combobox.currentText()
        materials_data = self.data.get(selected_component, {})
        
        # --- FIXED: PASS COMPONENT NAME TO POPUP ---
        popup = MaterialInputPopup(materials_data, selected_component, self)
        if popup.exec() == QDialog.Accepted:
            data = popup.get_data()
            self.add_row_from_popup_data(data)

    def add_row_from_popup_data(self, data):
        if data.get('is_custom', False):
            self.add_custom_material_row(data)
        else:
            self.add_material_row(data)

    def add_custom_material_row(self, data=None):
        validator = QDoubleValidator()
        validator.setRange(0.0, 9999999.999, 3)
        validator.setBottom(0.0)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
    
        row_widgets = {}
        row_idx = self.current_material_row_idx
        
        type_material_input = QLineEdit()
        type_material_input.setPlaceholderText("Enter custom material")
        type_material_input.setObjectName("MaterialGridInput")
        type_material_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(type_material_input, row_idx, 0)
        row_widgets[KEY_TYPE] = type_material_input
        type_material_input.textChanged.connect(self._on_value_changed)

        grade_input = QComboBox() 
        grade_input.setEditable(True)
        grade_input.setObjectName("MaterialGridInput")
        grade_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(grade_input, row_idx, 1)
        row_widgets[KEY_GRADE] = grade_input
        grade_input.currentTextChanged.connect(self._on_value_changed)

        quantity_edit = QLineEdit()
        quantity_edit.setValidator(validator)
        quantity_edit.setPlaceholderText("0")
        quantity_edit.setObjectName("MaterialGridInput")
        quantity_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(quantity_edit, row_idx, 2)
        row_widgets[KEY_QUANTITY] = quantity_edit
        quantity_edit.textChanged.connect(self._on_value_changed)

        unit_combo_m3 = QComboBox()
        unit_combo_m3.setEditable(True)
        unit_combo_m3.setObjectName("MaterialGridInput")
        unit_combo_m3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(unit_combo_m3, row_idx, 3)
        row_widgets[KEY_UNIT_M3] = unit_combo_m3
        unit_combo_m3.currentTextChanged.connect(self._on_value_changed)

        rate_edit = QLineEdit()
        rate_edit.setValidator(validator)
        rate_edit.setPlaceholderText("0.00")
        rate_edit.setObjectName("MaterialGridInput")
        rate_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(rate_edit, row_idx, 4)
        row_widgets[KEY_RATE] = rate_edit
        rate_edit.textChanged.connect(self._on_value_changed)

        rate_data_source_edit = QLineEdit()
        rate_data_source_edit.setObjectName("MaterialGridInput")
        rate_data_source_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(rate_data_source_edit, row_idx, 5)
        row_widgets[KEY_RATE_DATA_SOURCE] = rate_data_source_edit
        rate_data_source_edit.textChanged.connect(self._on_value_changed)

        remove_button = QPushButton("x")
        remove_button.setFixedSize(24, 24)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #FFCCCC;
                border: 1px solid #FF9999;
                border-radius: 12px;
                font-weight: bold;
                line-height:12px;
                padding: 0px;
                color: #CC0000;
            }
            QPushButton:hover {
                background-color: #FF9999;
                color: white;
            }
            QPushButton:pressed {
                background-color: #FF6666;
            }
        """)
        remove_button.clicked.connect(lambda: self.remove_material_row_by_widgets(row_widgets))
        
        self.material_grid_layout.addWidget(remove_button, row_idx, 6, alignment=Qt.AlignCenter)
        
        row_widgets['remove_button'] = remove_button

        if data:
            type_material_input.setText(data.get(KEY_TYPE, ""))
            grade_input.addItem(data.get(KEY_GRADE, ""))
            quantity_edit.setText(data.get(KEY_QUANTITY, ""))
            unit_combo_m3.addItem(data.get(KEY_UNIT_M3, ""))
            rate_edit.setText(data.get(KEY_RATE, ""))
            rate_data_source_edit.setText(data.get(KEY_RATE_DATA_SOURCE, ""))
            row_widgets["carbon_emission"] = data.get("carbon_emission")
            row_widgets["carbon_unit"] = data.get("carbon_unit")
            row_widgets["conversion_factor"] = data.get("conversion_factor")
            row_widgets["carbon_source"] = data.get("carbon_source")
            row_widgets["recyclable"] = data.get("recyclable")
            row_widgets["save_to_db"] = data.get("save_to_db")

        self.material_rows.append(row_widgets)
        self.current_material_row_idx += 1
        
        self.updateGeometry()
        self.adjustSize()
        self._on_value_changed()

    def add_material_row(self, data=None):
        validator = QDoubleValidator()
        validator.setRange(0.0, 9999999.999, 3)
        validator.setBottom(0.0)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
    
        row_widgets = {}
        row_idx = self.current_material_row_idx

        type_material_combo = QComboBox()
        type_material_combo.setObjectName("MaterialGridInput")
        type_material_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(type_material_combo, row_idx, 0)
        row_widgets[KEY_TYPE] = type_material_combo

        grade_combo = QComboBox()
        grade_combo.setObjectName("MaterialGridInput")
        grade_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(grade_combo, row_idx, 1)
        row_widgets[KEY_GRADE] = grade_combo
        grade_combo.currentTextChanged.connect(self._on_value_changed)

        quantity_edit = QLineEdit()
        quantity_edit.setValidator(validator)
        quantity_edit.setPlaceholderText("0")
        quantity_edit.setObjectName("MaterialGridInput")
        quantity_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(quantity_edit, row_idx, 2)
        row_widgets[KEY_QUANTITY] = quantity_edit
        quantity_edit.textChanged.connect(self._on_value_changed)

        unit_combo_m3 = QComboBox()
        unit_combo_m3.setObjectName("MaterialGridInput")
        unit_combo_m3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(unit_combo_m3, row_idx, 3)
        row_widgets[KEY_UNIT_M3] = unit_combo_m3
        unit_combo_m3.currentTextChanged.connect(self._on_value_changed)

        rate_edit = QLineEdit()
        rate_edit.setValidator(validator)
        rate_edit.setPlaceholderText("0.00")
        rate_edit.setObjectName("MaterialGridInput")
        rate_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(rate_edit, row_idx, 4)
        row_widgets[KEY_RATE] = rate_edit
        rate_edit.textChanged.connect(self._on_value_changed)

        rate_data_source_edit = QLineEdit()
        rate_data_source_edit.setObjectName("MaterialGridInput")
        rate_data_source_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.material_grid_layout.addWidget(rate_data_source_edit, row_idx, 5)
        row_widgets[KEY_RATE_DATA_SOURCE] = rate_data_source_edit
        rate_data_source_edit.textChanged.connect(self._on_value_changed)

        remove_button = QPushButton("x")
        remove_button.setFixedSize(24, 24)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #FFCCCC;
                border: 1px solid #FF9999;
                border-radius: 12px;
                font-weight: bold;
                line-height:12px;
                padding: 0px;
                color: #CC0000;
            }
            QPushButton:hover {
                background-color: #FF9999;
                color: white;
            }
            QPushButton:pressed {
                background-color: #FF6666;
            }
        """)
        remove_button.clicked.connect(lambda: self.remove_material_row_by_widgets(row_widgets))
        
        self.material_grid_layout.addWidget(remove_button, row_idx, 6, alignment=Qt.AlignCenter)
        
        row_widgets['remove_button'] = remove_button

        type_material_combo.currentTextChanged.connect(
            lambda text, grade_widget=grade_combo, unit_widget=unit_combo_m3: self._on_type_material_changed(text, grade_widget, unit_widget)
        )

        self.material_rows.append(row_widgets)
        self.current_material_row_idx += 1

        selected_component = self.component_combobox.currentText()
        materials = list(self.data.get(selected_component, {}).keys())
        type_material_combo.addItems(materials)
        
        if data:
            type_material_combo.blockSignals(True)
            index = type_material_combo.findText(data.get(KEY_TYPE, ""))
            if index != -1:
                type_material_combo.setCurrentIndex(index)
            type_material_combo.blockSignals(False)
            
            self.update_comp_grades(type_material_combo.currentText(), grade_combo)
            self.update_comp_units(type_material_combo.currentText(), unit_combo_m3)
            
            g_index = grade_combo.findText(data.get(KEY_GRADE, ""))
            if g_index != -1:
                grade_combo.setCurrentIndex(g_index)
            
            quantity_edit.setText(data.get(KEY_QUANTITY, ""))
            
            u_index = unit_combo_m3.findText(data.get(KEY_UNIT_M3, ""))
            if u_index != -1:
                unit_combo_m3.setCurrentIndex(u_index)
                
            rate_edit.setText(data.get(KEY_RATE, ""))
            rate_data_source_edit.setText(data.get(KEY_RATE_DATA_SOURCE, ""))
            
            row_widgets["carbon_emission"] = data.get("carbon_emission")
            row_widgets["carbon_unit"] = data.get("carbon_unit")
            row_widgets["conversion_factor"] = data.get("conversion_factor")
            row_widgets["carbon_source"] = data.get("carbon_source")
            row_widgets["recyclable"] = data.get("recyclable")
        elif materials:
            first_material = materials[0]
            self.update_comp_grades(first_material, grade_combo)
            self.update_comp_units(first_material, unit_combo_m3)

        self.updateGeometry()
        self.adjustSize()
        self._on_value_changed()


    def remove_material_row_by_widgets(self, row_widgets_to_remove):
        if row_widgets_to_remove not in self.material_rows:
            return

        row_idx_in_grid = -1
        for i, row_dict in enumerate(self.material_rows):
            if row_dict == row_widgets_to_remove:
                row_idx_in_grid = i + 1
                break

        if row_idx_in_grid == -1:
            return

        for col in range(self.material_grid_layout.columnCount()):
            item = self.material_grid_layout.itemAtPosition(row_idx_in_grid, col)
            if item:
                if item.widget():
                    widget = item.widget()
                    self.material_grid_layout.removeWidget(widget)
                    widget.deleteLater()
                elif item.layout():
                    layout = item.layout()
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        if sub_item.widget():
                            sub_item.widget().deleteLater()
                    self.material_grid_layout.removeItem(layout)

        self.material_rows.remove(row_widgets_to_remove)
        self.current_material_row_idx -= 1

        for r_idx in range(row_idx_in_grid, self.current_material_row_idx + 1):
            for c_idx in range(self.material_grid_layout.columnCount()):
                item = self.material_grid_layout.itemAtPosition(r_idx + 1, c_idx)
                if item:
                    if item.widget():
                        widget = item.widget()
                        self.material_grid_layout.removeWidget(widget)
                        if c_idx == 6:
                            self.material_grid_layout.addWidget(widget, r_idx, c_idx, alignment=Qt.AlignCenter)
                        else:
                            self.material_grid_layout.addWidget(widget, r_idx, c_idx)
                    elif item.layout():
                        layout = item.layout()
                        self.material_grid_layout.removeItem(layout)
                        self.material_grid_layout.addLayout(layout, r_idx, c_idx)

        self.updateGeometry()
        self.update()
        self.material_grid_layout.invalidate()
        self.adjustSize()
        self._on_value_changed()

class Foundation(QWidget):
    closed = Signal()
    next = Signal(str)
    back = Signal(str)
    def __init__(self, database, parent=None):
        super().__init__()
        self.database_manager = database
        self.data_id = []
        self.setObjectName("central_panel_widget")
        self.component_widgets = []
        self._initializing = True
        self.state_changed = True
        self.is_first_visit = True
        self.is_locked = False
        
        self.setStyleSheet("""
            #central_panel_widget {
                background-color: #F8F8F8;
                border-radius: 8px;
            }
            #central_panel_widget QLabel {
                color: #333333;
                font-size: 12px;
            }
            #central_panel_widget QLabel#page_number_label {
                font-size: 14px;
                font-weight: bold;
                color: #555555;
            }

            QScrollArea {
                background-color: transparent;
                outline: none;
            }
            #scroll_content_widget {
                background-color: #FFF9F9;
                border: 1px solid #000000;
                padding-bottom: 20px;
            }

            QScrollBar:vertical {
                border: 1px solid #E0E0E0;
                background: #F0F0F0;
                width: 12px;
                margin: 18px 0px 18px 0px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background: #C0C0C0;
                border: 1px solid #A0A0A0;
                min-height: 20px;
                border-radius: 5px;
            }

            QScrollBar::add-line:vertical {
                border: 1px solid #E0E0E0;
                background: #E8E8E8;
                height: 18px;
                subcontrol-origin: bottom;
                subcontrol-position: bottom;
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            QScrollBar::sub-line:vertical {
                border: 1px solid #E0E0E0;
                background: #E8E8E8;
                height: 18px;
                subcontrol-origin: top;
                subcontrol-position: top;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                width: 10px;
                height: 10px;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar::up-arrow:vertical {
                image: url(:/images/arrow_up.png);
            }
            QScrollBar::down-arrow:vertical {
                image: url(:/images/arrow_down.png);
            }

            QScrollBar::add-line:vertical:hover, QScrollBar::sub-line:vertical:hover {
                background: #D0D0D0;
            }

            QPushButton#top_button_left_panel {
                background-color: #FDEFEF;
                border-top: 1px solid #000000;
                border-left: 1px solid #000000;
                border-right: 1px solid #000000;
                text-align: left;
                padding: 4px 10px;
                color: #000000;
            }
            QPushButton#top_button_left_panel:hover {
                background-color: #F0E6E6;
                border-color: #808080;
            }
            QPushButton#top_button_left_panel:pressed {
                background-color: #FFF3F3;
                border-color: #606060;
            }

            #component_first_widget {
                background-color: transparent;
                margin-top: 10px;
            }

            #component_first_scroll_content_widget {
                background-color: #FFFFFF;
                padding: 10px;
                border-radius: 8px;
            }

            QPushButton#nav_button {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                color: #3F3E5E;
                padding: 6px 15px;
                text-align: center;
                min-width: 80px;
            }
            QPushButton#nav_button:hover {
                background-color: #F8F8F8;
                border-color: #C0C0C0;
            }
            QPushButton#nav_button:pressed {
                background-color: #E8E8E8;
                border-color: #A0A0A0;
            }
            
            QPushButton#lock_button {
                background-color: #FFF8DC; 
                border: 2px solid #DAA520; 
                border-radius: 12px;
                color: #3F3E5E;
                padding: 2px 2px;
                text-align: center;
                font-weight: bold;
            }
            QPushButton#lock_button:hover {
                background-color: #FFE4B5;
                border-color: #C0C0C0;
            }
            QPushButton#lock_button[locked="true"] {
                background-color: #FFEEEE;
                border-color: #FF9999;
                color: #CC0000;
            }
            QPushButton#lock_button[locked="false"] {
                background-color: #E8F5E9;
                border-color: #45913E;
                color: #00AA00;
            }
            
            QLineEdit {
                text-align: center;
            }
            QComboBox {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
                text-align: center;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 5px;
            }
            QComboBox::down-arrow {
                image: url(:/images/country_arrow.png);
                width: 30px;
                height: 30px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #DDDCE0;
                border-radius: 5px;
                background-color: #FFFFFF;
                outline: none;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #FDEFEF;
                color: #000000;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #FDEFEF;
            }

            #MaterialGridLabel {
                font-weight: bold;
                color: #3F3E5E;
                padding: 5px;
                text-align: center;
            }
            #MaterialGridInput {
                border: 1px solid #DDDCE0;
                border-radius: 10px;
                padding: 3px 10px;
                background-color: #FFFFFF;
            }
            #MaterialGridInput:focus {
                border: 1px solid #DDDCE0;
                background-color: #FFFFFF;
            }
            #MaterialGridInput:disabled {
                background-color: #F0F0F0;
                color: #888888;
            }
            
            QPushButton#add_material_button, QPushButton#add_component_button {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                color: #3F3E5E;
                padding: 6px 15px;
                text-align: center;
            }
            QPushButton#add_material_button:hover, QPushButton#add_component_button:hover {
                background-color: #F8F8F8;
                border-color: #C0C0C0;
            }
            QPushButton#add_material_button:pressed, QPushButton#add_component_button:pressed {
                background-color: #E8E8E8;
                border-color: #A0A0A0;
            }
            QPushButton#add_material_button:disabled, QPushButton#add_component_button:disabled {
                background-color: #F0F0F0;
                color: #AAAAAA;
                border-color: #D0D0D0;
            }
        """)
        
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0,0,0,0)
        left_panel_vlayout.setSpacing(0)

        lock_hlayout = QHBoxLayout()
        lock_hlayout.setContentsMargins(0,2,2,0)
        lock_hlayout.setSpacing(0)
        lock_hlayout.addStretch()

        self.lock_button = QPushButton("🔓")
        self.lock_button.setObjectName("lock_button")
        self.lock_button.setFixedSize(24, 24)
        self.lock_button.setProperty("locked", "false")
        self.lock_button.clicked.connect(self.toggle_lock)
        lock_hlayout.addWidget(self.lock_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content_widget)

        self.scroll_content_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(0,0,0,0)
        self.scroll_content_layout.setSpacing(0)

        self.scroll_content_layout.addLayout(lock_hlayout)

        self.add_component_button = QPushButton("+ Add Component")
        self.add_component_button.setObjectName("add_component_button")
        self.add_component_button.clicked.connect(self.add_component_layout)

        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.setSpacing(10)
        self.button_h_layout.setContentsMargins(10,10,10,10)

        self.button_h_layout.addStretch(6)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        next_button.clicked.connect(self.on_next_clicked)
        self.button_h_layout.addWidget(next_button)

        self.add_component_layout()

        self.scroll_content_layout.addLayout(self.button_h_layout)
        left_panel_vlayout.addWidget(self.scroll_area)
        self._initializing = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self.is_first_visit:
            self.set_form_locked(True)
        else:
            self.is_first_visit = False

    def toggle_lock(self):
        self.set_form_locked(not self.is_locked)
    
    def set_form_locked(self, locked):
        self.is_locked = locked
        
        if locked:
            self.lock_button.setText("🔒")
            self.lock_button.setProperty("locked", "true")
        else:
            self.lock_button.setText("🔓")
            self.lock_button.setProperty("locked", "false")
        
        self.lock_button.style().unpolish(self.lock_button)
        self.lock_button.style().polish(self.lock_button)
        
        for component_widget in self.component_widgets:
            component_widget.set_locked(locked)
        
        self.add_component_button.setEnabled(not locked)

    def collect_data(self):
        all_data = []
        for component_widget in self.component_widgets:
            component_data = component_widget.collect_data()
            all_data.append(component_data)
        return all_data
    
    def mark_state_changed(self):
        if self._initializing:
            return
        self.state_changed = True
    
    def save_data(self):
        from pprint import pprint
        data = self.collect_data()
        print("\nCollected Data from Foundation UI:")
        pprint(data)
            
        if self.data_id:
            self.data_id = self.database_manager.replace_structure_work_rows(KEY_FOUNDATION, data, self.data_id)
        else:
            self.data_id = self.database_manager.input_data_row(KEY_FOUNDATION, data)
        self.state_changed = False

    def on_next_clicked(self):
        if not self.state_changed:
            self.next.emit(KEY_FOUNDATION)
            return
        if self.data_id:
            message = "Do you want to replace previous data?"
        else:
            message = "Do you want to save data?"
        reply = QMessageBox.question(self, "Confirm", message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.save_data()
        self.next.emit(KEY_FOUNDATION)

    def add_component_layout(self):
        new_component = ComponentWidget(self)
        self.component_widgets.append(new_component)
        new_component.remove_component_button.clicked.connect(lambda: self.remove_component_layout(new_component))

        if self.scroll_content_layout.indexOf(self.add_component_button) != -1:
            self.scroll_content_layout.removeWidget(self.add_component_button)
        if self.scroll_content_layout.indexOf(self.button_h_layout) != -1:
            self.scroll_content_layout.removeItem(self.button_h_layout)

        self.scroll_content_layout.addWidget(new_component)
        self.scroll_content_layout.addWidget(self.add_component_button, alignment=Qt.AlignCenter)
        self.scroll_content_layout.addLayout(self.button_h_layout) 

        if self.is_locked:
            new_component.set_locked(True)

        self.scroll_area.widget().updateGeometry()
        self.scroll_area.widget().adjustSize()
        self.mark_state_changed()

    def remove_component_layout(self, component_to_remove):
        if component_to_remove in self.component_widgets:
            self.scroll_content_layout.removeWidget(component_to_remove)
            self.component_widgets.remove(component_to_remove)
            component_to_remove.deleteLater()
            self.scroll_area.widget().updateGeometry()
            self.scroll_area.widget().adjustSize()
            self.mark_state_changed()

    def expand_scroll_area(self):
        pass

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)