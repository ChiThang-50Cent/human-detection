import telebot
from decouple import config

BOT_TOKEN = config('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

def send_noti(photo_path, text):
    chat_id = '1331912442'

    photo = open(photo_path, 'rb')
    bot.send_photo(chat_id, photo)
    # bot.send_photo(chat_id, "FILEID")

    bot.send_message(chat_id, text)

if __name__ == '__main__':
    send_noti('./bedroom_window.jpg', 'bedroom_window')