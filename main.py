import sys
import time

import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

from PyQt5.QtCore import Qt



class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()
        self.ask_city = QLabel("Enter a city: ", self)
        self.input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("70°C", self)
        self.weather_emoji_label = QLabel("☀️️", self)
        self.weather_description_label = QLabel("description", self)

        self.initializeUI()

        self.get_weather_button.clicked.connect(self.get_weather)

    def initializeUI(self):
        self.setWindowTitle("Python Weather App")
        self.setWindowIcon(QIcon("images/app_icon.png"))
        self.resize(700, 800)

        layout = QVBoxLayout()
        layout.addWidget(self.ask_city)
        layout.addWidget(self.input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.weather_emoji_label)
        layout.addWidget(self.weather_description_label)

        layout.setAlignment(self.ask_city, Qt.AlignCenter)
        self.input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.weather_emoji_label.setAlignment(Qt.AlignCenter)
        self.weather_description_label.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

        self.ask_city.setObjectName("ask_city")
        self.input.setObjectName("input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.weather_emoji_label.setObjectName("weather_emoji_label")
        self.weather_description_label.setObjectName("weather_description_label")

        self.setStyleSheet("""
        
            QLabel, QPushButton {
                font-family: Tahoma;
            }
            
            QLineEdit#input {
                height: 70px;
                font-size: 40px;
            }
            
            QPushButton#get_weather_button {
                height: 50px;
                font-size: 25px;
                
            }
            
            QLabel#weather_emoji_label {
                font-family: Segoe UI Emoji;
                font-size: 100px;
            }
             
            QLabel#ask_city {
                font-family: Times New Roman;
                font-size: 40px;
                font-style: italic;
            }        
            
            QLabel#temperature_label{
                font-size: 60px;
            }
            
            QLabel#weather_description_label {
                font-size: 40px;
            }
        """)

    def get_weather(self):

        start_time = time.time()  # for debug purposes

        # paste you own OpenWeather API key
        # to get your API key, visit https://openweathermap.org/api
        api_key = ""

        city = self.input.text()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            self.display_weather(data, start_time)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input", start_time)
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key", start_time)
                case 403:
                    self.display_error("Forbidden:\nAccess is denied", start_time)
                case 404:
                    self.display_error("Not found:\nCity not found", start_time)
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later", start_time)
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server", start_time)
                case 503:
                    self.display_error("Service Unavailable:\nServer is down", start_time)
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server", start_time)
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}", start_time)

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection", start_time)
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out", start_time)
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL", start_time)
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}", start_time)

    def display_error(self, message, start_time):
        self.weather_emoji_label.clear()
        self.weather_description_label.clear()
        self.temperature_label.setStyleSheet("font-size: 45px;")
        self.temperature_label.setText(message)

        # for debug purposes
        end_time = time.time()
        print(f"time taken: {(end_time - start_time):.3f}")
        start_time = 0

    def display_weather(self, data, start_time):
        self.temperature_label.setStyleSheet("font-size: 60px;")
        self.temperature_label.setText(f"{data["main"]["temp"]}°C")

        self.weather_description_label.setText(f"{data['weather'][0]['description']}")

        weather_id = data['weather'][0]['id']
        self.weather_emoji_label.setText(self.get_weather_emoji(weather_id))

        # for debug purposes
        end_time = time.time()
        print(f"time taken: {(end_time - start_time):.3f}")
        start_time = 0

    def get_weather_emoji(self, weather_id):
        if 200 <= weather_id <= 232:
            return "⚡"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 781:
            return "🌫️"
        elif 801 <=weather_id <= 804:
            return "⛅"
        else:
            return "☀️"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())