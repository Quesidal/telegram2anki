import logging

import config
from providers.telegram import TelegramBot
from use_cases.add_new_card import AddNewCardUseCase

logger = logging.getLogger('controllers')


class Telegram2AnkiController:
    def start_server(self):
        TelegramBot(bot_token=config.BOT_TOKEN,
                    allowed_chat_ids=config.ALLOWED_CHAT_ID,
                    server_url=config.SERVER_URL).start(Telegram2AnkiController.telegram_message_handler)

    @staticmethod
    async def telegram_message_handler(telegram_message: str, chat_id: int):
        cls = Telegram2AnkiController
        logger.info(f"Message received: {telegram_message}")
        cards = cls.parse_telegram_message_to_anki_cards(telegram_message)

        response = "Card Added: \n"
        for front, back in cards:
            card = await AddNewCardUseCase.execute(chat_id, front, back)
            response += f"{card}\n"
        return response

    @staticmethod
    def parse_telegram_message_to_anki_cards(telegram_message: str) -> list:
        message_rows = telegram_message.split('\n')
        cards = []
        for row in message_rows:
            try:
                front, back = row.split(' - ')
                cards.append([front, back])
            except ValueError:
                logger.info(f"Couldn't parse row {row}")
        return cards
