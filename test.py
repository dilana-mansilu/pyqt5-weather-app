import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name: ", self)
        self.city_input = QLineEdit(self)
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 300, 250)
        self.get_weather_button_ = QPushButton("Get Weather", self)
        self.tempature_label = QLabel("", self)
        self.emoji_label = QLabel("", self)
        self.description_label = QLabel("", self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button_)
        vbox.addWidget(self.tempature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        # Alignment
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.tempature_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Object names
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button_.setObjectName("get_weather_button_")
        self.tempature_label.setObjectName("tempature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Stylesheet
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }       

            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }

            QLineEdit#city_input {
                font-size: 20px;
                padding: 5px;
            }

            QPushButton#get_weather_button_ {
                font-size: 25px;
                font-weight: bold;
                background-color: #0078D7;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }

            QPushButton#get_weather_button_:hover {
                background-color: #005A9E;
            }

            QLabel#tempature_label {
                font-size: 75px;
                color: blue;
            }

            QLabel#emoji_label {
                font-size: 100px;
                font-family: "Segoe UI Emoji";
            }

            QLabel#description_label {
                font-size: 50px;
                font-style: italic;
            }
        """)

        self.get_weather_button_.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "7ec3abb7fa6f30e19e15597df683f8b1"
        city = self.city_input.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
            else:
                self.display_error(data.get("message", "Unknown error"))

        except requests.exceptions.RequestException as e:
            self.display_error(str(e))

    def display_error(self, message):
        self.tempature_label.setText("Error")
        self.emoji_label.setText("⚠️")
        self.description_label.setText(message)

    def display_weather(self, data):
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"].capitalize()

        # choose emoji based on weather
        icon = "☀️"
        if "cloud" in description.lower():
            icon = "☁️"
        elif "rain" in description.lower():
            icon = "🌧️"
        elif "snow" in description.lower():
            icon = "❄️"

        self.tempature_label.setText(f"{temp:.1f}°C")
        self.emoji_label.setText(icon)
        self.description_label.setText(description)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
