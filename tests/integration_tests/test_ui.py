import pytest
from PyQt5.QtWidgets import QApplication
from desktop_app.ui.main_window import MainWindow

@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    window = MainWindow()
    qtbot.addWidget(window)
    return window

# ✅ Test if UI Window Loads
@pytest.mark.integration
def test_ui_load(app):
    assert app.isVisible() is True
# Placeholder for test UI
