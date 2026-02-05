"""
Home widget for Osdag GUI.
Displays recent projects, modules, and search bar.
"""
import sys, shutil
import os, subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QLineEdit, QPushButton, QFileDialog,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QSize, Signal, QPropertyAnimation, QEasingCurve, QThread
from PySide6.QtGui import QIcon, QKeySequence, QColor, QFont, QShortcut, QFontMetrics
from PySide6.QtSvgWidgets import QSvgWidget

from osbridgelcca.desktop_app.resources.resources_rc import *
from osbridgelcca.desktop_app.widgets.home.recent_projects_widget import RecentProjectsWidget

# --- Enhanced Search Bar Widget ---
class SearchBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.is_focused = False
        self.setupUI()

    def setupUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.search_container = QWidget()
        self.search_container.setObjectName("searchContainer")
        container_layout = QHBoxLayout(self.search_container)
        container_layout.setContentsMargins(15, 0, 15, 0)
        container_layout.setSpacing(15)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search modules or projects...")
        self.search_input.setFixedHeight(48)
        self.search_input.setObjectName("searchInput")
        container_layout.addWidget(self.search_input)

        shortcut_layout = QHBoxLayout()
        shortcut_layout.setContentsMargins(0, 0, 0, 0)
        shortcut_layout.setSpacing(0)

        self.shortcut_hint = QLabel("Ctrl")
        self.shortcut_hint.setObjectName("shortcutKey")
        self.shortcut_hint.setFixedSize(32, 20)
        self.shortcut_hint.setAlignment(Qt.AlignmentFlag.AlignRight)
        shortcut_layout.addWidget(self.shortcut_hint)

        self.plus_label = QLabel("+")
        self.plus_label.setObjectName("plusLabel")
        self.plus_label.setFixedSize(20, 20)
        self.plus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shortcut_layout.addWidget(self.plus_label)

        self.l_key = QLabel("L")
        self.l_key.setObjectName("lKey")
        self.l_key.setFixedSize(20, 20)
        self.l_key.setAlignment(Qt.AlignmentFlag.AlignLeft)
        shortcut_layout.addWidget(self.l_key)

        container_layout.addLayout(shortcut_layout)

        self.search_icon = QSvgWidget(":/vectors/search_icon.svg")
        self.search_icon.setObjectName("searchIcon")
        self.search_icon.setFixedSize(20, 20)
        container_layout.addWidget(self.search_icon)
        

        layout.addWidget(self.search_container)
        
        self.search_input.focusInEvent = self._focus_in_event
        self.search_input.focusOutEvent = self._focus_out_event

    def _focus_in_event(self, event):
        self.is_focused = True
        self.search_container.setProperty("focused", True)
        self.search_container.style().unpolish(self.search_container)
        self.search_container.style().polish(self.search_container)
        QLineEdit.focusInEvent(self.search_input, event)

    def _focus_out_event(self, event):
        self.is_focused = False
        self.search_container.setProperty("focused", False)
        self.search_container.style().unpolish(self.search_container)
        self.search_container.style().polish(self.search_container)
        QLineEdit.focusOutEvent(self.search_input, event)

    @property
    def textChanged(self):
        return self.search_input.textChanged

    def setFocus(self):
        self.search_input.setFocus()

    def selectAll(self):
        self.search_input.selectAll()

class CentralWidget(QWidget):
    createNewProject = Signal()
    def __init__(self):
        super().__init__()
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.selected_item = None
        self.search_overlay = None
        
        self.setupUI()
        self.setupShortcuts()
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Hide overlay when clicking outside"""
        if self.search_overlay and self.search_overlay.isVisible():
            if event.type() == event.Type.MouseButtonPress:
                if not self.search_bar.geometry().contains(event.pos()) and \
                not self.search_overlay.geometry().contains(event.globalPos()):
                    self.search_overlay.hide()
        return super().eventFilter(obj, event)

    def setupShortcuts(self):
        search_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        search_shortcut.activated.connect(self.focus_search_bar)

    def focus_search_bar(self):
        self.search_bar.setFocus()
        self.search_bar.selectAll()

    def setupUI(self):
        content_area_layout = QVBoxLayout(self)
        content_area_layout.setContentsMargins(0, 0, 0, 0)
        content_area_layout.setSpacing(0)
        content_area_layout.addStretch()

        search_layout = QHBoxLayout()
        search_layout.addStretch()
        self.search_bar = SearchBarWidget()
        self.search_bar.setFixedWidth(500)

        search_layout.addWidget(self.search_bar)
        search_layout.addStretch()

        content_area_layout.addLayout(search_layout)
        content_area_layout.addStretch()

        sections_layout = QHBoxLayout()
        sections_layout.setSpacing(30)

        self.recent_projects = RecentProjectsWidget()

        sections_layout.addStretch(1)
        sections_layout.addWidget(self.recent_projects, stretch=4)
        self.recent_projects.createNewProject.connect(self.createNewProject)
        sections_layout.addStretch(1)
        content_area_layout.addLayout(sections_layout)
        content_area_layout.addStretch()
