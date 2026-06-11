import sys
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "icon.ico"

class WeatherReport(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Report")
        self.setGeometry(100, 100, 400, 300)

        if ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(ICON_PATH)))

        self.layout = QVBoxLayout()

        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Nome da Cidade")
        self.layout.addWidget(self.city_input)

        self.get_weather_button = QPushButton("Obter Previsão do Tempo", self)
        self.get_weather_button.clicked.connect(self.get_weather)
        self.layout.addWidget(self.get_weather_button)

        self.weather_label = QLabel("", self)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.weather_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def get_weather(self):
        city = self.city_input.text()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        api_key = os.getenv("API_KEY")
        if not api_key:
            QMessageBox.critical(self, "Error", "Chave de API não encontrada no arquivo .env")
            return
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if data["cod"] != 200:
                QMessageBox.warning(self, "Error", f"Cidade não encontrada: {data['message']}")
                return

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            self.weather_label.setText(f"Temperatura: {temp}°C\nSensação Térmica: {feels_like}°C\nUmidade: {humidity}%")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocorreu um erro: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherReport()
    window.show()
    sys.exit(app.exec_())