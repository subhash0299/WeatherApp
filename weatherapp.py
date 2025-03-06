import requests
import tkinter as tk
from tkinter import messagebox


API_KEY = "YOUR-API-KEY"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌤 Weather App")
        self.root.geometry("450x400")
        self.root.config(bg="#2C3E50")  # Background color

        # Title Label
        self.title_label = tk.Label(root, text="🌍 Weather Forecast", font=("Helvetica", 18, "bold"), fg="white", bg="#2C3E50")
        self.title_label.pack(pady=10)

        # Input Field
        self.city_input = tk.Entry(root, font=("Arial", 14), fg="black", bg="white", relief="solid", borderwidth=2)
        self.city_input.pack(pady=10, ipadx=8, ipady=5)

        # Search Button
        self.search_button = tk.Button(root, text="🔍 Get Weather", font=("Arial", 12, "bold"), fg="white", bg="#3498DB",
                                       relief="raised", borderwidth=2, command=self.get_weather, padx=10, pady=5)
        self.search_button.pack(pady=5)

        # Weather Info Label
        self.weather_label = tk.Label(root, text="Enter a city to get started!", font=("Arial", 12), fg="white",
                                      bg="#2C3E50", justify="left", wraplength=400)
        self.weather_label.pack(pady=20)

    def get_weather(self):
        city = self.city_input.get().strip()

        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name!")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            # If the city name is incorrect
            if data.get("cod") != 200:
                messagebox.showwarning("⚠️"," City not found! Please enter a valid city.")
                return

            # Extract weather data
            actual_temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            min_temp = data["main"]["temp_min"]
            max_temp = data["main"]["temp_max"]
            weather = data["weather"][0]["description"].capitalize()
            wind_speed_kmh = round(data["wind"]["speed"] * 3.6, 2)  # Convert m/s to km/h
            
            self.weather_label.config(
                text=(
                    f"🌡 Temperature: {actual_temp}°C\n"
                    f"🤒 Feels Like: {feels_like}°C\n"
                    f"🔻 Min Temp: {min_temp}°C\n"
                    f"🔺 Max Temp: {max_temp}°C\n"
                    f"💨 Wind Speed: {wind_speed_kmh} km/h\n"
                    f"🌥 Condition: {weather}"
                ),
                fg="white"
            )

        except requests.exceptions.RequestException:
            messagebox.showerror("Network Error", "Unable to fetch data. Check your internet connection!")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
