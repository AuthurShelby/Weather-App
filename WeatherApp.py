import sys
from PyQt5.QtWidgets import QWidget , QApplication , QVBoxLayout , QLabel , QPushButton ,QLineEdit
from PyQt5.QtCore import Qt
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.EnterCityLabel = QLabel("Enter City Name:",self)
        self.CityInput = QLineEdit(self)
        self.GetButton = QPushButton("Get Weather",self)
        self.TempratureLabel = QLabel(self)
        self.EmojiLabel =QLabel(self)
        self.DescriptionLabel = QLabel(self)
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle("Weather App")
        VLayout = QVBoxLayout()
        VLayout.addWidget(self.EnterCityLabel)
        VLayout.addWidget(self.CityInput)
        VLayout.addWidget(self.GetButton)
        VLayout.addWidget(self.TempratureLabel)
        VLayout.addWidget(self.EmojiLabel)
        VLayout.addWidget(self.DescriptionLabel)
        self.setLayout(VLayout)
        
        self.EnterCityLabel.setObjectName("EnterCityLabel")
        self.CityInput.setObjectName("CityInput")
        self.GetButton.setObjectName("GetButton")
        self.TempratureLabel.setObjectName("TempratureLabel")
        self.EmojiLabel.setObjectName("EmojiLabel")
        self.DescriptionLabel.setObjectName("DescriptionLabel")

        self.EnterCityLabel.setAlignment(Qt.AlignCenter)
        self.CityInput.setAlignment(Qt.AlignCenter)
        self.TempratureLabel.setAlignment(Qt.AlignCenter)
        self.EmojiLabel.setAlignment(Qt.AlignCenter)
        self.DescriptionLabel.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
        QWidget{
            background-color:skyblue;
        }
        QLabel#EnterCityLabel , QLabel#TempratureLabel , QLabel#DescriptionLabel{
            font-family:Gill Sans;
            }
        QLineEdit#CityInput,QPushButton{
            background-color:white;
        }
        QLabel#EnterCityLabel{
            font-size:45px;
        }
        QLineEdit#CityInput{
            font-size:35px;
        }
        QPushButton{
            font-size:30px;
        }
        QLabel#TempratureLabel{
            font-size:75px;
        }
        QLabel#EmojiLabel{
            font-family:Segoe UI emoji;
            font-size:100px;

        }
        QLabel#DescriptionLabel{
            font-size:39px;
        }
        """)
        self.GetButton.clicked.connect(self.RetriveWeather)

    def RetriveWeather(self):
        city = self.CityInput.text()
        ApiKey = "4b0c5c9e20e0c85052b8078af13601f4"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={ApiKey}"

        try:
            generalData = requests.get(url)
            generalData.status_code
            generalData.raise_for_status()
            data = generalData.json()
            if data['cod'] == 200:
                self.DisplayWeather(data)   

        except requests.exceptions.HTTPError as httpError:
            match generalData.status_code:
                case 400:
                    self.DisplayError("Bad Request:\nPlease Check Your Input")
                
                case 401:
                    self.DisplayError("Unauthorized Access\nInvalid API Key")
                
                case 403:
                    self.DisplayError("Forbidden:\nAccess Denied")
                
                case 404:
                    self.DisplayError("Not Found:\nCity Not Found")
                
                case 500:
                    self.DisplayError("Internal Server Error:\nPlease Try Again Later")
                
                case 502:
                    self.DisplayError("Bad Gateway:\nPlease Try Again Later")
                
                case 503:
                    self.DisplayError("Service Unavailable:\nPlease Try Again Later")
                
                case 504:
                    self.DisplayError("Gateway Timeout:\nPlease Try Again Later")
                
                case _:
                    self.DisplayError(f"An Unexpected Error Occurred:\n{httpError}")
                

        except requests.exceptions.ConnectionError:
            self.DisplayError("Connection Error:\nPlease Check Your Internet Connection")
        
        except requests.exceptions.Timeout:
            self.DisplayError("Timeout Error:\nPlease Try Again Later")
        
        except requests.exceptions.TooManyRedirects:
            self.DisplayError("Too Many Redirects:\nPlease Try Again Later")
        
        except requests.exceptions.RequestException as RequestError:
            self.DisplayError(f"Request Error:\n{RequestError}")

    

    def DisplayError(self,message):
        self.TempratureLabel.setStyleSheet("font-size:30px; color:red;")
        self.EmojiLabel.setText("")
        self.DescriptionLabel.setText("")
        self.TempratureLabel.setText(message)

    def DisplayWeather(self,data):
        self.TempratureLabel.setStyleSheet("font-size:75px;")
        temp = str(int(data['main']['temp'] - 273.15))
        description = data['weather'][0]['description']
        IconCode = data['weather'][0]['id']
        self.TempratureLabel.setText(f"{temp}°C")            
        self.DescriptionLabel.setText(description)

        if IconCode >= 200 and IconCode <= 232:
            icon = "⛈️"
        
        elif IconCode >= 300 and IconCode <= 321:
            icon = "🌦️"
        
        elif IconCode >= 500 and IconCode <= 531:
            icon = "🌧️"
        
        elif IconCode >= 600 and IconCode <= 622:
            icon = "❄️"
        
        elif IconCode >= 701 and IconCode <= 741:
            icon = "🌫️" 

        elif IconCode == 762:
            icon = "🌋"

        elif IconCode == 771:
            icon = "💨"

        elif IconCode == 781:
            icon = "🌪️"
        
        elif IconCode == 800:
            icon = "☀️"
        
        elif IconCode >= 800 and IconCode <=804:
            icon = "☁️"
        else:
            icon = ""

        self.EmojiLabel.setText(icon)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherApp = WeatherApp()
    weatherApp.show()
    sys.exit(app.exec_())
