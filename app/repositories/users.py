from config import USERS


class UsersRepository:
    @staticmethod
    def get_anki_creds_by_chat_id(chat_id: int):
        for user in USERS:
            if user['chat_id'] == chat_id:
                return {'username': user['anki_username'],
                        'password': user['anki_password']}
        raise Exception(f'User with chat_id:{chat_id} not found')
