import logging

import firebase_admin
from firebase_admin import credentials, firestore

from telegram import *
from telegram.ext import *
from requests import *

# credentialData = credentials.Certificate("credentials.json")
# firebase_admin.initialize_app(credentialData)
#
# firestoreDb = firestore.client()
#
# snapshots = list(firestoreDb.collection(u'test').get())
# for snap in snapshots:
#     print(snap.to_dict())

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

Deneme1 = "deneme1"
Deneme2 = "deneme2"

name = ""

randomPeopleText = "Rastgele İnsan"
randomImageText = "Rastgele Resim"

randomPeopleUrl = "https://thispersondoesnotexist.com/image"
randomPImageUrl = "https://picsum.photos/1200"


deneme1sec = 'deneme1 basıldı'

buton1='1'
buton2='2'

def start(update, context):
    update.message.reply_text('Başladık hadi hayırlısı')


def listele(update, context):
    update.message.reply_text()


def help(update, context):
    update.message.reply_text('Yardım geliyor')


def naber(update, context):
    update.message.reply_text(f'iyi {update.effective_user.first_name} senden')


def hadi(update, context):
    update.message.reply_text(f'{update.effective_user.first_name} kime sövmemi istersin ?')



def echo(update, context):
    update.message.reply_text(update.message.text)



def bebek(update, context):
    update.message.reply_text('https://www.instagram.com/asiyenurzenginn/')


# def kaydet(update, context):
#     update.message.reply_text('kayıt tamamlandı')
#     firestoreDb.collection(u'test').add({'kayıt1'})

def resim(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(randomImageText)], [KeyboardButton(randomPeopleText)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Botuma Hoş Geldin!",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def messageHandler(update: Update, context: CallbackContext):
    if randomPeopleText in update.message.text:
        image = get(randomPeopleUrl).content
    if randomImageText in update.message.text:
        image = get(randomPImageUrl).content

    if image:
        context.bot.sendMediaGroup(chat_id=update.effective_chat.id, media=[InputMediaPhoto(image, caption="")])

        buttons = [[InlineKeyboardButton("👍", callback_data="like")], [InlineKeyboardButton("👎", callback_data="dislike")]]
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
                                 text="Resmi beğendin mi?")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    token = "2009712769:AAG71lr8rnSwO4GNaxrEl7Fi5o2N7IV5r9Y"
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("listele", listele))
    # dp.add_handler(CommandHandler("kaydet", kaydet))
    dp.add_handler(CommandHandler("hadi", hadi))
    dp.add_handler(CommandHandler("bebek", bebek))
    dp.add_handler(CommandHandler("naber", naber))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    option_handler = CommandHandler("resim", resim)
    dp.add_handler(option_handler)
    dp.add_handler(MessageHandler(Filters.text, messageHandler))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
