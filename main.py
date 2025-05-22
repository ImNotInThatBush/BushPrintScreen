import sys
import os
import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
import pyautogui

class OverlaySelector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showFullScreen()
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2))
        painter.setBrush(QtGui.QColor(0, 0, 0, 120))
        painter.drawRect(self.rect())
        rect = QtCore.QRect(self.begin, self.end).normalized()
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
        painter.fillRect(rect, QtCore.Qt.transparent)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        painter.drawRect(rect)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.begin = event.pos()
            self.end = self.begin
            self.update()
        elif event.button() == QtCore.Qt.RightButton:
            self.begin = QtCore.QPoint(0, 0)
            self.end = self.rect().bottomRight()
            self.update()
        elif event.button() == QtCore.Qt.MiddleButton:
            self.close()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.capture()
            self.close()

    def capture(self):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        region = (x1, y1, x2 - x1, y2 - y1)
        screenshot = pyautogui.screenshot(region=region)
        self.save_image(screenshot)

    def save_image(self, image):
        folder = os.path.join(os.path.expanduser("~"), "Pictures", "My Screen Shot")
        os.makedirs(folder, exist_ok=True)
        filename = datetime.datetime.now().strftime("screenshot_%Y-%m-%d_%H%M%S.png")
        image.save(os.path.join(folder, filename))


class TrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.menu = QtWidgets.QMenu(parent)

        capture_full = self.menu.addAction("📷 Schermo intero")
        capture_selection = self.menu.addAction("📐 Selezione area")
        quit_action = self.menu.addAction("❌ Esci")

        capture_full.triggered.connect(self.capture_fullscreen)
        capture_selection.triggered.connect(self.selection)
        quit_action.triggered.connect(QtWidgets.qApp.quit)

        self.setContextMenu(self.menu)

    def capture_fullscreen(self):
        screenshot = pyautogui.screenshot()
        self.save_image(screenshot)

    def selection(self):
        self.overlay = OverlaySelector()

    def save_image(self, image):
        folder = os.path.join(os.path.expanduser("~"), "Pictures", "My Screen Shot")
        os.makedirs(folder, exist_ok=True)
        filename = datetime.datetime.now().strftime("screenshot_%Y-%m-%d_%H%M%S.png")
        image.save(os.path.join(folder, filename))


def main():
    app = QtWidgets.QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(sys.argv[0]), "tray_icon.ico")
    tray_icon = TrayApp(QtGui.QIcon(icon_path))
    tray_icon.show()
    tray_icon.showMessage("Bush Print Screen", "Attivo nella tray", QtWidgets.QSystemTrayIcon.Information, 3000)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

