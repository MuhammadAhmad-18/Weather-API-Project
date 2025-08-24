import tkinter as tk
from tkinter import ttk, messagebox
import requests
import datetime as dt
# from PIL import Image, ImageTk
import io
import urllib.request


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast Pro")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")

        # Set theme colors
        self.primary_color = "#3498db"
        self.secondary_color = "#2980b9"
        self.accent_color = "#e74c3c"
        self.text_color = "#2c3e50"
        self.bg_color = "#f0f2f5"

        self.create_widgets()

    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=100)
        header_frame.pack(fill="x", padx=10, pady=10)

        # App Title
        title_label = tk.Label(
            header_frame,
            text="Weather Forecast Pro",
            font=("Helvetica", 24, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=20)

        # Weather icon (using emoji as a placeholder)
        weather_icon = tk.Label(
            header_frame,
            text="⛅",
            font=("Helvetica", 30),
            bg=self.primary_color,
            fg="white"
        )
        weather_icon.place(x=20, y=20)

        # Input Frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=20, padx=20, fill="x")

        # City Entry
        self.city_var = tk.StringVar()
        city_label = tk.Label(
            input_frame,
            text="Enter City:",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        city_label.grid(row=0, column=0, padx=5, sticky="w")

        self.city_entry = ttk.Entry(
            input_frame,
            textvariable=self.city_var,
            font=("Helvetica", 12),
            width=30
        )
        self.city_entry.grid(row=0, column=1, padx=5)

        # Search Button
        search_btn = ttk.Button(
            input_frame,
            text="Get Weather",
            command=self.get_weather,
            style="Accent.TButton"
        )
        search_btn.grid(row=0, column=2, padx=10)

        # Bind Enter key to search
        self.root.bind('<Return>', lambda event: self.get_weather())

        # Weather Display Frame
        self.weather_frame = tk.Frame(
            self.root, bg="white", bd=2, relief="groove")
        self.weather_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Initially hide weather frame
        self.weather_frame.pack_forget()

        # Configure styles
        self.configure_styles()

        # Set focus to entry
        self.city_entry.focus()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Configure button styles
        style.configure('TButton',
                        font=('Helvetica', 12),
                        padding=6,
                        background=self.primary_color,
                        foreground="white")

        style.configure('Accent.TButton',
                        font=('Helvetica', 12, 'bold'),
                        padding=6,
                        background=self.accent_color,
                        foreground="white")

        style.map('TButton',
                  background=[('active', self.secondary_color)],
                  foreground=[('active', 'white')])

        style.map('Accent.TButton',
                  background=[('active', '#c0392b')],
                  foreground=[('active', 'white')])

    def get_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return

        try:
            BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
            API_KEY = "Enter your own api key"
            url = BASE_URL + "appid=" + API_KEY + "&q=" + city + \
                "&units=metric"  # Added units=metric for Celsius

            response = requests.get(url).json()

            if response.get("cod") != 200:
                error_message = response.get(
                    "message", "Failed to fetch weather data")
                messagebox.showerror("Error", error_message.capitalize())
                return

            # Clear previous weather data
            for widget in self.weather_frame.winfo_children():
                widget.destroy()

            # Show weather frame
            self.weather_frame.pack(pady=10, padx=20, fill="both", expand=True)

            # Get weather data
            weather_data = {
                "city": f"{response['name']}, {response['sys']['country']}",
                "coordinates": f"{response['coord']['lat']}°N, {response['coord']['lon']}°E",
                "temperature": f"{response['main']['temp']}°C",
                "feels_like": f"{response['main']['feels_like']}°C",
                "weather": response['weather'][0]['description'].capitalize(),
                "icon": response['weather'][0]['icon'],
                "humidity": f"{response['main']['humidity']}%",
                "pressure": f"{response['main']['pressure']} hPa",
                "wind": f"{response['wind']['speed']} m/s",
                "min_temp": f"{response['main']['temp_min']}°C",
                "max_temp": f"{response['main']['temp_max']}°C",
                "sunrise": dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone']).strftime('%H:%M:%S'),
                "sunset": dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone']).strftime('%H:%M:%S')
            }

            # Display weather data
            self.display_weather(weather_data)

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to fetch weather data: {str(e)}")

    def display_weather(self, data):
        # City and Weather Header
        header_frame = tk.Frame(self.weather_frame, bg="white")
        header_frame.pack(fill="x", pady=(10, 20), padx=10)

        city_label = tk.Label(
            header_frame,
            text=data["city"],
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg=self.text_color
        )
        city_label.pack(side="left")

        # Weather icon from OpenWeatherMap
        try:
            icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@2x.png"
            with urllib.request.urlopen(icon_url) as u:
                image_data = u.read()
            image = Image.open(io.BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)

            icon_label = tk.Label(header_frame, image=photo, bg="white")
            icon_label.image = photo  # Keep a reference
            icon_label.pack(side="right", padx=10)
        except:
            pass  # If icon fails to load, continue without it

        # Current Weather
        current_frame = tk.Frame(self.weather_frame, bg="white")
        current_frame.pack(fill="x", pady=5, padx=20)

        temp_label = tk.Label(
            current_frame,
            text=data["temperature"],
            font=("Helvetica", 48, "bold"),
            bg="white",
            fg=self.text_color
        )
        temp_label.pack(side="left")

        weather_label = tk.Label(
            current_frame,
            text=data["weather"],
            font=("Helvetica", 16),
            bg="white",
            fg=self.text_color
        )
        weather_label.pack(side="left", padx=20, pady=20)

        feels_like_label = tk.Label(
            current_frame,
            text=f"Feels like {data['feels_like']}",
            font=("Helvetica", 12),
            bg="white",
            fg=self.text_color
        )
        feels_like_label.pack(side="left", padx=10)

        # Details Frame
        details_frame = tk.Frame(self.weather_frame, bg="white")
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Column
        left_frame = tk.Frame(details_frame, bg="white")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.create_detail_row(
            left_frame, "Minimum Temperature", data["min_temp"])
        self.create_detail_row(
            left_frame, "Maximum Temperature", data["max_temp"])
        self.create_detail_row(left_frame, "Humidity", data["humidity"])
        self.create_detail_row(left_frame, "Pressure", data["pressure"])

        # Right Column
        right_frame = tk.Frame(details_frame, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.create_detail_row(right_frame, "Wind Speed", data["wind"])
        self.create_detail_row(right_frame, "Coordinates", data["coordinates"])
        self.create_detail_row(right_frame, "Sunrise", data["sunrise"])
        self.create_detail_row(right_frame, "Sunset", data["sunset"])

    def create_detail_row(self, parent, label, value):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", pady=5)

        label = tk.Label(
            frame,
            text=label + ":",
            font=("Helvetica", 12),
            bg="white",
            fg=self.text_color,
            width=20,
            anchor="w"
        )
        label.pack(side="left")

        value = tk.Label(
            frame,
            text=value,
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg=self.primary_color,
            anchor="w"
        )
        value.pack(side="left")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

