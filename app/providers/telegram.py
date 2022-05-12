import asyncio
import logging

from telegram import Update
from telegram.ext import CallbackContext, DispatcherHandlerStop, TypeHandler, Updater

logger = logging.getLogger('providers')


class TelegramBot:
    def __init__(self, bot_token: str, allowed_chat_ids: list, server_url: str):
        self._bot_token = bot_token
        self._allowed_chat_ids = allowed_chat_ids
        self._server_url = server_url

    def start(self, message_handler: callable):
        def new_message_handler(update: Update, context: CallbackContext):
            message_text = update.message.text

            if update.message.chat_id not in self._allowed_chat_ids:
                logger.debug(f"{update.message.chat_id} not in allowed list: {self._allowed_chat_ids}")
                raise DispatcherHandlerStop

            loop = asyncio.new_event_loop()
            coro = message_handler(message_text, update.message.chat_id)
            result = loop.run_until_complete(coro)

            update.message.reply_text(result)
            raise DispatcherHandlerStop

        updater = Updater(self._bot_token)
        tg_new_message_handler = TypeHandler(Update, new_message_handler)
        updater.dispatcher.add_handler(tg_new_message_handler, -1)

        logger.info("Starting server log...")
        updater.start_webhook(listen='0.0.0.0',
                              port=80,
                              webhook_url=self._server_url)
