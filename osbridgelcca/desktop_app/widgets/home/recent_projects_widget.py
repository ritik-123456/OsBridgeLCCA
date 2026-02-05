"""
Recent Projects Widget for displaying projects in a horizontal scrollable layout.
"""
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QCheckBox, QPushButton
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from osbridgelcca.desktop_app.resources.resources_rc import *

class RecentProjectsWidget(QWidget):
    """Widget for displaying recent projects in a horizontal scrollable layout."""
    
    createNewProject = Signal()
    compareProjects = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_cards = []
        self.setupUI()
        # Load dummy data
        self._load_dummy_data()
    
    def setupUI(self):
        """Setup the main layout with horizontal scroll area."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(0)
        
        # Title label
        title_widget = QWidget()
        title_widget.setObjectName("titleWidget")
        title_widget.setStyleSheet("""
            QWidget#titleWidget {
                background-color: rgba(0,0,0,0.05);
                border: 0px;
                border-top-right-radius: 5px;
                border-top-left-radius: 5px;
            }
        """)
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 10, 0, 0)
        title_layout.setSpacing(0)
        title_layout.addStretch()
        title_label = QLabel("Recent Projects")
        title_label.setObjectName("recentProjectsTitle")
        title_label.setStyleSheet("""
            QLabel#recentProjectsTitle {
                color: #000000;
                font-size: 24px;
                font-weight: 600;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        main_layout.addWidget(title_widget)
        
        # Create scroll area for horizontal scrolling
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setObjectName("recentProjectsScrollArea")
        scroll_area.setFixedHeight(320)  # Fixed height to prevent vertical scrolling
        
        # Set viewport background explicitly
        scroll_area.viewport().setStyleSheet("background-color: rgba(0,0,0,0.05); border: 0px;")
        
        # Content widget for project cards
        scroll_content = QWidget()
        scroll_content.setObjectName("scrollContent")
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(10)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 0)
        buttons_layout.setSpacing(15)
        buttons_layout.addStretch()
        
        # Create new project button
        self.create_new_btn = QPushButton("Create new project")
        self.create_new_btn.setObjectName("createNewButton")
        self.create_new_btn.setFixedSize(180, 40)
        self.create_new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_new_btn.setStyleSheet("""
            QPushButton#createNewButton {
                background-color: #90AF13;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 20px;
            }
            QPushButton#createNewButton:hover {
                background-color: #7d9710;
            }
            QPushButton#createNewButton:pressed {
                background-color: #90AF13;
            }
        """)
        self.create_new_btn.clicked.connect(self.createNewProject.emit)
        buttons_layout.addWidget(self.create_new_btn)
        
        # Compare projects button
        self.compare_btn = QPushButton("Compare projects")
        self.compare_btn.setObjectName("compareButton")
        self.compare_btn.setFixedSize(180, 40)
        self.compare_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.compare_btn.setStyleSheet("""
            QPushButton#compareButton {
                background-color: #90AF13;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 20px;
            }
            QPushButton#compareButton:hover {
                background-color: #7d9710;
            }
            QPushButton#compareButton:pressed {
                background-color: #90AF13;
            }
        """)
        self.compare_btn.clicked.connect(self.compareProjects.emit)
        buttons_layout.addWidget(self.compare_btn)
        
        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)
        
        self.scroll_content = scroll_content
        self.scroll_layout = scroll_layout
    
    def _load_dummy_data(self):
        """Load dummy project data for demonstration."""
        dummy_projects = [
            {
                "title": "Bridge 5245",
                "image_path": ":/images/recent_proj.png",
                "data": {"id": 1, "name": "Bridge 5245"} # must have aspect ratio 220:140
            },
            {
                "title": "Bridge 4246",
                "image_path": ":/images/recent_proj.png",
                "data": {"id": 2, "name": "Bridge 4246"}
            },
            {
                "title": "Bridge 5247",
                "image_path": ":/images/recent_proj.png",
                "data": {"id": 3, "name": "Bridge 5247"}
            },
            {
                "title": "Bridge 5257",
                "image_path": ":/images/recent_proj.png",
                "data": {"id": 4, "name": "Bridge 5257"}
            },
            {
                "title": "Bridge 9247",
                "image_path": ":/images/recent_proj.png",
                "data": {"id": 5, "name": "Bridge 9247"}
            }
        ]
        
        self.set_projects(dummy_projects)
    
    def add_project_card(self, title: str, image_path: str = None, project_data: dict = None):
        """
        Add a project card to the widget.
        
        Args:
            title: Project title to display
            image_path: Path to project image/thumbnail (optional)
            project_data: Dictionary containing project data (optional)
        """
        card = self._create_project_card(title, image_path, project_data)
        # Insert before the stretch at the end
        self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, card)
        self.project_cards.append(card)
        return card
    
    def _create_project_card(self, title: str, image_path: str = None, project_data: dict = None) -> QWidget:
        """Create a single project card widget."""
        card = QFrame()
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        card.setObjectName("projectCard")
        card.setFixedSize(240, 290)  # Reduced size for better fit
        card.setStyleSheet("""
            QFrame#projectCard {
                border: 2px solid #000000;
                border-radius: 8px;
                background-color: white;
            }
            QFrame#projectCard:hover {
                border: 2px solid #90AF13;
                background-color: #90AF13;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(8)
        
        # Project image
        image_label = QLabel()
        image_label.setObjectName("projectImage")
        image_label.setFixedHeight(140)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("""
            QLabel#projectImage {
                border: none;
                border-radius: 4px;
                background-color: #f5f5f5;
            }
        """)
        
        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale pixmap to fit while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    220, 140, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
        else:
            # Placeholder text if no image
            image_label.setText("No Image")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_label.setStyleSheet("""
                QLabel#projectImage {
                    border: none;
                    border-radius: 4px;
                    background-color: #f5f5f5;
                    color: #999;
                    font-size: 14px;
                }
            """)
        
        card_layout.addWidget(image_label)
        
        # Project title
        title_label = QLabel(title)
        title_label.setObjectName("projectTitle")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        title_label.setStyleSheet("""
            QLabel#projectTitle {
                color: #0066cc;
                font-size: 15px;
                font-weight: 600;
                padding: 5px 0px;
            }
        """)
        card_layout.addWidget(title_label)
        
        # Checkboxes section
        checkboxes_layout = QVBoxLayout()
        checkboxes_layout.setContentsMargins(0, 0, 0, 0)
        checkboxes_layout.setSpacing(6)
        
        # "Make copy" checkbox
        make_copy_checkbox = QCheckBox("Make copy")
        make_copy_checkbox.setObjectName("makeCopyCheckbox")
        make_copy_checkbox.setChecked(True)
        make_copy_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        make_copy_checkbox.setStyleSheet("""
            QCheckBox#makeCopyCheckbox {
                font-size: 12px;
                color: #000;
                spacing: 6px;
            }
            QCheckBox#makeCopyCheckbox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #000;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox#makeCopyCheckbox::indicator:checked {
                background-color: #FFF;
                border-color: #000;
                image: url(:/vectors/checked.svg);
            }
        """)
        checkboxes_layout.addWidget(make_copy_checkbox)
        
        # "Add to compare" checkbox
        add_to_compare_checkbox = QCheckBox("Add to compare")
        add_to_compare_checkbox.setObjectName("addToCompareCheckbox")
        add_to_compare_checkbox.setChecked(False)
        add_to_compare_checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        add_to_compare_checkbox.setStyleSheet("""
            QCheckBox#addToCompareCheckbox {
                font-size: 12px;
                color: #000;
                spacing: 6px;
            }
            QCheckBox#addToCompareCheckbox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #000;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox#addToCompareCheckbox::indicator:checked {
                background-color: #FFF;
                border-color: #000;
                image: url(:/vectors/checked.svg);
            }
        """)
        checkboxes_layout.addWidget(add_to_compare_checkbox)
        
        card_layout.addLayout(checkboxes_layout)
        card_layout.addStretch()
        
        # Store project data in card for later retrieval
        card.project_data = project_data
        card.title = title
        card.make_copy_checkbox = make_copy_checkbox
        card.add_to_compare_checkbox = add_to_compare_checkbox
        
        return card
    
    def clear_projects(self):
        """Clear all project cards from the widget."""
        for card in self.project_cards:
            card.setParent(None)
            card.deleteLater()
        self.project_cards.clear()
    
    def set_projects(self, projects: list):
        """
        Set multiple projects at once.
        
        Args:
            projects: List of dictionaries, each containing 'title', 'image_path', and 'data' keys
        """
        self.clear_projects()
        for project in projects:
            title = project.get('title', 'Untitled Project')
            image_path = project.get('image_path')
            data = project.get('data')
            self.add_project_card(title, image_path, data)
    
    def get_selected_projects_for_comparison(self):
        """Get list of projects that have 'Add to compare' checked."""
        selected = []
        for card in self.project_cards:
            if card.add_to_compare_checkbox.isChecked():
                selected.append({
                    'title': card.title,
                    'data': card.project_data
                })
        return selected