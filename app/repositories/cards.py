from providers.anki import AnkiProvider
from repositories.users import UsersRepository


class CardsRepository:
    provider = AnkiProvider
    providers_cache = {}

    @classmethod
    async def save_card(cls, chat_id: int, front: str, back: str, tag: str = None):
        if cls.providers_cache.get(chat_id) is None:
            user_creds = UsersRepository.get_anki_creds_by_chat_id(chat_id)

            cls.providers_cache[chat_id] = AnkiProvider(username=user_creds['username'],
                                                        password=user_creds['password'])

        return await cls.providers_cache[chat_id].save_card(front, back)
