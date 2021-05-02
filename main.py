from logging import getLogger
from telegram import Bot
from telegram import Update
from echo.config import load_config
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters

logger = getLogger(__name__)
config = load_config()


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Сәлематсыз ба!\n"
             " Аты жөніңізді, телефон номеріңізді, тапсырыс бергіңіз келетін тағамдардың атын және мекен жайыңызды жазып жіберіңіз",
    )


def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = update.message.text
    if chat_id == config.FEEDBACK_USER_ID:
        reply = update.message.reply_to_message
        if reply:
            logger.info(reply)
            text = update.message.text
            bot.send_message(
                chat_id=reply.forward_from.id,
                text=text,
            )
        else:
            bot.send_message(
                chat_id=chat_id,
                text='Жауап беру үшін reply жасаҢыз',
            )
    else:
        bot.forward_message(
            chat_id=config.FEEDBACK_USER_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id,
        )

        bot.send_message(
            chat_id=chat_id,
            text='Сіздің тапсырысыңыз өңделуде.\n Тапсырысңыз қабылданған жағдайда хабардар етеміз🥰',
        )

def about_bbb(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Таңғы астар:\n\n"
             "омлет-890тг\n"
             "құймақ-590тг\n"
             "Европалық таңғы ас-1590тг\n\n"
             "Ыстық сусындар:\n\n"
             "американо-490тг\n"
             "латте-590тг\n"
             "сүтті шәй-890тг\n\n"
             "Тәттілер:\n\n"
             "брауни-690тг\n"
             "торт Вупи-1190тг\n"
             "эклер-490тг\n",
    )

def main():
    logger.info("Zapuskaem bota...")
    bot = Bot(
        token=config.TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    about_handler = CommandHandler("about", about_bbb)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(about_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

    logger.info("Zakonchili...")


if __name__ == "__main__":
    main()
