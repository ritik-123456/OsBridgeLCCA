"""
<Author>: Prerna Praveen Vidyarthi
<Intern>: FOSSEE Summer Fellowship 2025
<Github>: https://github.com/prerna2024-cyber
<Email>: vidyarthiprerna637@gmail.com
"""
from PySide6.QtCore import (QSize, Qt, QPropertyAnimation, QEasingCurve)
from PySide6.QtGui import (QAction,QFont, QFontDatabase, QIcon)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QTextEdit, QScrollArea, QSpacerItem, QSizePolicy,
    QMenu, QMenuBar, QPushButton, QWidget, QLabel, QVBoxLayout, QGridLayout, QLineEdit, QComboBox)

from osbridgelcca.desktop_app.widgets.title_bar import CustomTitleBar
from osbridgelcca.desktop_app.widgets.project_details_right_widget import ProjectDetailsWidget
from osbridgelcca.desktop_app.widgets.tutorial_widget_left import TutorialWidget
from osbridgelcca.desktop_app.widgets.results_widget import ResultsWidget
from osbridgelcca.desktop_app.widgets.comparison_widget import ComparisonWidget
from osbridgelcca.desktop_app.widgets.structure_works_data.foundation_widget import Foundation
from osbridgelcca.desktop_app.widgets.structure_works_data.super_structure_widget import SuperStructure
from osbridgelcca.desktop_app.widgets.structure_works_data.sub_structure_widget import SubStructure
from osbridgelcca.desktop_app.widgets.structure_works_data.auxiliary_works_widget import AuxiliaryWorks
from osbridgelcca.desktop_app.widgets.financial_data import FinancialData
from osbridgelcca.desktop_app.widgets.carbon_emission_data.carbon_emission_data import CarbonEmissionData
from osbridgelcca.desktop_app.widgets.carbon_emission_data.carbon_emission_cost_data import CarbonEmissionCostData
from osbridgelcca.desktop_app.widgets.bridge_and_traffic_data import BridgeAndTrafficData
from osbridgelcca.desktop_app.widgets.maintenance_repair_data import MaintenanceRepairData
from osbridgelcca.desktop_app.widgets.demolition_and_recycling_data import DemolitionAndRecyclingData
from osbridgelcca.desktop_app.widgets.project_details_left_widget import ProjectDetailsLeft
from osbridgelcca.desktop_app.widgets.tab_widget import CustomTabWidget
from osbridgelcca.desktop_app.widgets.utils.data import *
from osbridgelcca.desktop_app.widgets.utils.database import DatabaseManager
from osbridgelcca.desktop_app.resources.resources_rc import *
from PySide6.QtWidgets import QFileDialog
import pandas as pd
import json
import numpy as np

# ================== CHANGES MADE BY RITIK ==================
# Excel Parsing & Validation Logic (INLINE)

ALLOWED_UNITS = {'cum', 'rmt', 'm2', 'mt'}
FLEXIBLE_FIELD_CONFIG = ['carbon_emission', 'conversion_factor']
ALLOWED_FLEXIBLE_VALUES = {'not_available'}
ALLOWED_RECYCLE_VALUES = {'recycleable', 'recyclable', 'non-recyclable'}

def clean_header(header_val):
    if not isinstance(header_val, str):
        return str(header_val)
    return header_val.replace('CID#', '').lower().strip()

def is_valid_number(val):
    if val is None or val == "":
        return False
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False

def get_row_identifier(sheet, type_name, row_idx):
    return f"Sheet: '{sheet}', Component: '{type_name}', Row: {row_idx + 1}"

def parse_and_validate_excel(file_path):
    try:
        all_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
    except Exception as e:
        return {"fatal_error": f"Failed to read file: {str(e)}"}

    parsed_sections = []
    global_errors = []
    global_warnings = []

    for sheet_name, df in all_sheets.items():

        current_section = None
        current_keys = None
        section_seen_data = {}

        for idx, row in df.iterrows():
            if row.isnull().all():
                continue

            first_val = str(row[0]).strip() if pd.notna(row[0]) else ""

            # 1. Identify Header (CID#)
            if first_val.startswith('CID#'):
                current_keys = []
                for i, val in enumerate(row):
                    if pd.notna(val) and str(val).strip() != "":
                        current_keys.append((i, clean_header(str(val).strip())))
                continue

            # Skip visual headers
            if first_val == 'Material':
                continue

            # 2. Identify Section
            col2 = row[2] if len(row) > 2 else np.nan
            col3 = row[3] if len(row) > 3 else np.nan

            if pd.notna(row[0]) and pd.isna(col2) and pd.isna(col3):
                if current_section:
                    parsed_sections.append(current_section)

                current_section = {
                    "sheetName": sheet_name,
                    "type": first_val,
                    "data": []
                }
                section_seen_data = {}
                continue

            # 3. Process Data Row
            if current_section and current_keys:
                raw_row_data = {}
                for col_idx, key in current_keys:
                    if col_idx < len(row):
                        val = row[col_idx]
                        raw_row_data[key] = None if pd.isna(val) or str(val).strip() == "" else val
                    else:
                        raw_row_data[key] = None

                qty_val = raw_row_data.get('quantity')
                if qty_val is None:
                    continue

                final_row_data = raw_row_data.copy()
                row_has_critical_error = False
                is_duplicate = False
                row_context = get_row_identifier(sheet_name, current_section['type'], idx)

                # Quantity
                if not is_valid_number(qty_val):
                    global_errors.append(f"{row_context} - Error: Quantity '{qty_val}' is not a valid number.")
                    row_has_critical_error = True

                # Rate
                rate_val = final_row_data.get('rate')
                if rate_val is None or not is_valid_number(rate_val):
                    global_errors.append(f"{row_context} - Error: Invalid or missing rate.")
                    row_has_critical_error = True

                # Sources (warnings)
                if final_row_data.get('rate_src') is None:
                    global_warnings.append(f"{row_context} - Warning: 'rate_src' is missing.")
                if final_row_data.get('carbon_emission_src') is None:
                    global_warnings.append(f"{row_context} - Warning: 'carbon_emission_src' is missing.")

                # Flexible fields
                for field in FLEXIBLE_FIELD_CONFIG:
                    val = final_row_data.get(field)
                    if val is not None:
                        val_str = str(val).strip().lower()
                        if not is_valid_number(val) and val_str not in ALLOWED_FLEXIBLE_VALUES:
                            global_errors.append(
                                f"{row_context} - Error: Field '{field}' value '{val}' is invalid."
                            )
                            row_has_critical_error = True

                # Unit
                unit_val = final_row_data.get('unit')
                if not unit_val or str(unit_val).strip().lower() not in ALLOWED_UNITS:
                    global_errors.append(f"{row_context} - Error: Invalid or missing unit.")
                    row_has_critical_error = True

                # Recyclable
                recycle_val = final_row_data.get('recycleable')
                if recycle_val is None or str(recycle_val).strip() == "":
                    global_warnings.append(
                        f"{row_context} - Warning: 'recycleable' blank, assumed non-recyclable."
                    )
                else:
                    if str(recycle_val).strip().lower() not in ALLOWED_RECYCLE_VALUES:
                        global_errors.append(
                            f"{row_context} - Error: Invalid 'recycleable' value '{recycle_val}'."
                        )
                        row_has_critical_error = True

                # Duplicate check
                name_val = final_row_data.get('name')
                if name_val:
                    if name_val in section_seen_data:
                        original = section_seen_data[name_val]
                        if final_row_data == original['data']:
                            global_warnings.append(
                                f"{row_context} - Warning: Duplicate '{name_val}' merged."
                            )
                            is_duplicate = True
                        else:
                            global_errors.append(
                                f"{row_context} - Error: Duplicate '{name_val}' with conflicts."
                            )
                            is_duplicate = True
                    else:
                        section_seen_data[name_val] = {
                            "data": final_row_data,
                            "row_id": row_context
                        }

                if not row_has_critical_error and not is_duplicate:
                    current_section['data'].append(final_row_data)

        if current_section:
            parsed_sections.append(current_section)

    return {
        "validation_report": {
            "errors": global_errors,
            "warnings": global_warnings
        },
        "parsed_data": parsed_sections
    }

   



class UiMainWindow(object):
    def open_excel_dialog(self):
        print("Upload Excel clicked")

        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_path:
            print("No file selected")
            return

        print(f"\nSelected file: {file_path}")

        result = parse_and_validate_excel(file_path)

        if result is None:
            print("[FATAL] Parser returned None. Check parse_and_validate_excel().")
            return

        try:
            result = parse_and_validate_excel(file_path)

            validation = result.get("validation_report", {})
            errors = validation.get("errors", [])
            warnings = validation.get("warnings", [])

            print("\n--- ERRORS ---")
            for e in errors or ["No errors found"]:
                print(e)

            print("\n--- WARNINGS ---")
            for w in warnings or ["No warnings found"]:
                print(w)

            print("\n--- PARSED DATA ---")
            print(json.dumps(result.get("parsed_data", []), indent=2))

        except Exception as e:
            print("[FATAL] Excel parsing failed")
            print(e)

    def setupUi(self, MainWindow):
        self.database_manager = DatabaseManager()
        # To check if tab widget is there or no
        self.tabs_active = False
        # Contains name of widget and its index in tabs
        self.active_tab_widgets = {}
        self.widget_map = {
            KEY_STRUCTURE_WORKS_DATA: Foundation,
            KEY_FOUNDATION: Foundation,
            KEY_SUPERSTRUCTURE: SuperStructure,
            KEY_SUBSTRUCTURE: SubStructure,
            KEY_AUXILIARY: AuxiliaryWorks,
            KEY_FINANCIAL: FinancialData,
            KEY_CARBON_EMISSION: CarbonEmissionData,
            KEY_CARBON_EMISSION_COST: CarbonEmissionCostData,
            KEY_BRIDGE_TRAFFIC: BridgeAndTrafficData,
            KEY_MAINTAINANCE_REPAIR: MaintenanceRepairData,
            KEY_DEMOLITION_RECYCLE: DemolitionAndRecyclingData
        }

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        # Load and set the Alata Regular font
        font_id = QFontDatabase.addApplicationFont(":/font/AlataRegular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app_font = QFont(font_family, 10)
            QApplication.setFont(app_font)
        else:
            print("Failed to load Alata font")

        MainWindow.setWindowTitle("3psLCCA")
        # --- CHANGED: Commented out FramelessWindowHint ---
        # MainWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width()*1//8)
        y = (screen.height()*1//8)
        MainWindow.setGeometry(x, y, screen.width()*3//4, screen.height()*3//4)

        # Set window stylesheet
        MainWindow.setStyleSheet("""
            QMainWindow {
                border: none;
            }
            QMenuBar {
                background-color: #E8F5E9;
                border-bottom: 1px solid #d0d0d0;
                border-left: 1px solid #285A23;
                border-right: 1px solid #285A23;
            }
            QMenuBar::item {
                padding: 4px 10px;
                background-color: transparent;
                border-bottom: 2px solid #FAFAFA;
                margin: 2px;
            }
            QMenuBar::item:selected {
                border-bottom: 2px solid #806C6C;
            }
            QMenu {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
            }
            QMenu::item {
                padding: 4px 4px 4px 12px;
                text-align: left;
                color: #514E4E;
            }
            QMenu::item:selected {
                background-color: #e0e0e0;
            }
            QMenu::separator {
                height: 1px;
                background-color: #d0d0d0;
                margin: 4px 0px;
            }
            QMenu::icon {
                padding-left: 5px;
                width: 16px;
                height: 16px;
            }
            QMenu::indicator {
                width: 16px;
                height: 16px;
            }
            QMenu::right-arrow {
                margin-right: 5px;
            }
        """)

        # Create a central widget and main layout for the window
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("border: none;")
        self.central_widget.setObjectName("central_widget")
        MainWindow.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #     CHANGED: Commented out Custom Title Bar 
        
        # Add the custom title bar to the top of the main layout
        # self.title_bar = CustomTitleBar(MainWindow)
        # main_layout.addWidget(self.title_bar)

        # Create and add menu bar directly to the central widget's main_layout
        # DO NOT use MainWindow.setMenuBar() when using FramelessWindowHint
        self.menubar = QMenuBar()
        self.menubar.setObjectName(u"menubar")
        main_layout.addWidget(self.menubar) # This is the crucial line for custom frame

        # Create menus
        self.menuFile = QMenu("&File", self.menubar)
        self.menuHome = QMenu("&Home", self.menubar)
        self.menuReport = QMenu("&Report", self.menubar)
        self.menuHelp = QMenu("&Help", self.menubar)

        # Add menus to menubar
        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuHome)
        self.menubar.addMenu(self.menuReport)
        self.menubar.addMenu(self.menuHelp)

        # Create and add actions to File menu with icons
        self.actionNew = QAction(QIcon(":/vectors/new.svg"), "New", MainWindow)
        self.actionOpen = QAction(QIcon(":/vectors/open.svg"), "Open", MainWindow)
        self.actionSave = QAction(QIcon(":/vectors/save.svg"), "Save", MainWindow)
        self.actionSaveAs = QAction(QIcon(":/vectors/save_as.svg"), "Save As...", MainWindow)
        self.actionCreateCopy = QAction(QIcon(":/vectors/create_copy.svg"), "Create a Copy", MainWindow)
        self.actionPrint = QAction(QIcon(":/vectors/print.svg"), "Print", MainWindow)
        self.actionRename = QAction(QIcon(":/vectors/rename.svg"), "Rename", MainWindow)
        self.actionExport = QAction(QIcon(":/vectors/export.svg"), "Export", MainWindow)
        self.actionVersionHistory = QAction(QIcon(":/vectors/version_history.svg"), "Version History", MainWindow)
        self.actionInfo = QAction(QIcon(":/vectors/info.svg"), "Info", MainWindow)

        # Add actions to File menu
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionCreateCopy)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRename)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionVersionHistory)
        self.menuFile.addAction(self.actionInfo)

        # Create and add actions to Help menu with icons
        self.actionDocumentation = QAction(QIcon(":/vectors/contact.svg"), "Contact us", MainWindow)
        self.actionFeedback = QAction(QIcon(":/vectors/feedback.svg"), "Feedback", MainWindow)
        self.actionVideoTutorial = QAction(QIcon(":/vectors/video_tutorial.svg"), "Video Tutorials", MainWindow)
        self.actionJoinCommunity = QAction(QIcon(":/vectors/join_community.svg"), "Join our Community", MainWindow)

        # Add actions to Help menu
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionFeedback)
        self.menuHelp.addSeparator()

        self.menuHelp.addAction(self.actionVideoTutorial)
        self.menuHelp.addAction(self.actionJoinCommunity)

        # Main content area below the menubar
        self.main_content_area = QWidget()
        # This widget needs to stretch to fill the remaining space
        main_layout.addWidget(self.main_content_area, 1) # Add stretch factor of 1
        self.main_content_area.setObjectName("main_content_area")
        self.main_content_area.setStyleSheet("""
            #main_content_area {
                background-color: #FAFAFA;
                border: 1px solid #285A23;
                border-top: 1px solid #BBBBBB;
                
            }
            QLabel {
                color: #9F8888;
                font-size: 14px;
                border: none;
                padding: 5px;
            }
            QPushButton {
                background-color: #EDEDED;
                border: 1px solid #d0d0d0;
                padding: 6px 16px;
                color: #514E4E;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #BBBBBB,
                    stop: 0.26 #E8E8E8,
                    stop: 1 #EDEDED
                    );
                border-color: #806C6C;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)

        # Main vertical layout for content inside main_content_area
        content_layout = QVBoxLayout(self.main_content_area)
        content_layout.setContentsMargins(0,0,0,0)
        content_layout.setSpacing(0)

        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(0)  # Add spacing between all buttons
        button_layout.setContentsMargins(5, 5, 5, 5)  # Add some margin around the layout

        # ------------------------------------------------------------

        # Add buttons to left container
        self.edit_button = QPushButton()
        self.edit_button.setObjectName(u"edit_button")
        self.edit_button.setIcon(QIcon(":/images/edit_button.png"))
        self.edit_button.setFixedSize(60, 30)
        self.edit_button.setIconSize(QSize(25, 25))
        self.edit_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #EDEDED;
                border: 1px solid #BBBBBB;
                margin-right: 20px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #FAFAFA;
                border: 1px solid #888888;
            }
        """)
        button_layout.addWidget(self.edit_button)

        self.file_button= QPushButton()
        self.file_button.setObjectName(u"file_button")
        self.file_button.setFixedSize(50, 30)
        self.file_button.setIcon(QIcon(":/images/file_button.png"))
        self.file_button.setIconSize(QSize(30, 30))
        self.file_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #EDEDED;
                border: 1px solid #BBBBBB;
                margin-right: 20px;
            }
            QPushButton:hover {
                border: 1px solid #888888;
                background-color: #FAFAFA;
            }
        """)
        button_layout.addWidget(self.file_button)

        # Create save menu button
        self.save_button = QPushButton()
        self.save_button.setObjectName(u"save_button")
        self.save_button.setFixedSize(40, 30)
        self.save_button.setIcon(QIcon(":/images/save_button.png"))
        self.save_button.setIconSize(QSize(25, 25))
        self.save_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #EDEDED;
                border: 1px solid #BBBBBB;
               
            }
            QPushButton:hover {
                background-color: #FAFAFA;
                border: 1px solid #888888;
            }
            QPushButton::menu-indicator {
                image: url(:/images/arrow_down.png);
                width: 8px;
                height: 30px;
                subcontrol-position: right center;
                subcontrol-origin: padding;
                margin-right: 2px;
                margin-left: 2px;
                border-left: 1px solid #BBBBBB;
            }
        """)

        # Create save menu
        self.save_menu = QMenu(self.save_button)
        self.save_menu.setStyleSheet("""
            QMenu {
                background-color: #EDEDED;
                border: 1px solid #BBBBBB;
                padding: 2px;
                color: #9F8888;
            }

            QMenu::item {
                padding: 2px 2px;
                margin: 0px;
                border: none;
                min-height: 18px;
                font-size: 11px;
            }

            QMenu::item:selected {
                background-color: #FAFAFA;
            }

            QMenu::icon {
                width: 0px;
            }
        """)
        self.save_action = QAction("Save", self.save_menu)
        self.save_as_action = QAction("Save As", self.save_menu)
        self.save_menu.addAction(self.save_action)
        self.save_menu.addAction(self.save_as_action)
        self.save_button.setMenu(self.save_menu)

        button_layout.addWidget(self.save_button)

        # --- ADDED: Upload Excel Button ---
        self.upload_excel_button = QPushButton("Upload Excel")
        self.upload_excel_button.setObjectName("upload_excel_button")
        #CHANGES MADE BY RITIK: Connect Upload Excel button to file dialog
        self.upload_excel_button.clicked.connect(self.open_excel_dialog)

        self.upload_excel_button.setFixedSize(100, 30) # Wider to fit text
        self.upload_excel_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #217346; /* Excel Green Background */
                border: 1px solid #1a5c38;
                color: white; /* White Text */
                font-weight: bold;
                font-size: 10px;
                padding-left: 5px;
                padding-right: 5px;
                margin-left: 20px;
            }
            QPushButton:hover {
                background-color: #2b945a; /* Lighter Green on hover */
                border: 1px solid #217346;
            }
            QPushButton:pressed {
                background-color: #1a5c38;
            }
        """)
        self.upload_excel_button.setToolTip("Upload Excel")
        button_layout.addWidget(self.upload_excel_button)
        # ----------------------------------

        # ------------------------------------------------------------

        button_layout.addStretch()

        # Add label
        self.windows = QLabel("Windows:")
        button_layout.addWidget(self.windows)

        # add buttons to the right
        self.tutorial_tab = QPushButton("Tutorials")
        self.project_details_tab = QPushButton("Project Details")
        self.results_tab = QPushButton("Results")
        self.compare = QPushButton("Compare")

        # Add buttons to layout (Reordered: Project Details -> Results -> Compare -> Tutorials)
        button_layout.addWidget(self.project_details_tab)
        button_layout.addWidget(self.results_tab)
        button_layout.addWidget(self.compare)
        button_layout.addWidget(self.tutorial_tab)

        button_layout.addStretch()

        # Add the button layout to the main content layout
        content_layout.addLayout(button_layout)

        # ------------------------------------------------------------
        body_widget = QWidget()
        body_widget.setObjectName("body_widget")
        body_widget.setStyleSheet("""
            #body_widget {
                border-top: 1px solid #d0d0d0;
            }
        """)
        # ------------------------------------------------------------
        body_layout = QHBoxLayout(body_widget)
        body_layout.setSpacing(20)

        # Placeholders for dynamic widgets
        self.left_panel_placeholder = QWidget()
        self.left_panel_placeholder.setLayout(QVBoxLayout())
        self.right_panel_placeholder = QWidget()
        self.right_panel_placeholder.setLayout(QVBoxLayout())
        body_layout.addWidget(self.left_panel_placeholder, 1)
        body_layout.addWidget(self.right_panel_placeholder, 4)
        content_layout.addWidget(body_widget)

        # Store references to current widgets
        self.current_left_widget = None
        self.current_right_widget = None

        # Button click handlers
        def show_tutorial_widget():
            if self.current_left_widget:
                self.left_panel_placeholder.layout().removeWidget(self.current_left_widget)
                self.current_left_widget.setParent(None)
            self.current_left_widget = TutorialWidget()
            self.left_panel_placeholder.layout().addWidget(self.current_left_widget)
            self.current_left_widget.closed.connect(lambda: self.remove_left_widget())

        def show_results_widget():
            if self.current_right_widget:
                self.right_panel_placeholder.layout().removeWidget(self.current_right_widget)
                self.current_right_widget.setParent(None)
            self.current_right_widget = ResultsWidget()
            self.right_panel_placeholder.layout().addWidget(self.current_right_widget)
            self.current_right_widget.closed.connect(lambda: self.remove_right_widget())
            print("results widget")
        self.results_tab.clicked.connect(show_results_widget)

        def show_comparison_widget():
            if self.current_right_widget:
                self.right_panel_placeholder.layout().removeWidget(self.current_right_widget)
                self.current_right_widget.setParent(None)
            self.current_right_widget = ComparisonWidget()
            self.right_panel_placeholder.layout().addWidget(self.current_right_widget)
            self.current_right_widget.closed.connect(lambda: self.remove_right_widget())
        self.compare.clicked.connect(show_comparison_widget)

        def show_project_details_widget(widget_name=None):
            # Check for BOTH the old key and the new display name
            if widget_name == KEY_STRUCTURE_WORKS_DATA or widget_name == "Construction work data":
                # treat it as foundation
                widget_name = KEY_FOUNDATION
            if widget_name and widget_name in self.widget_map:                
                # Tabs are already visible
                if self.tabs_active:
                    if self.active_tab_widgets.get(widget_name) is not None:
                        # change active tab to that tab
                        index = self.active_tab_widgets[widget_name]
                        self.current_right_widget.activate_tab(index)
                else:
                    # Flush active tabs
                    self.remove_right_widget()
                    self.active_tab_widgets = {}
                    self.tabs_active = True
                    self.current_right_widget = CustomTabWidget(parent=self)
                    
                    # Add Tab widget
                    self.right_panel_placeholder.layout().addWidget(self.current_right_widget)
                    

                # Remove left widget first
                self.remove_left_widget()
                # Create left panel
                self.current_left_widget = ProjectDetailsLeft(self.widget_map, parent=self)
                self.left_panel_placeholder.layout().addWidget(self.current_left_widget)
                self.current_left_widget.closed.connect(lambda: self.remove_left_widget())
                self.current_left_widget.handle_button_selection(button_name=widget_name)
            else:
                # Switch to normal widget mode
                if self.current_right_widget:
                    self.right_panel_placeholder.layout().removeWidget(self.current_right_widget)
                    self.current_right_widget.setParent(None)
                self.tabs_active = False
                self.active_tab_widgets = {}  # Clear tab tracking
                self.current_right_widget = ProjectDetailsWidget()
                self.right_panel_placeholder.layout().addWidget(self.current_right_widget)
                self.current_right_widget.closed.connect(lambda: self.remove_right_widget())
                
            # Connect param_buttons if present
            if hasattr(self.current_right_widget, 'param_buttons'):
                for btn in self.current_right_widget.param_buttons:
                    btn.clicked.connect(lambda checked, b=btn: show_project_details_widget(b.text().strip()))

        def remove_right_widget():
            if self.current_right_widget:
                self.right_panel_placeholder.layout().removeWidget(self.current_right_widget)
                self.current_right_widget.setParent(None)
                self.current_right_widget = None
        self.remove_right_widget = remove_right_widget

        def remove_left_widget():
            if self.current_left_widget:
                self.left_panel_placeholder.layout().removeWidget(self.current_left_widget)
                self.current_left_widget.setParent(None)
                self.current_left_widget = None
        self.remove_left_widget = remove_left_widget

        self.tutorial_tab.clicked.connect(show_tutorial_widget)
        self.project_details_tab.clicked.connect(lambda: show_project_details_widget())
    
    def show_project_detail_widgets(self, widget_name):
        """Public method to show project detail widgets"""
        if widget_name == KEY_STRUCTURE_WORKS_DATA:
            # treat it as foundation
            widget_name = KEY_FOUNDATION
        if widget_name and widget_name in self.widget_map:
            # Tabs are already visible
            if self.tabs_active:
                if self.active_tab_widgets.get(widget_name) is not None:
                    # change active tab to that tab
                    index = self.active_tab_widgets[widget_name]
                    self.current_right_widget.activate_tab(index)
                else:
                    # add new tab
                    widget = self.widget_map[widget_name](database=self.database_manager, parent=self)
                    widget.next.connect(self.next_widget)
                    widget.back.connect(self.prev_widget)
                    index = self.current_right_widget.add_new_tab(widget, widget_name)
                    # add record of this widget
                    self.active_tab_widgets[widget_name] = index

    def next_widget(self, widget_name):
        current = list(self.widget_map.keys()).index(widget_name)
        next = list(self.widget_map.keys())[current + 1]
        if self.current_left_widget and hasattr(self.current_left_widget, 'all_param_buttons'):
            self.current_left_widget.all_param_buttons[next].click()
        self.show_project_detail_widgets(next)

    def prev_widget(self, widget_name):
        current = list(self.widget_map.keys()).index(widget_name)
        prev = list(self.widget_map.keys())[current - 1]
        if self.current_left_widget and hasattr(self.current_left_widget, 'all_param_buttons'):
            self.current_left_widget.all_param_buttons[prev].click()
        self.show_project_detail_widgets(prev)