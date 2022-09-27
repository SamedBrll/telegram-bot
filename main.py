import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import pyrebase

BOT_TOKEN = "5451842728:AAE3NmpugRkOyUE94EjHHNNVppSk35pRiec"

config = {
    "apiKey": "AIzaSyD09Mgieo4a-u-WOtnQRiCyrwbrqd8KS-k",
    "authDomain": "botdeneme-10ce5.firebaseapp.com",
    "projectId": "botdeneme-10ce5",
    "databaseURL": "https://botdeneme-10ce5-default-rtdb.firebaseio.com/",
    "storageBucket": "botdeneme-10ce5.appspot.com",
    "messagingSenderId": "218270457281",
    "appId": "1:218270457281:web:1bf2ac1d283071d159a340"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

izle = db.child("sayılar").child("revir").get()
print(izle.val())

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    firebase = pyrebase.initialize_app(config)

    db = firebase.database()


    izle = db.child("sayılar").child("revir").get()
    print(izle.val())
    update.message.reply_text(izle.val())


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Merhaba,aktif komutlar :\n/Durum => Güncel Sayılar\n/MuayeneEkle => 1 Adet Muayene Ekler\n"
                              "/SevkEkle => 1 Adet Sevk Ekler\n/Bilgi => Aktif Komutları Görmeye Yarar\n"
                              "/Reset => Muayene Ve Sevk Sayılarını Sıfırlar")


def sıfırla(update, context):
    db.child("sayılar").child("revir").update({"Muayene":0},"AIzaSyD09Mgieo4a-u-WOtnQRiCyrwbrqd8KS-k")
    db.child("sayılar").child("revir").update({"Sevk": 0}, "AIzaSyD09Mgieo4a-u-WOtnQRiCyrwbrqd8KS-k")
    update.message.reply_text("Güncelleme Tamamlandı")


def yenileM(update, context):
    izleM = db.child("sayılar").child("revir").child("Muayene").get()
    db.child("sayılar").child("revir").update({"Muayene":(izleM.val())+1},"AIzaSyD09Mgieo4a-u-WOtnQRiCyrwbrqd8KS-k")
    update.message.reply_text("Güncelleme Tamamlandı")

def yenileS(update, context):
    izleM = db.child("sayılar").child("revir").child("Sevk").get()
    db.child("sayılar").child("revir").update({"Sevk":(izleM.val())+1},"AIzaSyD09Mgieo4a-u-WOtnQRiCyrwbrqd8KS-k")
    update.message.reply_text("Güncelleme Tamamlandı")

def echo(update, context):
    """Echo the user message."""
    # update.message.text
    update.message.reply_text("Yanlış Komut Girdiniz!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("Durum", start))
    dp.add_handler(CommandHandler("Bilgi", help))
    dp.add_handler(CommandHandler("MuayeneEkle", yenileM))
    dp.add_handler(CommandHandler("SevkEkle", yenileS))
    dp.add_handler(CommandHandler("Reset", sıfırla))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
