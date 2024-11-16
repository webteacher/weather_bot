from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
import requests
from telegram.ext import ApplicationBuilder, CommandHandler,  MessageHandler, filters
import settings

WEATHER_API_KEY = "39a56c1e858c31d721c7107d7d31e0df"
LOCATION = "https://maps.app.goo.gl/eJBDKhz1NGcJTtb96"
keyboard = [[KeyboardButton("Надіслати геолокацію", request_location=True),

             ]]


def get_weather(lat, lon, WEATHER_API_KEY):
    """отримуємо поточну погоду від openweathermap
    """
    url = (f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=uk")
    response = requests.get(url)
    return response.json()

def get_forecast(lat, lon, WEATHER_API_KEY):
    """отримуємо прогноз погоди від openweathermap
    """
    url = (f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=uk&cnt=3")
    response = requests.get(url)
    return response.json()

async def start(update: Update, context):
    """Функція для обробки команди /start
    """
    reply = ReplyKeyboardMarkup(keyboard=keyboard)
    await update.message.reply_text("Привіт, я чат бот погоди! Надішли свою геолокацію", reply_markup=reply)


async def get_location(update, context):
    location = update.message.location
    lat, lon = location.latitude, location.longitude
    context.user_data['location'] = (lat, lon)
    weather_info = get_weather(lat,lon,WEATHER_API_KEY)
    temp = weather_info['main']["temp"]
    description = weather_info["weather"][0]["description"]
    wind_speed = weather_info["wind"]["speed"]

    keyboard2 = [
        [KeyboardButton("Отримати прогноз")],
        [KeyboardButton("Надіслати геолокацію", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard2, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(f"Weather: {temp} °C, {description}, Швидкість вітру:{wind_speed} м/с", reply_markup = reply_markup)

async def send_forecast(update,context):
    lat, lon = context.user_data["location"]
    forecast_info = get_forecast(lat,lon,WEATHER_API_KEY)
    await update.message.reply_text(f"weather forecast {forecast_info}")
    


# Основна частина програми
if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TOKEN).build()

    # Додаємо обробник для команди /start
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.LOCATION, get_location))
    application.add_handler(MessageHandler(filters.TEXT,send_forecast))

    # Запускаємо бота
    application.run_polling()
