"""
Home window for Osdag GUI.
Displays navigation, SVG cards, and home widgets.
"""
from osbridgelcca.desktop_app.resources.resources_rc import *

from PySide6.QtCore import QRectF, Signal, Slot

from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication,
    QLabel, QSizePolicy, QFrame, QScrollArea, QButtonGroup
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, Signal, QSize, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QFont, QIcon, QPainter, QColor, QPixmap
from PySide6.QtSvg import QSvgRenderer

from osbridgelcca.desktop_app.widgets.home.navbar import VerticalMenuBar
from osbridgelcca.desktop_app.widgets.home.top_right_buttons import TopButton
from osbridgelcca.desktop_app.widgets.home.central_widget import CentralWidget

# --- Theme Toggle Button ---
class ThemeToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)
        self.setObjectName("themeToggle")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_light = True
        self.clicked.connect(self._toggle_theme)
        self.update_icon()

    def _toggle_theme(self):
        self.theme_light = not self.theme_light
        self.update_icon()

    def update_icon(self):
        if self.theme_light:
            icon_path = ":/vectors/day_button.svg"
        else:
            icon_path = ":/vectors/night_button.svg"
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(25, 25))

class BackgroundSvgWidget(QWidget):
    def __init__(self, svg_light, svg_dark, parent=None):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.is_light = True
        self.light = QSvgRenderer(svg_light)
        self.dark = QSvgRenderer(svg_dark)
        self.pixmap = None
        self.setObjectName("svg_widget_background")
        self.setContentsMargins(0, 0, 0, 0) # Ensure no margins for drawing

    def updatePixmap(self):
        size = self.size()
        if not size.isValid():
            return
        renderer = self.light
        self.pixmap = QPixmap(size)
        self.pixmap.fill(Qt.transparent)
        painter = QPainter(self.pixmap)
        # Draw SVG background
        renderer.render(painter, QRectF(0, 0, size.width(), size.height()))
        # Draw left border
        pen = painter.pen()
        border_color = QColor("#90AF13")
        pen.setColor(border_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(0, 0, 0, self.height())
        painter.end()

    def resizeEvent(self, event):
        self.updatePixmap()

    def paintEvent(self, event):
        if self.pixmap:
            painter = QPainter(self)
            painter.drawPixmap(0, 0, self.pixmap)
        self.updatePixmap()

# --- End of background_svg_widget.py content ---
class FadeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self._opacity = 1.0
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.update()

    opacity = Property(float, getOpacity, setOpacity)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the current opacity for drawing the background
        painter.setOpacity(self._opacity)

        # Now, set opacity for child widgets if needed, or rely on their own painting
        # For child widgets to also respect this opacity, they need to be painted after this
        # or have their own opacity set. For simple layout containers, this is sufficient.
        painter.end() # End painter for the background drawing

        # Now, call the superclass paintEvent. This is where child widgets will be painted.
        # It's crucial to call this AFTER your custom background drawing.
        super().paintEvent(event)

class HomeWidget(QWidget):
    createNewProject = Signal()
    def __init__(self):
        super().__init__()
        # Ensures automatic deletion when closed
        self.setAttribute(Qt.WA_DeleteOnClose, True)
    
        self.menu_bar_data = {
                                "Home": [""]
                             }
        floating_navbar = FLOATING_NAVBAR = [
                                                (
                                                    ":/vectors/info_default.svg",
                                                    ":/vectors/info_hover.svg",
                                                    "   Info",
                                                    None
                                                ),
                                                (
                                                    ":/vectors/resources_default.svg",
                                                    ":/vectors/resources_hover.svg",
                                                    "Resources",
                                                    None
                                                ),
                                                (
                                                    ":/vectors/plugin_default.svg",
                                                    ":/vectors/plugin_hover.svg",
                                                    "Plugins",
                                                    None
                                                ),
                                                (
                                                    ":/vectors/load_default.svg",
                                                    ":/vectors/load_hover.svg", 
                                                    " Import",
                                                    None
                                                ),
                                            ]
        navbar_icons = NAVBAR_ICONS = {
                                        "Home": [":/vectors/nav_icons/home_default.svg", ":/vectors/nav_icons/home_clicked.svg"]
                                    }

        main_v_layout = QVBoxLayout(self)
        main_v_layout.setSpacing(0)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        
        # Horizontal line separating titleBar and tabWidget
        self.bottom_line = QWidget()
        self.bottom_line.setObjectName("BottomLine")
        self.bottom_line.setFixedHeight(1)
        main_v_layout.addWidget(self.bottom_line)

        main_h_layout = QHBoxLayout()
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        main_h_layout.setSpacing(0)

        # Left Navigation Bar
        self.nav_bar = VerticalMenuBar(self.menu_bar_data, navbar_icons)

        main_h_layout.addWidget(self.nav_bar, 2)

        self.content = BackgroundSvgWidget(":/vectors/background_light.svg", ":/vectors/background_dark.svg", parent=self)

        content_v_layout = QVBoxLayout(self.content)
        content_v_layout.setContentsMargins(0, 0, 0, 0)
        content_v_layout.setSpacing(0)

        # --- Top Horizontal Layout with SVG and Widget ---
        self.top_right_container = QWidget()
        self.top_right_container.setObjectName("home_top_right_container")

        self.top_right_h_layout = QHBoxLayout(self.top_right_container)
        self.top_right_h_layout.setContentsMargins(10, 5, 10, 0)
        self.top_right_h_layout.setSpacing(10)
        self.top_right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.top_svg_widget_1 = QSvgWidget()
        self.top_svg_widget_1.setFixedSize(286, 120)
        # No explicit stylesheet for QSvgWidget here. It will rely on its parent's background.
        self.top_right_h_layout.addWidget(self.top_svg_widget_1)

        self.top_widget_2 = QHBoxLayout()
        self.top_widget_2.setContentsMargins(0, 0, 15, 0)
        self.top_widget_2.setSpacing(2)
        self.button_group = QButtonGroup(self)
        self.buttons = [] # Store references to the created buttons

        # Instantiate and add the Buttons
        for i, (black_icon, white_icon, label, submenu_data) in enumerate(floating_navbar):
            button = TopButton(black_icon, white_icon, label)
            
            self.buttons.append(button)
            self.button_group.addButton(button, i) # Add button to the group with an ID
            self.top_widget_2.addWidget(button)

        # --- Theme Toggle Button ---
        self.theme_toggle = ThemeToggleButton(self)
        self.top_widget_2.addWidget(self.theme_toggle)

        self.top_right_h_layout.addStretch(1)
        self.top_right_h_layout.addLayout(self.top_widget_2)

        content_v_layout.addWidget(self.top_right_container)

        # ------------------Home-Widget---------------------
        central_widget = CentralWidget()
        central_widget.createNewProject.connect(self.createNewProject)

        content_v_layout.addWidget(central_widget)

        # --- Bottom Horizontal Layout with three SVG Widgets ---
        self.bottom_right_container = QWidget()
        self.bottom_right_container.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        self.bottom_right_h_layout = QHBoxLayout(self.bottom_right_container)
        self.bottom_right_h_layout.setContentsMargins(10, 10, 0, 10)
        self.bottom_right_h_layout.setSpacing(20)
        self.bottom_right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.bottom_svg_widget_1 = QSvgWidget()
        self.bottom_svg_widget_1.setFixedSize(100, 46)         # 1032 x 479(ratio 2.15) ~ 100 x 46
        self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_1)

        self.bottom_svg_widget_2 = QSvgWidget()
        self.bottom_svg_widget_2.setFixedSize(95, 47)         # 970 x 479(ratio 2.02) ~ 95 x 47
        self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_2)

        self.bottom_svg_widget_3 = QSvgWidget()
        self.bottom_svg_widget_3.setFixedSize(306, 35)  # 2048 x 234 (ratio 8.75) ~ 250 x 28.6
        self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_3, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.bottom_svg_widget_4 = QSvgWidget()
        self.bottom_svg_widget_4.setFixedSize(41, 43)       # 490 x 510(ratio 0.96) ~ 58 x 60
        self.bottom_right_h_layout.addWidget(self.bottom_svg_widget_4, alignment=Qt.AlignmentFlag.AlignBottom)

        self.top_svg_widget_1.load(":/vectors/LCC_label_light.svg")
        self.bottom_svg_widget_1.load(":/vectors/MOE_light.svg")
        self.bottom_svg_widget_2.load(":/vectors/MOS_light.svg")
        self.bottom_svg_widget_3.load(":/vectors/ConstructSteel_light.svg")
        self.bottom_svg_widget_4.load(":/vectors/INSDAG_light.svg")

        self.bottom_right_h_layout.addStretch(1)

        content_v_layout.addWidget(self.bottom_right_container)

        main_h_layout.addWidget(self.content, 8)       
        main_v_layout.addLayout(main_h_layout)

# if __name__ == "__main__":
#     import sys, os
#     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#     app = QApplication(sys.argv)
#     window = HomeWidget()
#     window.show()
#     sys.exit(app.exec())