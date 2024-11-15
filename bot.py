from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
import requests
from telegram.ext import ApplicationBuilder, CommandHandler,  MessageHandler, filters
# import settings

WEATHER_API_KEY= "39a56c1e858c31d721c7107d7d31e0df"
LOCATION = "https://maps.app.goo.gl/eJBDKhz1NGcJTtb96"
keyboard = [[KeyboardButton("Наіслати геолокацію", request_location= True),
             
             ]]

# Функція для обробки команди /start
async def start(update: Update, context):
    
    reply = ReplyKeyboardMarkup (keyboard=keyboard)
    await update.message.reply_text("Привіт, я чат бот погоди! Надішли свою геолокацію", reply_markup=reply)
    


async def get_location(update,context):
    location = update.message.location
    lat,lon  = location.latitude, location.longitude
    context.user_data[WEATHER_API_KEY] = (lat, lon)
    await update.message.reply_text(f'Ваші координати:{lat,lon}')

async   def get_weather(lat, lon, WEATHER_API_KEY):
    url = (f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=uk")
    response = requests.get(url)
    await update.message.reply_text(f'Погда у вашому регіоні::{lat,lon}')
    return response.json()
    




    
# Основна частина програми
if __name__ == '__main__':
    application = ApplicationBuilder().token("7347148528:AAF7UELcx96pl-5NIqHId3-mNWOP0GAMbs8").build()

    # Додаємо обробник для команди /start
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.LOCATION, get_location))
    application.add_handler(MessageHandler(filters.LOCATION, get_weather))


    # Запускаємо бота
    application.run_polling()