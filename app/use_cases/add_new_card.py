import logging

from repositories.cards import CardsRepository

logger = logging.getLogger('use_cases')


class AddNewCardUseCase:
    @staticmethod
    async def execute(chat_id: int, front: str, back: str):
        try:
            card = await CardsRepository.save_card(chat_id=chat_id,
                                                   front=front,
                                                   back=back)
        except Exception as e:
            logger.info(f"Exception occur {str(e)}")
            return ''
        logger.info(f"Card saved {front} - {back}")
        return card
