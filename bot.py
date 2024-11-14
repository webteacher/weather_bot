from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
import requests
from telegram.ext import ApplicationBuilder, CommandHandler,  MessageHandler, filters
import settings


keyboard = [[KeyboardButton("Наіслати геолокацію", request_location= True),
             
             ]]

# Функція для обробки команди /start
async def start(update: Update, context):
    
    reply = ReplyKeyboardMarkup (keyboard=keyboard)
    await update.message.reply_text("Привіт, я чат бот погоди! Надішли свою геолокацію", reply_markup=reply)
    


async def get_location(update,context):
    location = update.message.location
    lat,lon  = location.latitude, location.longitude
    context.user_data["location"] = (lat, lon)
    await update.message.reply_text(f'Ваші координати:{lat,lon}')


    
# Основна частина програми
if __name__ == '__main__':
    application = ApplicationBuilder().token(settings"7347148528:AAF7UELcx96pl-5NIqHId3-mNWOP0GAMbs8").build()

    # Додаємо обробник для команди /start
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.LOCATION, get_location))

    # Запускаємо бота
    application.run_polling()