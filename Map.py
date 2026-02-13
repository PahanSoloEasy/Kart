import os
import sys

import requests
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

class Example(QMainWindow):
    def on_button_click(self):
        self.theme = "light"
        pass

    def on_button_click1(self):
        self.theme = "dark"
        pass
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.z = 15
        self.theme = "dark"
        self.delta = 0.001
        self.ll = [37.530887, 55.703118]
        self.light.clicked.connect(self.on_button_click)
        self.night.clicked.connect(self.on_button_click1)
        self.getImage()

    def getImage(self):
        map_params = {
            "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
            "ll": f'{self.ll[0]},{self.ll[1]}',
            "z": self.z,
            "theme": self.theme

        }
        response = requests.get('https://static-maps.yandex.ru/v1?', params=map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self,event):
        if event.key() == Qt.Key.Key_PageUp and self.z < 21:
            self.z += 1
        if event.key() == Qt.Key.Key_PageDown and self.z > 0:
            self.z -= 1
        if event.key() == Qt.Key.Key_Left and self.z > 0:
            self.ll[0] -= self.delta * (17 - self.z)
        if event.key() == Qt.Key.Key_Right and self.z > 0:
            self.ll[0] += self.delta * (17 - self.z)
        if event.key() == Qt.Key.Key_Up:
            self.ll[1] += self.delta * (17 - self.z)
        if event.key() == Qt.Key.Key_Down:
            self.ll[1] -= self.delta * (17 - self.z)
        if event.key() == Qt.Key.Key_W:
            self.theme = "light"
        if event.key() == Qt.Key.Key_S:
            self.theme = "dark"
        self.getImage()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())